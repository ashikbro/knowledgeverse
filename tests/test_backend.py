"""
Test suite for KnowledgeVerse backend
"""
import pytest
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from blockchain.blockchain_manager import MockBlockchainManager


class TestBlockchainManager:
    """Test blockchain manager functionality"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.blockchain = MockBlockchainManager()
    
    def test_submit_knowledge(self):
        """Test knowledge submission"""
        result = self.blockchain.submit_knowledge("test_hash_123")
        
        assert result is not None
        assert result['node_id'] == 1
        assert result['status'] == 1
        assert 'transaction_hash' in result
    
    def test_validate_knowledge(self):
        """Test knowledge validation"""
        # First submit knowledge
        submit_result = self.blockchain.submit_knowledge("test_hash_456")
        node_id = submit_result['node_id']
        
        # Then validate it
        validate_result = self.blockchain.validate_knowledge(node_id, True)
        
        assert validate_result is not None
        assert validate_result['status'] == 1
        assert 'transaction_hash' in validate_result
    
    def test_get_node_info(self):
        """Test retrieving node information"""
        # Submit knowledge first
        submit_result = self.blockchain.submit_knowledge("test_hash_789")
        node_id = submit_result['node_id']
        
        # Get node info
        node_info = self.blockchain.get_node_info(node_id)
        
        assert node_info is not None
        assert node_info['content_hash'] == "test_hash_789"
        assert node_info['validations'] == 0
        assert node_info['is_validated'] == False
    
    def test_validation_threshold(self):
        """Test that validation threshold triggers validated status"""
        # Submit knowledge
        submit_result = self.blockchain.submit_knowledge("test_hash_threshold")
        node_id = submit_result['node_id']
        
        # Validate 3 times (threshold)
        for i in range(3):
            self.blockchain.validate_knowledge(node_id, True)
        
        # Check if validated
        node_info = self.blockchain.get_node_info(node_id)
        assert node_info['is_validated'] == True
        assert node_info['validations'] == 3
    
    def test_reputation_system(self):
        """Test reputation tracking"""
        address = "0xTestAddress"
        
        # Initial reputation should be 0
        reputation = self.blockchain.get_reputation(address)
        assert reputation == 0
    
    def test_token_balance(self):
        """Test token balance retrieval"""
        address = "0xTestAddress"
        
        # Initial balance should be 0
        balance = self.blockchain.get_token_balance(address)
        assert balance == 0.0


def test_import_modules():
    """Test that all modules can be imported"""
    try:
        from ai.gnn_model import KnowledgeGNN, ReasoningEngine
        from ai.nlp_processor import NLPProcessor
        from database.graph_db import KnowledgeGraphDB
        from blockchain.blockchain_manager import BlockchainManager
        
        # If we get here, all imports succeeded
        assert True
    except ImportError as e:
        pytest.fail(f"Failed to import module: {e}")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
