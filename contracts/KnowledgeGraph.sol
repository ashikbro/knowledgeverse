// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title KnowledgeToken
 * @dev ERC20 Token for rewarding knowledge contributions
 */
contract KnowledgeToken {
    string public name = "Knowledge Token";
    string public symbol = "KNOW";
    uint8 public decimals = 18;
    uint256 public totalSupply;
    
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;
    
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    
    constructor(uint256 _initialSupply) {
        totalSupply = _initialSupply * 10 ** uint256(decimals);
        balanceOf[msg.sender] = totalSupply;
    }
    
    function transfer(address _to, uint256 _value) public returns (bool success) {
        require(balanceOf[msg.sender] >= _value, "Insufficient balance");
        balanceOf[msg.sender] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(msg.sender, _to, _value);
        return true;
    }
    
    function approve(address _spender, uint256 _value) public returns (bool success) {
        allowance[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }
    
    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        require(_value <= balanceOf[_from], "Insufficient balance");
        require(_value <= allowance[_from][msg.sender], "Insufficient allowance");
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        allowance[_from][msg.sender] -= _value;
        emit Transfer(_from, _to, _value);
        return true;
    }
}

/**
 * @title KnowledgeGraph
 * @dev Smart contract for decentralized knowledge validation and rewards
 */
contract KnowledgeGraph {
    KnowledgeToken public token;
    
    struct KnowledgeNode {
        uint256 id;
        address contributor;
        string contentHash; // IPFS hash of knowledge content
        uint256 timestamp;
        uint256 validations;
        uint256 reputation;
        bool isValidated;
    }
    
    struct Validator {
        address validatorAddress;
        uint256 timestamp;
        bool approved;
    }
    
    mapping(uint256 => KnowledgeNode) public knowledgeNodes;
    mapping(uint256 => mapping(address => bool)) public hasValidated;
    mapping(uint256 => Validator[]) public nodeValidators;
    mapping(address => uint256) public userReputation;
    
    uint256 public nodeCounter;
    uint256 public constant VALIDATION_THRESHOLD = 3;
    uint256 public constant BASE_REWARD = 10 * 10**18; // 10 tokens
    uint256 public constant VALIDATOR_REWARD = 1 * 10**18; // 1 token
    
    event NodeCreated(uint256 indexed nodeId, address indexed contributor, string contentHash);
    event NodeValidated(uint256 indexed nodeId, address indexed validator, bool approved);
    event RewardDistributed(address indexed recipient, uint256 amount);
    
    constructor(address _tokenAddress) {
        token = KnowledgeToken(_tokenAddress);
    }
    
    /**
     * @dev Submit new knowledge to the graph
     */
    function submitKnowledge(string memory _contentHash) public returns (uint256) {
        nodeCounter++;
        
        knowledgeNodes[nodeCounter] = KnowledgeNode({
            id: nodeCounter,
            contributor: msg.sender,
            contentHash: _contentHash,
            timestamp: block.timestamp,
            validations: 0,
            reputation: 0,
            isValidated: false
        });
        
        emit NodeCreated(nodeCounter, msg.sender, _contentHash);
        return nodeCounter;
    }
    
    /**
     * @dev Validate a knowledge node
     */
    function validateNode(uint256 _nodeId, bool _approved) public {
        require(_nodeId > 0 && _nodeId <= nodeCounter, "Invalid node ID");
        require(!hasValidated[_nodeId][msg.sender], "Already validated");
        require(knowledgeNodes[_nodeId].contributor != msg.sender, "Cannot validate own submission");
        
        hasValidated[_nodeId][msg.sender] = true;
        
        nodeValidators[_nodeId].push(Validator({
            validatorAddress: msg.sender,
            timestamp: block.timestamp,
            approved: _approved
        }));
        
        if (_approved) {
            knowledgeNodes[_nodeId].validations++;
            
            // Check if validation threshold is reached
            if (knowledgeNodes[_nodeId].validations >= VALIDATION_THRESHOLD && 
                !knowledgeNodes[_nodeId].isValidated) {
                knowledgeNodes[_nodeId].isValidated = true;
                
                // Reward contributor
                token.transfer(knowledgeNodes[_nodeId].contributor, BASE_REWARD);
                userReputation[knowledgeNodes[_nodeId].contributor] += 10;
                emit RewardDistributed(knowledgeNodes[_nodeId].contributor, BASE_REWARD);
            }
            
            // Reward validator
            token.transfer(msg.sender, VALIDATOR_REWARD);
            userReputation[msg.sender] += 1;
            emit RewardDistributed(msg.sender, VALIDATOR_REWARD);
        }
        
        emit NodeValidated(_nodeId, msg.sender, _approved);
    }
    
    /**
     * @dev Get node details
     */
    function getNode(uint256 _nodeId) public view returns (
        address contributor,
        string memory contentHash,
        uint256 timestamp,
        uint256 validations,
        bool isValidated
    ) {
        KnowledgeNode memory node = knowledgeNodes[_nodeId];
        return (
            node.contributor,
            node.contentHash,
            node.timestamp,
            node.validations,
            node.isValidated
        );
    }
    
    /**
     * @dev Get user's reputation score
     */
    function getReputation(address _user) public view returns (uint256) {
        return userReputation[_user];
    }
}
