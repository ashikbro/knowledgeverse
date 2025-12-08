"""
Graph Neural Network (GNN) module for knowledge reasoning
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GCNConv, GATConv, global_mean_pool
from torch_geometric.data import Data, Batch
import numpy as np


class KnowledgeGNN(nn.Module):
    """
    Graph Neural Network for reasoning over knowledge graphs
    Uses Graph Attention Networks (GAT) for better relationship understanding
    """
    
    def __init__(self, input_dim=768, hidden_dim=256, output_dim=128, num_heads=4, num_layers=3):
        super(KnowledgeGNN, self).__init__()
        
        self.num_layers = num_layers
        self.convs = nn.ModuleList()
        self.batch_norms = nn.ModuleList()
        
        # First layer
        self.convs.append(GATConv(input_dim, hidden_dim, heads=num_heads, concat=True))
        self.batch_norms.append(nn.BatchNorm1d(hidden_dim * num_heads))
        
        # Hidden layers
        for _ in range(num_layers - 2):
            self.convs.append(GATConv(hidden_dim * num_heads, hidden_dim, heads=num_heads, concat=True))
            self.batch_norms.append(nn.BatchNorm1d(hidden_dim * num_heads))
        
        # Output layer
        self.convs.append(GATConv(hidden_dim * num_heads, output_dim, heads=1, concat=False))
        
        # Prediction heads
        self.link_predictor = nn.Sequential(
            nn.Linear(output_dim * 2, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(hidden_dim, 1),
            nn.Sigmoid()
        )
        
        self.node_classifier = nn.Sequential(
            nn.Linear(output_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(hidden_dim, 10)  # 10 knowledge categories
        )
    
    def forward(self, x, edge_index, batch=None):
        """
        Forward pass through the GNN
        
        Args:
            x: Node features [num_nodes, input_dim]
            edge_index: Graph connectivity [2, num_edges]
            batch: Batch vector for graph-level tasks
        
        Returns:
            node_embeddings: Learned node representations
        """
        # Apply GAT layers
        for i in range(self.num_layers - 1):
            x = self.convs[i](x, edge_index)
            x = self.batch_norms[i](x)
            x = F.relu(x)
            x = F.dropout(x, p=0.3, training=self.training)
        
        # Final layer without activation
        x = self.convs[-1](x, edge_index)
        
        return x
    
    def predict_link(self, z, edge_index):
        """
        Predict link probability between nodes
        
        Args:
            z: Node embeddings
            edge_index: Edges to predict
        
        Returns:
            Link probabilities
        """
        src, dst = edge_index
        node_pairs = torch.cat([z[src], z[dst]], dim=-1)
        return self.link_predictor(node_pairs)
    
    def classify_node(self, z):
        """
        Classify node into knowledge categories
        
        Args:
            z: Node embeddings
        
        Returns:
            Category logits
        """
        return self.node_classifier(z)


class ReasoningEngine:
    """
    AI-powered reasoning engine using GNN
    """
    
    def __init__(self, model_path=None, device='cpu'):
        self.device = torch.device(device if torch.cuda.is_available() else 'cpu')
        self.model = KnowledgeGNN().to(self.device)
        
        if model_path:
            self.load_model(model_path)
        
        self.model.eval()
    
    def load_model(self, path):
        """Load pre-trained model"""
        checkpoint = torch.load(path, map_location=self.device)
        self.model.load_state_dict(checkpoint['model_state_dict'])
    
    def save_model(self, path):
        """Save model checkpoint"""
        torch.save({
            'model_state_dict': self.model.state_dict(),
        }, path)
    
    def train_step(self, data, optimizer, criterion):
        """Single training step"""
        self.model.train()
        optimizer.zero_grad()
        
        # Forward pass
        z = self.model(data.x, data.edge_index)
        
        # Compute loss (example: link prediction)
        if hasattr(data, 'edge_label_index'):
            pred = self.model.predict_link(z, data.edge_label_index)
            loss = criterion(pred.squeeze(), data.edge_label.float())
        else:
            # Node classification
            pred = self.model.classify_node(z)
            loss = criterion(pred, data.y)
        
        # Backward pass
        loss.backward()
        optimizer.step()
        
        return loss.item()
    
    def infer_relationships(self, graph_data, node_embeddings):
        """
        Infer potential relationships between knowledge nodes
        
        Args:
            graph_data: PyTorch Geometric Data object
            node_embeddings: Pre-computed node embeddings
        
        Returns:
            Predicted relationships with confidence scores
        """
        self.model.eval()
        
        with torch.no_grad():
            # Get embeddings
            z = self.model(node_embeddings, graph_data.edge_index)
            
            # Generate all possible pairs
            num_nodes = z.size(0)
            all_pairs = []
            for i in range(num_nodes):
                for j in range(i + 1, num_nodes):
                    all_pairs.append([i, j])
            
            if len(all_pairs) == 0:
                return []
            
            edge_index = torch.tensor(all_pairs, dtype=torch.long).t().to(self.device)
            
            # Predict links
            link_probs = self.model.predict_link(z, edge_index)
            
            # Filter by threshold
            threshold = 0.7
            predictions = []
            for idx, prob in enumerate(link_probs):
                if prob.item() > threshold:
                    src, dst = all_pairs[idx]
                    predictions.append({
                        'source': int(src),
                        'target': int(dst),
                        'confidence': float(prob.item())
                    })
            
            return predictions
    
    def get_node_embeddings(self, graph_data):
        """
        Get learned embeddings for all nodes
        
        Args:
            graph_data: PyTorch Geometric Data object
        
        Returns:
            Node embeddings as numpy array
        """
        self.model.eval()
        
        with torch.no_grad():
            z = self.model(graph_data.x, graph_data.edge_index)
            return z.cpu().numpy()
    
    def explain_prediction(self, graph_data, source_node, target_node):
        """
        Provide explainable AI for relationship predictions
        
        Args:
            graph_data: PyTorch Geometric Data object
            source_node: Source node index
            target_node: Target node index
        
        Returns:
            Explanation dictionary with attention weights and reasoning paths
        """
        self.model.eval()
        
        with torch.no_grad():
            # Get embeddings
            z = self.model(graph_data.x, graph_data.edge_index)
            
            # Get prediction
            edge_index = torch.tensor([[source_node], [target_node]], dtype=torch.long).to(self.device)
            prob = self.model.predict_link(z, edge_index).item()
            
            # Get attention weights from GAT layers
            attention_weights = []
            x = graph_data.x
            
            for conv in self.model.convs[:-1]:
                x, (edge_idx, attn) = conv(x, graph_data.edge_index, return_attention_weights=True)
                attention_weights.append(attn.cpu().numpy())
            
            explanation = {
                'prediction_confidence': prob,
                'source_embedding': z[source_node].cpu().numpy().tolist(),
                'target_embedding': z[target_node].cpu().numpy().tolist(),
                'attention_weights': [w.tolist() for w in attention_weights],
                'reasoning': self._generate_reasoning_text(prob, source_node, target_node)
            }
            
            return explanation
    
    def _generate_reasoning_text(self, confidence, source, target):
        """Generate human-readable reasoning explanation"""
        if confidence > 0.8:
            strength = "strong"
        elif confidence > 0.6:
            strength = "moderate"
        else:
            strength = "weak"
        
        return f"The model predicts a {strength} relationship (confidence: {confidence:.2%}) " \
               f"between node {source} and node {target} based on learned graph patterns " \
               f"and semantic similarities in the knowledge graph."
