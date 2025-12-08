"""
Neo4j Graph Database Interface for Knowledge Graph
"""
from neo4j import GraphDatabase
import logging
from typing import List, Dict, Optional
import json


class KnowledgeGraphDB:
    """
    Interface for managing knowledge graph in Neo4j
    """
    
    def __init__(self, uri: str, user: str, password: str):
        """
        Initialize database connection
        
        Args:
            uri: Neo4j database URI
            user: Database username
            password: Database password
        """
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self._setup_constraints()
        logging.info("Connected to Neo4j database")
    
    def close(self):
        """Close database connection"""
        self.driver.close()
    
    def _setup_constraints(self):
        """Create database constraints and indexes"""
        with self.driver.session() as session:
            # Create uniqueness constraints
            session.run("""
                CREATE CONSTRAINT knowledge_id IF NOT EXISTS
                FOR (k:Knowledge) REQUIRE k.id IS UNIQUE
            """)
            
            session.run("""
                CREATE CONSTRAINT user_address IF NOT EXISTS
                FOR (u:User) REQUIRE u.address IS UNIQUE
            """)
            
            # Create indexes for better performance
            session.run("""
                CREATE INDEX knowledge_timestamp IF NOT EXISTS
                FOR (k:Knowledge) ON (k.timestamp)
            """)
            
            session.run("""
                CREATE INDEX knowledge_category IF NOT EXISTS
                FOR (k:Knowledge) ON (k.category)
            """)
    
    def create_knowledge_node(self, node_data: Dict) -> Dict:
        """
        Create a new knowledge node
        
        Args:
            node_data: Dictionary containing node properties
        
        Returns:
            Created node data
        """
        with self.driver.session() as session:
            result = session.run("""
                CREATE (k:Knowledge {
                    id: $id,
                    title: $title,
                    content: $content,
                    content_hash: $content_hash,
                    category: $category,
                    contributor: $contributor,
                    timestamp: $timestamp,
                    validations: $validations,
                    is_validated: $is_validated,
                    embedding: $embedding
                })
                RETURN k
            """, 
                id=node_data['id'],
                title=node_data.get('title', ''),
                content=node_data.get('content', ''),
                content_hash=node_data.get('content_hash', ''),
                category=node_data.get('category', 'general'),
                contributor=node_data.get('contributor', ''),
                timestamp=node_data.get('timestamp', 0),
                validations=node_data.get('validations', 0),
                is_validated=node_data.get('is_validated', False),
                embedding=json.dumps(node_data.get('embedding', []))
            )
            
            record = result.single()
            return dict(record['k'])
    
    def get_knowledge_node(self, node_id: int) -> Optional[Dict]:
        """
        Retrieve a knowledge node by ID
        
        Args:
            node_id: Node identifier
        
        Returns:
            Node data or None if not found
        """
        with self.driver.session() as session:
            result = session.run("""
                MATCH (k:Knowledge {id: $id})
                RETURN k
            """, id=node_id)
            
            record = result.single()
            if record:
                node = dict(record['k'])
                # Parse embedding from JSON
                if 'embedding' in node:
                    node['embedding'] = json.loads(node['embedding'])
                return node
            return None
    
    def create_relationship(self, source_id: int, target_id: int, 
                          relationship_type: str, properties: Dict = None) -> bool:
        """
        Create a relationship between two knowledge nodes
        
        Args:
            source_id: Source node ID
            target_id: Target node ID
            relationship_type: Type of relationship
            properties: Optional relationship properties
        
        Returns:
            Success status
        """
        with self.driver.session() as session:
            props = properties or {}
            result = session.run("""
                MATCH (a:Knowledge {id: $source_id})
                MATCH (b:Knowledge {id: $target_id})
                CREATE (a)-[r:""" + relationship_type + """ $props]->(b)
                RETURN r
            """, source_id=source_id, target_id=target_id, props=props)
            
            return result.single() is not None
    
    def query_neighbors(self, node_id: int, depth: int = 1) -> List[Dict]:
        """
        Get neighboring nodes
        
        Args:
            node_id: Central node ID
            depth: Search depth
        
        Returns:
            List of neighboring nodes
        """
        with self.driver.session() as session:
            result = session.run("""
                MATCH (k:Knowledge {id: $id})-[r*1..""" + str(depth) + """]->(neighbor:Knowledge)
                RETURN DISTINCT neighbor, type(last(r)) as relationship
            """, id=node_id)
            
            neighbors = []
            for record in result:
                node = dict(record['neighbor'])
                if 'embedding' in node:
                    node['embedding'] = json.loads(node['embedding'])
                node['relationship'] = record['relationship']
                neighbors.append(node)
            
            return neighbors
    
    def search_by_category(self, category: str, limit: int = 10) -> List[Dict]:
        """
        Search knowledge nodes by category
        
        Args:
            category: Knowledge category
            limit: Maximum number of results
        
        Returns:
            List of matching nodes
        """
        with self.driver.session() as session:
            result = session.run("""
                MATCH (k:Knowledge {category: $category})
                RETURN k
                ORDER BY k.timestamp DESC
                LIMIT $limit
            """, category=category, limit=limit)
            
            nodes = []
            for record in result:
                node = dict(record['k'])
                if 'embedding' in node:
                    node['embedding'] = json.loads(node['embedding'])
                nodes.append(node)
            
            return nodes
    
    def search_by_text(self, search_text: str, limit: int = 10) -> List[Dict]:
        """
        Full-text search on knowledge nodes
        
        Args:
            search_text: Text to search for
            limit: Maximum number of results
        
        Returns:
            List of matching nodes
        """
        with self.driver.session() as session:
            result = session.run("""
                MATCH (k:Knowledge)
                WHERE k.title CONTAINS $text OR k.content CONTAINS $text
                RETURN k
                ORDER BY k.validations DESC, k.timestamp DESC
                LIMIT $limit
            """, text=search_text, limit=limit)
            
            nodes = []
            for record in result:
                node = dict(record['k'])
                if 'embedding' in node:
                    node['embedding'] = json.loads(node['embedding'])
                nodes.append(node)
            
            return nodes
    
    def get_graph_structure(self, limit: int = 100) -> Dict:
        """
        Get the entire graph structure for visualization
        
        Args:
            limit: Maximum number of nodes
        
        Returns:
            Graph data with nodes and edges
        """
        with self.driver.session() as session:
            # Get nodes
            nodes_result = session.run("""
                MATCH (k:Knowledge)
                RETURN k
                ORDER BY k.timestamp DESC
                LIMIT $limit
            """, limit=limit)
            
            nodes = []
            for record in nodes_result:
                node = dict(record['k'])
                if 'embedding' in node:
                    del node['embedding']  # Don't send embeddings for visualization
                nodes.append(node)
            
            # Get relationships between these nodes
            edges_result = session.run("""
                MATCH (a:Knowledge)-[r]->(b:Knowledge)
                WHERE a.id IN $node_ids AND b.id IN $node_ids
                RETURN a.id as source, b.id as target, type(r) as type, properties(r) as properties
            """, node_ids=[n['id'] for n in nodes])
            
            edges = []
            for record in edges_result:
                edges.append({
                    'source': record['source'],
                    'target': record['target'],
                    'type': record['type'],
                    'properties': dict(record['properties'])
                })
            
            return {
                'nodes': nodes,
                'edges': edges
            }
    
    def update_validation_status(self, node_id: int, validations: int, is_validated: bool):
        """
        Update validation status of a knowledge node
        
        Args:
            node_id: Node identifier
            validations: Number of validations
            is_validated: Validation status
        """
        with self.driver.session() as session:
            session.run("""
                MATCH (k:Knowledge {id: $id})
                SET k.validations = $validations,
                    k.is_validated = $is_validated
            """, id=node_id, validations=validations, is_validated=is_validated)
    
    def create_user(self, address: str, username: str = None) -> Dict:
        """
        Create or update a user node
        
        Args:
            address: Blockchain address
            username: Optional username
        
        Returns:
            User data
        """
        with self.driver.session() as session:
            result = session.run("""
                MERGE (u:User {address: $address})
                ON CREATE SET u.username = $username, u.reputation = 0, u.created_at = timestamp()
                ON MATCH SET u.username = COALESCE($username, u.username)
                RETURN u
            """, address=address, username=username)
            
            record = result.single()
            return dict(record['u'])
    
    def get_user_contributions(self, address: str) -> List[Dict]:
        """
        Get all contributions by a user
        
        Args:
            address: User's blockchain address
        
        Returns:
            List of contributed knowledge nodes
        """
        with self.driver.session() as session:
            result = session.run("""
                MATCH (k:Knowledge {contributor: $address})
                RETURN k
                ORDER BY k.timestamp DESC
            """, address=address)
            
            contributions = []
            for record in result:
                node = dict(record['k'])
                if 'embedding' in node:
                    node['embedding'] = json.loads(node['embedding'])
                contributions.append(node)
            
            return contributions
    
    def get_statistics(self) -> Dict:
        """
        Get database statistics
        
        Returns:
            Statistics dictionary
        """
        with self.driver.session() as session:
            # Count nodes
            node_count = session.run("MATCH (k:Knowledge) RETURN count(k) as count").single()['count']
            
            # Count relationships
            rel_count = session.run("MATCH ()-[r]->() RETURN count(r) as count").single()['count']
            
            # Count users
            user_count = session.run("MATCH (u:User) RETURN count(u) as count").single()['count']
            
            # Count validated nodes
            validated_count = session.run("""
                MATCH (k:Knowledge {is_validated: true}) 
                RETURN count(k) as count
            """).single()['count']
            
            return {
                'total_nodes': node_count,
                'total_relationships': rel_count,
                'total_users': user_count,
                'validated_nodes': validated_count
            }
