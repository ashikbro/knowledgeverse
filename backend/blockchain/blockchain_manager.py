"""
Blockchain integration for knowledge validation and rewards
"""
from web3 import Web3
from web3.middleware import geth_poa_middleware
import json
import logging
from typing import Dict, Optional


class BlockchainManager:
    """
    Manager for blockchain interactions
    """
    
    def __init__(self, provider_url: str, contract_address: str = None, private_key: str = None):
        """
        Initialize blockchain connection
        
        Args:
            provider_url: Blockchain node URL
            contract_address: Smart contract address
            private_key: Private key for transactions
        """
        self.w3 = Web3(Web3.HTTPProvider(provider_url))
        
        # Add PoA middleware if needed (for some testnets)
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        
        self.contract_address = contract_address
        self.private_key = private_key
        self.account = None
        
        if private_key:
            self.account = self.w3.eth.account.from_key(private_key)
        
        self.contract = None
        self.token_contract = None
        
        logging.info(f"Blockchain connection status: {self.w3.is_connected()}")
    
    def load_contract(self, contract_abi_path: str, token_abi_path: str = None):
        """
        Load smart contract
        
        Args:
            contract_abi_path: Path to KnowledgeGraph contract ABI
            token_abi_path: Path to KnowledgeToken contract ABI
        """
        if not self.contract_address:
            logging.warning("No contract address provided")
            return
        
        try:
            # Load KnowledgeGraph contract
            with open(contract_abi_path, 'r') as f:
                contract_abi = json.load(f)
            
            self.contract = self.w3.eth.contract(
                address=Web3.to_checksum_address(self.contract_address),
                abi=contract_abi
            )
            
            # Load token contract if provided
            if token_abi_path:
                with open(token_abi_path, 'r') as f:
                    token_abi = json.load(f)
                
                token_address = self.contract.functions.token().call()
                self.token_contract = self.w3.eth.contract(
                    address=token_address,
                    abi=token_abi
                )
            
            logging.info("Smart contracts loaded successfully")
        except Exception as e:
            logging.error(f"Error loading contracts: {e}")
    
    def submit_knowledge(self, content_hash: str) -> Optional[Dict]:
        """
        Submit knowledge to blockchain
        
        Args:
            content_hash: IPFS or content hash
        
        Returns:
            Transaction receipt
        """
        if not self.contract or not self.account:
            logging.error("Contract or account not initialized")
            return None
        
        try:
            # Build transaction
            nonce = self.w3.eth.get_transaction_count(self.account.address)
            
            tx = self.contract.functions.submitKnowledge(content_hash).build_transaction({
                'from': self.account.address,
                'nonce': nonce,
                'gas': 200000,
                'gasPrice': self.w3.eth.gas_price
            })
            
            # Sign and send transaction
            signed_tx = self.w3.eth.account.sign_transaction(tx, self.private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            
            # Wait for receipt
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            # Parse logs to get node ID
            logs = self.contract.events.NodeCreated().process_receipt(receipt)
            node_id = logs[0]['args']['nodeId'] if logs else None
            
            return {
                'transaction_hash': receipt['transactionHash'].hex(),
                'node_id': node_id,
                'status': receipt['status'],
                'gas_used': receipt['gasUsed']
            }
        except Exception as e:
            logging.error(f"Error submitting knowledge: {e}")
            return None
    
    def validate_knowledge(self, node_id: int, approved: bool) -> Optional[Dict]:
        """
        Validate a knowledge node
        
        Args:
            node_id: Node identifier
            approved: Validation approval status
        
        Returns:
            Transaction receipt
        """
        if not self.contract or not self.account:
            logging.error("Contract or account not initialized")
            return None
        
        try:
            nonce = self.w3.eth.get_transaction_count(self.account.address)
            
            tx = self.contract.functions.validateNode(node_id, approved).build_transaction({
                'from': self.account.address,
                'nonce': nonce,
                'gas': 150000,
                'gasPrice': self.w3.eth.gas_price
            })
            
            signed_tx = self.w3.eth.account.sign_transaction(tx, self.private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            return {
                'transaction_hash': receipt['transactionHash'].hex(),
                'status': receipt['status'],
                'gas_used': receipt['gasUsed']
            }
        except Exception as e:
            logging.error(f"Error validating knowledge: {e}")
            return None
    
    def get_node_info(self, node_id: int) -> Optional[Dict]:
        """
        Get knowledge node information from blockchain
        
        Args:
            node_id: Node identifier
        
        Returns:
            Node information
        """
        if not self.contract:
            logging.error("Contract not initialized")
            return None
        
        try:
            result = self.contract.functions.getNode(node_id).call()
            
            return {
                'contributor': result[0],
                'content_hash': result[1],
                'timestamp': result[2],
                'validations': result[3],
                'is_validated': result[4]
            }
        except Exception as e:
            logging.error(f"Error getting node info: {e}")
            return None
    
    def get_reputation(self, address: str) -> int:
        """
        Get user's reputation score
        
        Args:
            address: User's blockchain address
        
        Returns:
            Reputation score
        """
        if not self.contract:
            return 0
        
        try:
            return self.contract.functions.getReputation(
                Web3.to_checksum_address(address)
            ).call()
        except Exception as e:
            logging.error(f"Error getting reputation: {e}")
            return 0
    
    def get_token_balance(self, address: str) -> float:
        """
        Get user's token balance
        
        Args:
            address: User's blockchain address
        
        Returns:
            Token balance
        """
        if not self.token_contract:
            return 0.0
        
        try:
            balance = self.token_contract.functions.balanceOf(
                Web3.to_checksum_address(address)
            ).call()
            
            # Convert from wei to tokens
            decimals = self.token_contract.functions.decimals().call()
            return balance / (10 ** decimals)
        except Exception as e:
            logging.error(f"Error getting token balance: {e}")
            return 0.0
    
    def listen_for_events(self, event_name: str, from_block: int = 'latest'):
        """
        Listen for blockchain events
        
        Args:
            event_name: Name of the event to listen for
            from_block: Starting block number
        
        Returns:
            Event filter
        """
        if not self.contract:
            logging.error("Contract not initialized")
            return None
        
        try:
            if event_name == 'NodeCreated':
                event_filter = self.contract.events.NodeCreated.create_filter(fromBlock=from_block)
            elif event_name == 'NodeValidated':
                event_filter = self.contract.events.NodeValidated.create_filter(fromBlock=from_block)
            elif event_name == 'RewardDistributed':
                event_filter = self.contract.events.RewardDistributed.create_filter(fromBlock=from_block)
            else:
                logging.error(f"Unknown event: {event_name}")
                return None
            
            return event_filter
        except Exception as e:
            logging.error(f"Error creating event filter: {e}")
            return None
    
    def process_events(self, event_filter):
        """
        Process events from filter
        
        Args:
            event_filter: Event filter object
        
        Returns:
            List of events
        """
        try:
            events = event_filter.get_new_entries()
            return [dict(event['args']) for event in events]
        except Exception as e:
            logging.error(f"Error processing events: {e}")
            return []


class MockBlockchainManager(BlockchainManager):
    """
    Mock blockchain manager for testing without actual blockchain
    """
    
    def __init__(self):
        """Initialize mock blockchain"""
        self.nodes = {}
        self.next_node_id = 1
        self.user_reputations = {}
        self.user_balances = {}
        logging.info("Mock blockchain initialized")
    
    def submit_knowledge(self, content_hash: str) -> Optional[Dict]:
        """Mock submit knowledge"""
        node_id = self.next_node_id
        self.next_node_id += 1
        
        self.nodes[node_id] = {
            'content_hash': content_hash,
            'validations': 0,
            'is_validated': False
        }
        
        return {
            'transaction_hash': f"0xmock{node_id}",
            'node_id': node_id,
            'status': 1,
            'gas_used': 100000
        }
    
    def validate_knowledge(self, node_id: int, approved: bool) -> Optional[Dict]:
        """Mock validate knowledge"""
        if node_id in self.nodes and approved:
            self.nodes[node_id]['validations'] += 1
            
            if self.nodes[node_id]['validations'] >= 3:
                self.nodes[node_id]['is_validated'] = True
        
        return {
            'transaction_hash': f"0xmockval{node_id}",
            'status': 1,
            'gas_used': 80000
        }
    
    def get_node_info(self, node_id: int) -> Optional[Dict]:
        """Mock get node info"""
        if node_id in self.nodes:
            return {
                'contributor': '0xMockAddress',
                'content_hash': self.nodes[node_id]['content_hash'],
                'timestamp': 1234567890,
                'validations': self.nodes[node_id]['validations'],
                'is_validated': self.nodes[node_id]['is_validated']
            }
        return None
    
    def get_reputation(self, address: str) -> int:
        """Mock get reputation"""
        return self.user_reputations.get(address, 0)
    
    def get_token_balance(self, address: str) -> float:
        """Mock get token balance"""
        return self.user_balances.get(address, 0.0)
