import React, { useState, useEffect, useRef } from 'react';
import { Paper, Typography, Box, CircularProgress } from '@mui/material';
import ForceGraph2D from 'react-force-graph-2d';
import api from '../services/api';

const GraphVisualization = () => {
  const [graphData, setGraphData] = useState({ nodes: [], links: [] });
  const [loading, setLoading] = useState(true);
  const graphRef = useRef();

  useEffect(() => {
    loadGraphData();
  }, []);

  const loadGraphData = async () => {
    try {
      setLoading(true);
      const response = await api.get('/graph?limit=50');
      
      // Transform data for react-force-graph
      const nodes = response.data.nodes.map(node => ({
        id: node.id,
        name: node.title || `Node ${node.id}`,
        val: node.validations || 1,
        category: node.category || 'general',
        validated: node.is_validated || false,
      }));

      const links = response.data.edges.map(edge => ({
        source: edge.source,
        target: edge.target,
        type: edge.type,
      }));

      setGraphData({ nodes, links });
      setLoading(false);
    } catch (error) {
      console.error('Error loading graph:', error);
      setLoading(false);
    }
  };

  const getNodeColor = (node) => {
    if (node.validated) return '#4caf50';
    
    const categoryColors = {
      science: '#2196f3',
      technology: '#9c27b0',
      history: '#ff9800',
      general: '#607d8b',
    };
    
    return categoryColors[node.category] || categoryColors.general;
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="500px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Paper elevation={3} sx={{ p: 2 }}>
      <Typography variant="h5" gutterBottom>
        Knowledge Graph Visualization
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
        Interactive graph showing {graphData.nodes.length} knowledge nodes and {graphData.links.length} relationships
      </Typography>
      
      <Box sx={{ border: '1px solid #333', borderRadius: 1, overflow: 'hidden' }}>
        <ForceGraph2D
          ref={graphRef}
          graphData={graphData}
          nodeLabel="name"
          nodeColor={getNodeColor}
          nodeRelSize={6}
          linkColor={() => 'rgba(255, 255, 255, 0.2)'}
          linkWidth={1}
          backgroundColor="#0a1929"
          width={1200}
          height={600}
          onNodeClick={(node) => {
            console.log('Node clicked:', node);
          }}
        />
      </Box>

      <Box sx={{ mt: 2, display: 'flex', gap: 2 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Box sx={{ width: 16, height: 16, borderRadius: '50%', bgcolor: '#4caf50' }} />
          <Typography variant="caption">Validated</Typography>
        </Box>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Box sx={{ width: 16, height: 16, borderRadius: '50%', bgcolor: '#2196f3' }} />
          <Typography variant="caption">Science</Typography>
        </Box>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Box sx={{ width: 16, height: 16, borderRadius: '50%', bgcolor: '#9c27b0' }} />
          <Typography variant="caption">Technology</Typography>
        </Box>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Box sx={{ width: 16, height: 16, borderRadius: '50%', bgcolor: '#ff9800' }} />
          <Typography variant="caption">History</Typography>
        </Box>
      </Box>
    </Paper>
  );
};

export default GraphVisualization;
