# Quick Reference Guide

## 🚀 Quick Start

```bash
# 1. Clone and setup
git clone https://github.com/ashikbro/knowledgeverse.git
cd knowledgeverse
cp .env.example .env

# 2. Backend setup
pip install -r requirements.txt
python backend/server.py

# 3. Frontend setup (new terminal)
cd frontend
npm install
npm start
```

Access at: http://localhost:3000

## 📁 Project Structure

```
knowledgeverse/
├── backend/                    # Python Flask backend
│   ├── ai/                    # AI models (GNN, NLP)
│   ├── blockchain/            # Blockchain integration
│   ├── database/              # Neo4j interface
│   └── server.py              # Main API server
├── frontend/                  # React frontend
│   └── src/
│       ├── components/        # UI components
│       └── services/          # API services
├── contracts/                 # Solidity smart contracts
├── docs/                      # Documentation
└── tests/                     # Test suite
```

## 🔑 Key Files

| File | Purpose |
|------|---------|
| `backend/server.py` | Main Flask API server |
| `backend/ai/gnn_model.py` | Graph Neural Network implementation |
| `backend/ai/nlp_processor.py` | Natural Language Processing |
| `backend/blockchain/blockchain_manager.py` | Blockchain interface |
| `backend/database/graph_db.py` | Neo4j database interface |
| `contracts/KnowledgeGraph.sol` | Smart contracts |
| `frontend/src/App.js` | Main React app |
| `frontend/src/components/GraphVisualization.js` | Graph viewer |

## 🌐 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/api/auth/login` | POST | Login with address |
| `/api/knowledge` | POST | Submit knowledge |
| `/api/knowledge/:id` | GET | Get knowledge |
| `/api/knowledge/:id/validate` | POST | Validate knowledge |
| `/api/search` | POST | Search with NLP |
| `/api/graph` | GET | Get graph data |
| `/api/user/:address` | GET | Get user info |
| `/api/stats` | GET | Get statistics |

## 🧪 Testing

```bash
# Backend tests
pytest tests/

# Frontend tests
cd frontend && npm test

# Syntax validation
python -c "import ast; ast.parse(open('backend/server.py').read())"
```

## 🔧 Environment Variables

### Backend (.env)
```bash
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password
JWT_SECRET=your-secret
API_PORT=5000
```

### Frontend (.env)
```bash
REACT_APP_API_URL=http://localhost:5000
```

## 🐳 Docker Quick Start

```bash
# Using Docker Compose
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

## 📊 System Components

### Blockchain Layer
- **KnowledgeToken**: ERC20 token for rewards
- **KnowledgeGraph**: Validation and governance
- **Validation Threshold**: 3 approvals required
- **Base Reward**: 10 KNOW tokens

### AI Layer
- **GNN**: Graph Attention Networks (3 layers)
- **NLP**: Sentence-BERT + DistilBERT + BERT-NER
- **Features**: Semantic search, entity extraction, Q&A

### Database Layer
- **Graph DB**: Neo4j for knowledge storage
- **Nodes**: Knowledge, User
- **Relationships**: RELATES_TO, PREREQUISITE_FOR, CONTRIBUTED_BY

### Frontend Layer
- **Framework**: React 18 + Material-UI 5
- **Visualization**: react-force-graph with D3.js
- **Real-time**: Socket.IO for live updates

## 💡 Usage Examples

### Submit Knowledge
```bash
curl -X POST http://localhost:5000/api/knowledge \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "title": "Machine Learning",
    "content": "Machine learning is...",
    "category": "technology"
  }'
```

### Search Knowledge
```bash
curl -X POST http://localhost:5000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "What is artificial intelligence?"}'
```

### Get Graph Data
```bash
curl http://localhost:5000/api/graph?limit=50
```

## 🎨 Frontend Components

| Component | File | Purpose |
|-----------|------|---------|
| GraphVisualization | `GraphVisualization.js` | Interactive graph |
| QueryInterface | `QueryInterface.js` | AI-powered search |
| ContributionForm | `ContributionForm.js` | Submit knowledge |
| Dashboard | `Dashboard.js` | Statistics view |

## 🔐 Smart Contract Functions

```solidity
// Submit knowledge
submitKnowledge(contentHash) → nodeId

// Validate knowledge
validateNode(nodeId, approved) → success

// Get node info
getNode(nodeId) → (contributor, hash, timestamp, validations, validated)

// Get reputation
getReputation(address) → reputation
```

## 📈 Monitoring

```bash
# Health check
curl http://localhost:5000/health

# Database stats
curl http://localhost:5000/api/stats

# Neo4j browser
open http://localhost:7474
```

## 🛠️ Common Commands

```bash
# Start backend
python backend/server.py

# Start frontend
cd frontend && npm start

# Run tests
pytest tests/ -v

# Check syntax
python -c "import ast; ast.parse(open('backend/server.py').read())"

# View logs
tail -f logs/app.log
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Neo4j connection failed | Check if Neo4j is running: `docker ps` |
| Module not found | Install dependencies: `pip install -r requirements.txt` |
| Port already in use | Change port in `.env` file |
| Frontend can't connect | Check REACT_APP_API_URL in frontend/.env |

## 📚 Documentation

- [README.md](README.md) - Project overview
- [API.md](docs/API.md) - API documentation
- [ARCHITECTURE.md](docs/ARCHITECTURE.md) - System architecture
- [DEPLOYMENT.md](docs/DEPLOYMENT.md) - Deployment guide
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guide

## 🎯 Key Features Checklist

- [x] Blockchain-based validation
- [x] Tokenized rewards (KNOW tokens)
- [x] Graph Neural Networks (GAT)
- [x] NLP query processing
- [x] Real-time graph visualization
- [x] Semantic search
- [x] Explainable AI
- [x] User reputation system
- [x] WebSocket real-time updates
- [x] Category-based organization

## 🚦 Status Indicators

| Color | Meaning | Description |
|-------|---------|-------------|
| 🟢 Green | Validated | 3+ validations received |
| 🔵 Blue | Science | Science category |
| 🟣 Purple | Technology | Technology category |
| 🟠 Orange | History | History category |
| 🔵 Gray | General | General category |

## 📞 Support

- GitHub Issues: Report bugs
- GitHub Discussions: Ask questions
- Documentation: Read the docs

---

**Version**: 1.0.0  
**Last Updated**: 2024  
**License**: MIT
