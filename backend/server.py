"""
Main Flask API server for Knowledge Graph
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os
from dotenv import load_dotenv
import logging
from datetime import datetime
import hashlib

# Import custom modules
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.graph_db import KnowledgeGraphDB
from blockchain.blockchain_manager import MockBlockchainManager
from ai.nlp_processor import NLPProcessor
from ai.gnn_model import ReasoningEngine

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('JWT_SECRET', 'dev-secret-key')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET', 'dev-secret-key')

# Enable CORS
CORS(app)

# Initialize JWT
jwt = JWTManager(app)

# Initialize SocketIO for real-time updates
socketio = SocketIO(app, cors_allowed_origins="*")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize components
db = None
blockchain = None
nlp_processor = None
reasoning_engine = None


def initialize_services():
    """Initialize all services"""
    global db, blockchain, nlp_processor, reasoning_engine
    
    try:
        # Initialize database
        neo4j_uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
        neo4j_user = os.getenv('NEO4J_USER', 'neo4j')
        neo4j_password = os.getenv('NEO4J_PASSWORD', 'password')
        
        # Use mock database for now if Neo4j not available
        try:
            db = KnowledgeGraphDB(neo4j_uri, neo4j_user, neo4j_password)
            logger.info("Neo4j database connected")
        except Exception as e:
            logger.warning(f"Neo4j not available, using mock: {e}")
            db = None
        
        # Initialize blockchain (using mock for now)
        blockchain = MockBlockchainManager()
        logger.info("Blockchain manager initialized")
        
        # Initialize AI components (optional, may not work without models)
        try:
            nlp_processor = NLPProcessor()
            logger.info("NLP processor initialized")
        except Exception as e:
            logger.warning(f"NLP processor not available: {e}")
            nlp_processor = None
        
        try:
            reasoning_engine = ReasoningEngine()
            logger.info("Reasoning engine initialized")
        except Exception as e:
            logger.warning(f"Reasoning engine not available: {e}")
            reasoning_engine = None
        
    except Exception as e:
        logger.error(f"Error initializing services: {e}")


# API Routes

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'services': {
            'database': db is not None,
            'blockchain': blockchain is not None,
            'nlp': nlp_processor is not None,
            'gnn': reasoning_engine is not None
        }
    })


@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login with blockchain address"""
    data = request.json
    address = data.get('address')
    
    if not address:
        return jsonify({'error': 'Address required'}), 400
    
    # Create JWT token
    access_token = create_access_token(identity=address)
    
    # Get user info
    reputation = blockchain.get_reputation(address) if blockchain else 0
    balance = blockchain.get_token_balance(address) if blockchain else 0
    
    return jsonify({
        'access_token': access_token,
        'address': address,
        'reputation': reputation,
        'balance': balance
    })


