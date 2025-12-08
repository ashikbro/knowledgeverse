"""
NLP module for processing and understanding knowledge queries
"""
from transformers import AutoTokenizer, AutoModel, pipeline
from sentence_transformers import SentenceTransformer
import torch
import numpy as np
from typing import List, Dict, Tuple
import re


class NLPProcessor:
    """
    Natural Language Processing for AI-powered queries
    """
    
    def __init__(self, device='cpu'):
        self.device = torch.device(device if torch.cuda.is_available() else 'cpu')
        
        # Load sentence embedding model
        print("Loading NLP models...")
        self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.sentence_model.to(self.device)
        
        # Load question-answering model
        self.qa_pipeline = pipeline(
            "question-answering",
            model="distilbert-base-cased-distilled-squad",
            device=0 if torch.cuda.is_available() else -1
        )
        
        # Load NER model for entity extraction
        self.ner_pipeline = pipeline(
            "ner",
            model="dslim/bert-base-NER",
            device=0 if torch.cuda.is_available() else -1,
            aggregation_strategy="simple"
        )
        
        print("NLP models loaded successfully")
    
    def encode_text(self, texts: List[str]) -> np.ndarray:
        """
        Convert text to embeddings
        
        Args:
            texts: List of text strings
        
        Returns:
            Embeddings as numpy array
        """
        embeddings = self.sentence_model.encode(texts, convert_to_numpy=True)
        return embeddings
    
    def process_query(self, query: str) -> Dict:
        """
        Process natural language query
        
        Args:
            query: User's natural language query
        
        Returns:
            Processed query information
        """
        # Extract entities
        entities = self.extract_entities(query)
        
        # Identify query intent
        intent = self.identify_intent(query)
        
        # Generate query embedding
        embedding = self.encode_text([query])[0]
        
        # Extract keywords
        keywords = self.extract_keywords(query)
        
        return {
            'original_query': query,
            'intent': intent,
            'entities': entities,
            'keywords': keywords,
            'embedding': embedding.tolist(),
            'processed_query': self.preprocess_query(query)
        }
    
    def extract_entities(self, text: str) -> List[Dict]:
        """
        Extract named entities from text
        
        Args:
            text: Input text
        
        Returns:
            List of entities with types and confidence scores
        """
        try:
            entities = self.ner_pipeline(text)
            
            processed_entities = []
            for entity in entities:
                processed_entities.append({
                    'text': entity['word'],
                    'type': entity['entity_group'],
                    'score': float(entity['score']),
                    'start': entity['start'],
                    'end': entity['end']
                })
            
            return processed_entities
        except Exception as e:
            print(f"Entity extraction error: {e}")
            return []
    
    def identify_intent(self, query: str) -> str:
        """
        Identify the intent of the query
        
        Args:
            query: User query
        
        Returns:
            Query intent category
        """
        query_lower = query.lower()
        
        # Define intent patterns
        intents = {
            'search': ['find', 'search', 'look for', 'show me', 'what is', 'who is'],
            'relationship': ['how', 'relate', 'connection', 'link', 'relationship'],
            'explanation': ['why', 'explain', 'reason', 'because'],
            'comparison': ['compare', 'difference', 'similar', 'versus', 'vs'],
            'aggregate': ['count', 'how many', 'total', 'sum', 'average'],
            'recommendation': ['suggest', 'recommend', 'should', 'best']
        }
        
        for intent_type, patterns in intents.items():
            if any(pattern in query_lower for pattern in patterns):
                return intent_type
        
        return 'general'
    
    def extract_keywords(self, text: str) -> List[str]:
        """
        Extract important keywords from text
        
        Args:
            text: Input text
        
        Returns:
            List of keywords
        """
        # Simple keyword extraction (can be enhanced with TF-IDF or RAKE)
        # Remove common stop words
        stop_words = {'the', 'is', 'at', 'which', 'on', 'a', 'an', 'and', 'or', 
                     'but', 'in', 'with', 'to', 'for', 'of', 'as', 'by', 'this',
                     'that', 'it', 'from', 'be', 'are', 'was', 'were', 'been'}
        
        # Tokenize and filter
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        keywords = [word for word in words if word not in stop_words]
        
        # Return unique keywords
        return list(set(keywords))
    
    def preprocess_query(self, query: str) -> str:
        """
        Clean and preprocess query text
        
        Args:
            query: Raw query text
        
        Returns:
            Preprocessed query
        """
        # Remove extra whitespace
        query = ' '.join(query.split())
        
        # Remove special characters except basic punctuation
        query = re.sub(r'[^\w\s\?\.\!\,\-]', '', query)
        
        return query.strip()
    
    def semantic_search(self, query: str, knowledge_texts: List[str], top_k: int = 5) -> List[Dict]:
        """
        Perform semantic search over knowledge base
        
        Args:
            query: Search query
            knowledge_texts: List of knowledge texts to search
            top_k: Number of top results to return
        
        Returns:
            Ranked search results
        """
        if not knowledge_texts:
            return []
        
        # Encode query and knowledge texts
        query_embedding = self.encode_text([query])[0]
        text_embeddings = self.encode_text(knowledge_texts)
        
        # Calculate cosine similarities
        similarities = self._cosine_similarity(query_embedding, text_embeddings)
        
        # Get top-k results
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            results.append({
                'index': int(idx),
                'text': knowledge_texts[idx],
                'similarity': float(similarities[idx])
            })
        
        return results
    
    def answer_question(self, question: str, context: str) -> Dict:
        """
        Answer a question based on context
        
        Args:
            question: Question to answer
            context: Context containing the answer
        
        Returns:
            Answer with confidence score
        """
        try:
            result = self.qa_pipeline(question=question, context=context)
            return {
                'answer': result['answer'],
                'confidence': float(result['score']),
                'start': result['start'],
                'end': result['end']
            }
        except Exception as e:
            print(f"QA error: {e}")
            return {
                'answer': 'Unable to answer',
                'confidence': 0.0,
                'start': 0,
                'end': 0
            }
    
    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> np.ndarray:
        """
        Calculate cosine similarity between vectors
        
        Args:
            vec1: First vector or matrix
            vec2: Second vector or matrix
        
        Returns:
            Cosine similarity scores
        """
        if len(vec2.shape) == 1:
            vec2 = vec2.reshape(1, -1)
        
        dot_product = np.dot(vec2, vec1)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2, axis=1)
        
        return dot_product / (norm1 * norm2 + 1e-8)
    
    def generate_query_expansion(self, query: str) -> List[str]:
        """
        Generate alternative query formulations
        
        Args:
            query: Original query
        
        Returns:
            List of expanded queries
        """
        expansions = [query]
        
        # Simple expansion strategies
        # Add synonyms or related terms (this is a simplified version)
        keywords = self.extract_keywords(query)
        
        # Add queries with different keyword combinations
        if len(keywords) > 1:
            # Create queries with subsets of keywords
            for i in range(len(keywords)):
                subset = keywords[:i] + keywords[i+1:]
                expansions.append(' '.join(subset))
        
        return expansions[:5]  # Limit to 5 expansions
