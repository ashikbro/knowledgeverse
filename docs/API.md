# API Documentation

## Overview
KnowledgeVerse REST API for decentralized knowledge graph operations.

Base URL: `http://localhost:5000/api`

## Authentication
Most endpoints require JWT authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your_token>
```

## Endpoints

### POST /auth/login
Login with blockchain address and receive JWT token.

**Request:**
```json
{
  "address": "0x1234..."
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAi...",
  "address": "0x1234...",
  "reputation": 10,
  "balance": 50.0
}
```

### POST /knowledge
Submit new knowledge (requires authentication).

**Request:**
```json
{
  "title": "Machine Learning",
  "content": "Machine learning is...",
  "category": "technology"
}
```

**Response:**
```json
{
  "success": true,
  "node_id": 42,
  "message": "Knowledge submitted successfully",
  "blockchain_tx": "0xabc..."
}
```

### GET /knowledge/:id
Get knowledge node by ID.

**Response:**
```json
{
  "id": 42,
  "title": "Machine Learning",
  "content": "Machine learning is...",
  "category": "technology",
  "contributor": "0x1234...",
  "validations": 3,
  "is_validated": true
}
```

### POST /knowledge/:id/validate
Validate a knowledge node (requires authentication).

**Request:**
```json
{
  "approved": true
}
```

**Response:**
```json
{
  "success": true,
  "message": "Validation recorded",
  "blockchain_tx": "0xdef..."
}
```

### POST /search
Search knowledge with NLP processing.

**Request:**
```json
{
  "query": "What is artificial intelligence?"
}
```

**Response:**
```json
{
  "query_info": {
    "intent": "search",
    "entities": [...],
    "keywords": [...]
  },
  "results": [...],
  "count": 5
}
```

### GET /graph
Get graph structure for visualization.

**Query Parameters:**
- `limit`: Maximum number of nodes (default: 100)

**Response:**
```json
{
  "nodes": [...],
  "edges": [...]
}
```

### GET /user/:address
Get user information and statistics.

**Response:**
```json
{
  "address": "0x1234...",
  "reputation": 10,
  "balance": 50.0,
  "contributions": 5,
  "recent_contributions": [...]
}
```

### GET /stats
Get overall system statistics.

**Response:**
```json
{
  "total_nodes": 100,
  "total_relationships": 250,
  "total_users": 20,
  "validated_nodes": 75
}
```

## Error Responses
All error responses follow this format:
```json
{
  "error": "Error message description"
}
```

HTTP Status Codes:
- 400: Bad Request
- 401: Unauthorized
- 404: Not Found
- 500: Internal Server Error
- 503: Service Unavailable