@app.route('/api/knowledge', methods=['POST'])
@jwt_required()
def submit_knowledge():
    """Submit new knowledge to the graph"""
    try:
        data = request.json
        current_user = get_jwt_identity()
        
        title = data.get('title')
        content = data.get('content')
        category = data.get('category', 'general')
        
        if not title or not content:
            return jsonify({'error': 'Title and content required'}), 400
        
        # Generate content hash
        content_hash = hashlib.sha256(f"{title}{content}".encode()).hexdigest()
        
        # Process with NLP if available
        embedding = []
        if nlp_processor:
            try:
                embedding = nlp_processor.encode_text([content])[0].tolist()
            except Exception as e:
                logger.warning(f"NLP processing failed: {e}")
        
        # Submit to blockchain
        blockchain_result = blockchain.submit_knowledge(content_hash) if blockchain else None
        node_id = blockchain_result['node_id'] if blockchain_result else hash(content_hash) % 1000000
        
        # Store in database
        node_data = {
            'id': node_id,
            'title': title,
            'content': content,
            'content_hash': content_hash,
            'category': category,
            'contributor': current_user,
            'timestamp': int(datetime.now().timestamp()),
            'validations': 0,
            'is_validated': False,
            'embedding': embedding
        }
        
        if db:
            db.create_knowledge_node(node_data)
        
        # Emit real-time update
        socketio.emit('new_knowledge', node_data)
        
        return jsonify({
            'success': True,
            'node_id': node_id,
            'message': 'Knowledge submitted successfully',
            'blockchain_tx': blockchain_result['transaction_hash'] if blockchain_result else None
        })
    
    except Exception as e:
        logger.error(f"Error submitting knowledge: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/knowledge/<int:node_id>', methods=['GET'])
def get_knowledge(node_id):
    """Get knowledge node by ID"""
    try:
        if db:
            node = db.get_knowledge_node(node_id)
            if node:
                return jsonify(node)
        
        # Fallback to blockchain
        if blockchain:
            node_info = blockchain.get_node_info(node_id)
            if node_info:
                return jsonify(node_info)
        
        return jsonify({'error': 'Node not found'}), 404
    
    except Exception as e:
        logger.error(f"Error getting knowledge: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/knowledge/<int:node_id>/validate', methods=['POST'])
@jwt_required()
def validate_knowledge(node_id):
    """Validate a knowledge node"""
    try:
        data = request.json
        current_user = get_jwt_identity()
        approved = data.get('approved', True)
        
        # Submit validation to blockchain
        result = blockchain.validate_knowledge(node_id, approved) if blockchain else None
        
        # Update database
        if db and approved:
            node = db.get_knowledge_node(node_id)
            if node:
                new_validations = node.get('validations', 0) + 1
                is_validated = new_validations >= 3
                db.update_validation_status(node_id, new_validations, is_validated)
        
        # Emit real-time update
        socketio.emit('validation_update', {
            'node_id': node_id,
            'validator': current_user,
            'approved': approved
        })
        
        return jsonify({
            'success': True,
            'message': 'Validation recorded',
            'blockchain_tx': result['transaction_hash'] if result else None
        })
    
    except Exception as e:
        logger.error(f"Error validating knowledge: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/search', methods=['POST'])
def search_knowledge():
    """Search knowledge graph with NLP"""
    try:
        data = request.json
        query = data.get('query')
        
        if not query:
            return jsonify({'error': 'Query required'}), 400
        
        # Process query with NLP
        if nlp_processor:
            query_info = nlp_processor.process_query(query)
        else:
            query_info = {'original_query': query}
        
        # Search database
        results = []
        if db:
            # Try text search
            text_results = db.search_by_text(query, limit=10)
            results.extend(text_results)
            
            # If NLP available, also do semantic search
            if nlp_processor and text_results:
                texts = [r.get('content', '') for r in text_results]
                semantic_results = nlp_processor.semantic_search(query, texts, top_k=5)
                
                # Enhance results with similarity scores
                for i, result in enumerate(semantic_results):
                    idx = result['index']
                    if idx < len(results):
                        results[idx]['similarity'] = result['similarity']
        
        return jsonify({
            'query_info': query_info,
            'results': results,
            'count': len(results)
        })
    
    except Exception as e:
        logger.error(f"Error searching knowledge: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/graph', methods=['GET'])
def get_graph():
    """Get graph structure for visualization"""
    try:
        limit = request.args.get('limit', 100, type=int)
        
        if db:
            graph_data = db.get_graph_structure(limit=limit)
            return jsonify(graph_data)
        
        return jsonify({
            'nodes': [],
            'edges': []
        })
    
    except Exception as e:
        logger.error(f"Error getting graph: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/user/<address>', methods=['GET'])
def get_user_info(address):
    """Get user information and statistics"""
    try:
        reputation = blockchain.get_reputation(address) if blockchain else 0
        balance = blockchain.get_token_balance(address) if blockchain else 0
        
        contributions = []
        if db:
            contributions = db.get_user_contributions(address)
        
        return jsonify({
            'address': address,
            'reputation': reputation,
            'balance': balance,
            'contributions': len(contributions),
            'recent_contributions': contributions[:5]
        })
    
    except Exception as e:
        logger.error(f"Error getting user info: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/stats', methods=['GET'])
def get_statistics():
    """Get overall system statistics"""
    try:
        stats = {}
        
        if db:
            stats = db.get_statistics()
        else:
            stats = {
                'total_nodes': 0,
                'total_relationships': 0,
                'total_users': 0,
                'validated_nodes': 0
            }
        
        return jsonify(stats)
    
    except Exception as e:
        logger.error(f"Error getting statistics: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/reasoning/infer', methods=['POST'])
def infer_relationships():
    """Infer potential relationships using GNN"""
    try:
        if not reasoning_engine:
            return jsonify({'error': 'Reasoning engine not available'}), 503
        
        data = request.json
        # This would need graph data from the request
        # For now, return a placeholder
        
        return jsonify({
            'message': 'Relationship inference requires trained GNN model',
            'status': 'model_not_trained'
        })
    
    except Exception as e:
        logger.error(f"Error inferring relationships: {e}")
        return jsonify({'error': str(e)}), 500


# WebSocket events

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    logger.info('Client connected')
    emit('connection_response', {'status': 'connected'})


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    logger.info('Client disconnected')


@socketio.on('subscribe_updates')
def handle_subscribe():
    """Subscribe to real-time updates"""
    emit('subscription_confirmed', {'status': 'subscribed'})


if __name__ == '__main__':
    # Initialize services
    initialize_services()
    
    # Run server
    port = int(os.getenv('API_PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=True)
