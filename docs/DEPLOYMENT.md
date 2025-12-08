# Deployment Guide

## Prerequisites

### Required Software
- Docker 20.10+
- Docker Compose 2.0+
- Git
- Node.js 16+ (for local development)
- Python 3.8+ (for local development)

### Optional
- Kubernetes cluster (for production)
- Nginx (for production reverse proxy)
- SSL certificates (for HTTPS)

## Deployment Options

### Option 1: Docker Compose (Recommended for Development/Testing)

1. **Clone the repository**
```bash
git clone https://github.com/ashikbro/knowledgeverse.git
cd knowledgeverse
```

2. **Create docker-compose.yml**
```yaml
version: '3.8'

services:
  neo4j:
    image: neo4j:5.14
    ports:
      - "7474:7474"
      - "7687:7687"
    environment:
      - NEO4J_AUTH=neo4j/password123
      - NEO4J_PLUGINS=["apoc"]
    volumes:
      - neo4j_data:/data
      - neo4j_logs:/logs

  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    ports:
      - "5000:5000"
    environment:
      - NEO4J_URI=bolt://neo4j:7687
      - NEO4J_USER=neo4j
      - NEO4J_PASSWORD=password123
      - JWT_SECRET=your-secret-key-change-in-production
    depends_on:
      - neo4j
    volumes:
      - ./backend:/app/backend
      - ./models:/app/models

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:80"
    environment:
      - REACT_APP_API_URL=http://localhost:5000
    depends_on:
      - backend

volumes:
  neo4j_data:
  neo4j_logs:
```

3. **Create Dockerfile.backend**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend ./backend
COPY models ./models

EXPOSE 5000

CMD ["python", "backend/server.py"]
```

4. **Create frontend/Dockerfile**
```dockerfile
FROM node:16 as build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

5. **Start all services**
```bash
docker-compose up -d
```

6. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000
- Neo4j Browser: http://localhost:7474

### Option 2: Local Development Setup

1. **Setup Backend**
```bash
# Install Python dependencies
pip install -r requirements.txt

# Start Neo4j (via Docker)
docker run -d \
  --name neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/password123 \
  neo4j:5.14

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Start backend server
python backend/server.py
```

2. **Setup Frontend**
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

### Option 3: Kubernetes Deployment (Production)

1. **Create Kubernetes manifests**

**neo4j-deployment.yaml**
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: neo4j
spec:
  serviceName: neo4j
  replicas: 1
  selector:
    matchLabels:
      app: neo4j
  template:
    metadata:
      labels:
        app: neo4j
    spec:
      containers:
      - name: neo4j
        image: neo4j:5.14
        ports:
        - containerPort: 7474
        - containerPort: 7687
        env:
        - name: NEO4J_AUTH
          value: "neo4j/password123"
        volumeMounts:
        - name: neo4j-data
          mountPath: /data
  volumeClaimTemplates:
  - metadata:
      name: neo4j-data
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 10Gi
---
apiVersion: v1
kind: Service
metadata:
  name: neo4j
spec:
  ports:
  - port: 7474
    name: browser
  - port: 7687
    name: bolt
  selector:
    app: neo4j
```

**backend-deployment.yaml**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: backend
        image: your-registry/knowledgeverse-backend:latest
        ports:
        - containerPort: 5000
        env:
        - name: NEO4J_URI
          value: "bolt://neo4j:7687"
        - name: NEO4J_USER
          value: "neo4j"
        - name: NEO4J_PASSWORD
          valueFrom:
            secretKeyRef:
              name: neo4j-secret
              key: password
---
apiVersion: v1
kind: Service
metadata:
  name: backend
spec:
  type: LoadBalancer
  ports:
  - port: 5000
    targetPort: 5000
  selector:
    app: backend
```

**frontend-deployment.yaml**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
      - name: frontend
        image: your-registry/knowledgeverse-frontend:latest
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: frontend
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 80
  selector:
    app: frontend
```

2. **Deploy to Kubernetes**
```bash
# Create secrets
kubectl create secret generic neo4j-secret \
  --from-literal=password='your-secure-password'

kubectl create secret generic jwt-secret \
  --from-literal=secret='your-jwt-secret'

# Apply manifests
kubectl apply -f neo4j-deployment.yaml
kubectl apply -f backend-deployment.yaml
kubectl apply -f frontend-deployment.yaml

# Check status
kubectl get pods
kubectl get services
```

## Configuration

### Environment Variables

**Backend (.env)**
```bash
# Database
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-password

# Blockchain
BLOCKCHAIN_NETWORK=http://localhost:8545
CONTRACT_ADDRESS=0x...
PRIVATE_KEY=your-private-key

# Security
JWT_SECRET=your-jwt-secret

