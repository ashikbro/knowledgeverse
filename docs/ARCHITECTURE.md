# System Architecture

## High-Level Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend Layer                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Graph      │  │  Query       │  │ Contribution │         │
│  │ Visualization│  │ Interface    │  │   Form       │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                    React + Material-UI                          │
└────────────────────────┬────────────────────────────────────────┘
                         │ HTTP/WebSocket
┌────────────────────────┴────────────────────────────────────────┐
│                      API Layer (Flask)                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │     Auth     │  │  Knowledge   │  │    Search    │         │
│  │   Endpoints  │  │   Endpoints  │  │   Endpoints  │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└───┬──────────────┬──────────────┬─────────────────────┬────────┘
    │              │              │                     │
┌───▼────┐   ┌─────▼──────┐  ┌───▼──────┐      ┌──────▼────────┐
│ Neo4j  │   │ Blockchain │  │   NLP    │      │      GNN      │
│ Graph  │   │  Manager   │  │Processor │      │    Model      │
│   DB   │   │            │  │          │      │               │
└────────┘   └─────┬──────┘  └──────────┘      └───────────────┘
                   │
            ┌──────▼───────┐
            │   Ethereum   │
            │Smart Contract│
            └──────────────┘
```

## Component Details

### 1. Frontend Layer (React)
**Technology**: React 18, Material-UI, D3.js, react-force-graph

**Components**:
- **GraphVisualization**: Interactive 2D/3D graph rendering
- **QueryInterface**: Natural language query input and results
- **ContributionForm**: Knowledge submission interface
- **Dashboard**: Statistics and user information

**Features**:
- Real-time updates via WebSocket
- Responsive design
- Dark theme optimized for graph visualization
- Token balance and reputation display

### 2. API Layer (Flask)
**Technology**: Flask, Flask-SocketIO, Flask-JWT-Extended

**Endpoints**:
- Authentication (`/api/auth/*`)
- Knowledge management (`/api/knowledge/*`)
- Search and query (`/api/search`)
- Graph retrieval (`/api/graph`)
- User information (`/api/user/*`)
- Statistics (`/api/stats`)

**Features**:
- JWT-based authentication
- CORS support for cross-origin requests
- WebSocket for real-time updates
- Request validation and error handling

### 3. Database Layer (Neo4j)
**Technology**: Neo4j Graph Database

**Schema**:
```cypher
// Knowledge Node
(k:Knowledge {
  id: Integer,
  title: String,
  content: String,
  content_hash: String,
  category: String,
  contributor: String,
  timestamp: Integer,
  validations: Integer,
  is_validated: Boolean,
  embedding: JSON
})

// User Node
(u:User {
  address: String,
  username: String,
  reputation: Integer,
  created_at: Integer
})

// Relationships
(k1:Knowledge)-[:RELATES_TO]->(k2:Knowledge)
(k1:Knowledge)-[:PREREQUISITE_FOR]->(k2:Knowledge)
(k:Knowledge)-[:CONTRIBUTED_BY]->(u:User)
```

### 4. Blockchain Layer
**Technology**: Ethereum, Solidity, Web3.js

**Smart Contracts**:
- **KnowledgeToken (ERC20)**: Reward token
- **KnowledgeGraph**: Validation and governance

**Features**:
- Decentralized validation mechanism
- Automatic reward distribution
- Reputation tracking on-chain
- Immutable contribution records

### 5. AI Layer

#### Graph Neural Network (GNN)
**Technology**: PyTorch, PyTorch Geometric

**Architecture**:
- Graph Attention Networks (GAT)
- 3 layers with multi-head attention
- Node classification and link prediction

**Capabilities**:
- Infer hidden relationships
- Classify knowledge nodes
- Generate explanations for predictions

#### NLP Processor
**Technology**: Transformers, Sentence-BERT

**Models**:
- Sentence-BERT for embeddings
- DistilBERT for Q&A
- BERT-NER for entity extraction

**Capabilities**:
- Semantic search
- Intent classification
- Entity recognition
- Query expansion

## Data Flow

### Knowledge Contribution Flow
```
User → Frontend → API → Blockchain → Database
                      ↓
                   NLP Processing
                      ↓
              Generate Embedding
                      ↓
                Store in Graph DB
```

### Validation Flow
```
Validator → Frontend → API → Blockchain Contract
                             ↓
                   Check Threshold (3 validations)
                             ↓
                   Distribute Rewards (if threshold met)
                             ↓
                   Update Database
```

### Query Flow
```
User Query → Frontend → API → NLP Processor
                              ↓
                      Extract Intent & Entities
                              ↓
                      Semantic Search in DB
                              ↓
                      GNN Reasoning (optional)
                              ↓
                      Ranked Results → Frontend
```

### Real-time Update Flow
```
New Event → Backend → WebSocket → All Connected Clients
                 ↓
           Update Database
```

## Security Considerations

1. **Authentication**: JWT tokens with expiration
2. **Smart Contract**: Validation threshold prevents single-user manipulation
3. **Data Integrity**: Content hashing for verification
4. **API Security**: Rate limiting, input validation
5. **Database**: Parameterized queries prevent injection

## Scalability

1. **Database**: Neo4j clustering for horizontal scaling
2. **API**: Multiple Flask instances behind load balancer
3. **Blockchain**: Layer-2 solutions for faster transactions
4. **AI Models**: Model serving infrastructure (TensorFlow Serving, TorchServe)
5. **Frontend**: CDN for static assets

## Monitoring & Observability

1. **Metrics**: Prometheus for metrics collection
2. **Logging**: Structured logging with ELK stack
3. **Tracing**: Distributed tracing with Jaeger
4. **Alerting**: Alert manager for critical issues
5. **Dashboard**: Grafana for visualization

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Load Balancer                          │
└────────────┬──────────────────────┬──────────────────────────┘
             │                      │
    ┌────────▼────────┐    ┌───────▼────────┐
    │  Frontend CDN   │    │  API Cluster   │
    │    (Static)     │    │  (Flask x3)    │
    └─────────────────┘    └────────┬───────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
            ┌───────▼──────┐ ┌─────▼─────┐ ┌──────▼──────┐
            │  Neo4j       │ │ Ethereum  │ │ AI Services │
            │  Cluster     │ │   Node    │ │   (GPU)     │
            └──────────────┘ └───────────┘ └─────────────┘
```

## Technology Stack Summary

### Frontend
- React 18.2
- Material-UI 5.15
- react-force-graph 1.43
- Web3.js 4.3
- Socket.IO Client 4.6

### Backend
- Python 3.8+
- Flask 3.0
- Flask-SocketIO 5.3
- Flask-JWT-Extended 4.5

### AI/ML
- PyTorch 2.0
- PyTorch Geometric 2.4
- Transformers 4.35
- Sentence-Transformers 2.2

### Database & Blockchain
- Neo4j 5.14
- Solidity 0.8
- Web3.py 6.11

### Infrastructure
- Docker & Kubernetes (for deployment)
- Nginx (reverse proxy)
- Redis (caching)
- PostgreSQL (optional relational data)
