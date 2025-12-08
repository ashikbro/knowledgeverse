# 🧠 KnowledgeVerse

**Decentralized Knowledge Graph with AI-Powered Queries**

A revolutionary platform combining blockchain, artificial intelligence, and graph databases to create a decentralized, crowdsourced knowledge network.

## 🌟 Overview

KnowledgeVerse pioneers decentralized intellectual growth through interactive knowledge graphs and automated reasoning tools. Users contribute and monetize knowledge via blockchain-based validation, while AI-powered systems enable intuitive querying and relationship inference.

## ✨ Key Features

### 🔗 Blockchain Integration
- **Smart Contract Validation**: Decentralized validation of knowledge contributions
- **Tokenized Rewards**: Contributors earn KNOW tokens for validated knowledge
- **Reputation System**: Track user credibility and contribution quality
- **Transparent Governance**: All validations recorded on-chain

### 🤖 AI-Powered Intelligence
- **Graph Neural Networks (GNN)**: Advanced reasoning over knowledge relationships
- **Natural Language Processing**: Query the knowledge base conversationally
- **Semantic Search**: Find relevant knowledge using meaning, not just keywords
- **Explainable AI**: Understand how relationships are inferred

### 📊 Knowledge Graph Database
- **Neo4j Integration**: Powerful graph database for complex relationships
- **Real-time Visualization**: Interactive 2D/3D graph exploration
- **Relationship Inference**: AI discovers hidden connections
- **Category-based Organization**: Organize knowledge by domain

### 💎 User Experience
- **Intuitive Interface**: Modern React-based UI
- **Real-time Updates**: WebSocket integration for live changes
- **Contribution Dashboard**: Track your impact and rewards
- **Query Analytics**: Understand how your queries are processed

## 🏗️ Architecture

```
knowledgeverse/
├── backend/                  # Python/Flask backend
│   ├── ai/                  # AI models (GNN, NLP)
│   ├── blockchain/          # Blockchain integration
│   ├── database/            # Neo4j interface
│   └── api/                 # REST API endpoints
├── frontend/                # React frontend
│   ├── src/
│   │   ├── components/     # UI components
│   │   └── services/       # API services
├── contracts/              # Solidity smart contracts
├── models/                 # Trained AI models
└── docs/                   # Documentation
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Node.js 16+
- Neo4j 5.0+ (optional, can use mock)
- Ethereum node (optional, can use mock)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/ashikbro/knowledgeverse.git
cd knowledgeverse
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Install Node.js dependencies**
```bash
npm install
cd frontend && npm install
cd ..
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Start Neo4j (optional)**
```bash
# If you have Neo4j installed
neo4j start
```

### Running the Application

1. **Start the backend server**
```bash
python backend/server.py
```
The API will be available at `http://localhost:5000`

2. **Start the frontend (in a new terminal)**
```bash
cd frontend
npm start
```
The UI will be available at `http://localhost:3000`

## 📖 Usage Guide

### Contributing Knowledge

1. Navigate to the "Contribute" tab
2. Fill in the title, content, and category
3. Submit your knowledge
4. Wait for community validation (3 validations required)
5. Earn tokens once validated!

### Querying Knowledge

1. Go to the "AI Query" tab
2. Enter your question in natural language
3. View AI-processed results with relevance scores
4. Click on results to explore further

### Exploring the Graph

1. Visit the "Graph Visualization" tab
2. See the knowledge network in real-time
3. Nodes are colored by category
4. Green nodes are validated
5. Click nodes to see details

### Viewing Statistics

1. Check the "Dashboard" tab
2. See total nodes, validations, and users
3. Track network growth over time

## 🔧 API Endpoints

### Authentication
- `POST /api/auth/login` - Login with blockchain address

### Knowledge Management
- `POST /api/knowledge` - Submit new knowledge
- `GET /api/knowledge/:id` - Get knowledge by ID
- `POST /api/knowledge/:id/validate` - Validate knowledge

### Search & Query
- `POST /api/search` - Search with NLP processing
- `GET /api/graph` - Get graph structure

### User & Stats
- `GET /api/user/:address` - Get user information
- `GET /api/stats` - Get system statistics

## 🔐 Smart Contracts

### KnowledgeToken (ERC20)
- Token symbol: KNOW
- Decimals: 18
- Used for rewards and governance

### KnowledgeGraph
- `submitKnowledge(contentHash)` - Submit new knowledge
- `validateNode(nodeId, approved)` - Validate knowledge
- `getNode(nodeId)` - Get node information
- `getReputation(address)` - Get user reputation

## 🤖 AI Models

### Graph Neural Network (GNN)
- **Architecture**: Graph Attention Networks (GAT)
- **Purpose**: Infer relationships and classify nodes
- **Input**: Node embeddings + graph structure
- **Output**: Relationship predictions with confidence scores

### NLP Processor
- **Models**: Sentence-BERT, DistilBERT
- **Features**:
  - Semantic search
  - Entity extraction
  - Query intent classification
  - Question answering

## 🧪 Testing

```bash
# Backend tests
pytest tests/

# Frontend tests
cd frontend
npm test
```

## 📊 Data Flow

1. **Contribution**: User submits knowledge → Blockchain transaction → Database storage
2. **Validation**: Validators approve → Smart contract checks threshold → Rewards distributed
3. **Query**: User asks question → NLP processes → Semantic search → GNN reasoning → Results returned
4. **Visualization**: Database query → Graph data → Real-time rendering

## 🛠️ Development

### Adding New Knowledge Categories
Edit `backend/server.py` and `frontend/src/components/ContributionForm.js`

### Training GNN Models
```bash
python backend/ai/train_gnn.py --data ./data/knowledge_graph.json
```

### Deploying Smart Contracts
```bash
# Compile contracts
solc contracts/KnowledgeGraph.sol --bin --abi -o build/

# Deploy (using your preferred tool)
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Graph Neural Networks research community
- Ethereum and blockchain developers
- Neo4j graph database team
- Open source AI/ML community

## 📞 Support

- Issues: [GitHub Issues](https://github.com/ashikbro/knowledgeverse/issues)
- Discussions: [GitHub Discussions](https://github.com/ashikbro/knowledgeverse/discussions)

## 🗺️ Roadmap

- [ ] Multi-language support
- [ ] Mobile application
- [ ] Advanced visualization options
- [ ] Integration with more blockchains
- [ ] Federated learning for privacy
- [ ] Knowledge marketplace

---

Built with ❤️ by the KnowledgeVerse community