# API
API_PORT=5000

# AI Models
MODEL_PATH=./models
HUGGINGFACE_TOKEN=your-token
```

**Frontend (.env)**
```bash
REACT_APP_API_URL=http://localhost:5000
```

## Database Setup

### Initialize Neo4j

1. **Access Neo4j Browser**: http://localhost:7474
2. **Login** with credentials (neo4j/password123)
3. **Run initialization script**:

```cypher
// Create constraints
CREATE CONSTRAINT knowledge_id IF NOT EXISTS
FOR (k:Knowledge) REQUIRE k.id IS UNIQUE;

CREATE CONSTRAINT user_address IF NOT EXISTS
FOR (u:User) REQUIRE u.address IS UNIQUE;

// Create indexes
CREATE INDEX knowledge_category IF NOT EXISTS
FOR (k:Knowledge) ON (k.category);

CREATE INDEX knowledge_timestamp IF NOT EXISTS
FOR (k:Knowledge) ON (k.timestamp);
```

## Blockchain Setup

### Deploy Smart Contracts

1. **Install Hardhat**
```bash
npm install --save-dev hardhat @nomiclabs/hardhat-ethers ethers
```

2. **Create deployment script** (scripts/deploy.js)
```javascript
async function main() {
  // Deploy KnowledgeToken
  const Token = await ethers.getContractFactory("KnowledgeToken");
  const token = await Token.deploy(1000000); // 1M initial supply
  await token.deployed();
  console.log("Token deployed to:", token.address);

  // Deploy KnowledgeGraph
  const Graph = await ethers.getContractFactory("KnowledgeGraph");
  const graph = await Graph.deploy(token.address);
  await graph.deployed();
  console.log("Graph deployed to:", graph.address);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
```

3. **Deploy to testnet**
```bash
npx hardhat run scripts/deploy.js --network goerli
```

4. **Update backend configuration** with contract addresses

## Monitoring & Maintenance

### Health Checks

**Backend Health**
```bash
curl http://localhost:5000/health
```

**Neo4j Health**
```bash
curl http://localhost:7474/db/data/
```

### Logs

**Docker Compose**
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f neo4j
```

**Kubernetes**
```bash
kubectl logs -f deployment/backend
kubectl logs -f deployment/frontend
kubectl logs -f statefulset/neo4j
```

### Backup

**Neo4j Backup**
```bash
docker exec neo4j neo4j-admin backup \
  --backup-dir=/backups \
  --name=graph-backup
```

**Database Restore**
```bash
docker exec neo4j neo4j-admin restore \
  --from=/backups/graph-backup \
  --database=neo4j
```

## SSL/TLS Configuration

### Using Let's Encrypt with Nginx

1. **Install Certbot**
```bash
sudo apt-get install certbot python3-certbot-nginx
```

2. **Obtain Certificate**
```bash
sudo certbot --nginx -d knowledgeverse.example.com
```

3. **Auto-renewal**
```bash
sudo certbot renew --dry-run
```

## Performance Tuning

### Neo4j Optimization
```conf
# neo4j.conf
dbms.memory.heap.initial_size=2G
dbms.memory.heap.max_size=4G
dbms.memory.pagecache.size=2G
```

### Backend Optimization
- Use Gunicorn with multiple workers
- Enable Redis caching
- Implement connection pooling

### Frontend Optimization
- Enable gzip compression
- Use CDN for static assets
- Implement code splitting

## Troubleshooting

### Common Issues

**Neo4j Connection Failed**
```bash
# Check if Neo4j is running
docker ps | grep neo4j

# Check logs
docker logs neo4j
```

**Backend API Not Responding**
```bash
# Check if port is accessible
curl http://localhost:5000/health

# Check logs
docker logs knowledgeverse_backend_1
```

**Frontend Can't Connect to Backend**
- Verify REACT_APP_API_URL is correct
- Check CORS configuration in backend
- Ensure backend is accessible from frontend

## Scaling

### Horizontal Scaling
- Add more backend replicas
- Use load balancer (Nginx, HAProxy)
- Scale Neo4j with clustering

### Vertical Scaling
- Increase memory allocation
- Add GPU for AI models
- Use faster storage (SSD, NVMe)

## Security Checklist

- [ ] Change default passwords
- [ ] Use strong JWT secrets
- [ ] Enable HTTPS/SSL
- [ ] Configure firewall rules
- [ ] Regular security updates
- [ ] Implement rate limiting
- [ ] Enable audit logging
- [ ] Backup encryption
- [ ] Secret management (Vault, AWS Secrets Manager)

## Support

For deployment issues:
- Check logs first
- Review documentation
- Open GitHub issue
- Contact support team

---

Happy Deploying! 🚀
