import React from 'react';
import {
  Paper,
  Typography,
  Box,
  Grid,
  Card,
  CardContent
} from '@mui/material';
import AccountBalanceIcon from '@mui/icons-material/AccountBalance';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import PeopleIcon from '@mui/icons-material/People';
import GraphicEqIcon from '@mui/icons-material/GraphicEq';

const Dashboard = ({ stats }) => {
  const statCards = [
    {
      title: 'Total Knowledge Nodes',
      value: stats.total_nodes || 0,
      icon: <GraphicEqIcon sx={{ fontSize: 40 }} />,
      color: '#2196f3'
    },
    {
      title: 'Validated Nodes',
      value: stats.validated_nodes || 0,
      icon: <CheckCircleIcon sx={{ fontSize: 40 }} />,
      color: '#4caf50'
    },
    {
      title: 'Total Relationships',
      value: stats.total_relationships || 0,
      icon: <AccountBalanceIcon sx={{ fontSize: 40 }} />,
      color: '#ff9800'
    },
    {
      title: 'Community Members',
      value: stats.total_users || 0,
      icon: <PeopleIcon sx={{ fontSize: 40 }} />,
      color: '#9c27b0'
    }
  ];

  return (
    <Box>
      <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
        <Typography variant="h5" gutterBottom>
          System Dashboard
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Overview of the decentralized knowledge graph network
        </Typography>
      </Paper>

      <Grid container spacing={3}>
        {statCards.map((card, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <Card sx={{ 
              height: '100%',
              background: `linear-gradient(135deg, ${card.color}22 0%, ${card.color}11 100%)`
            }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Box sx={{ color: card.color, mr: 2 }}>
                    {card.icon}
                  </Box>
                </Box>
                <Typography variant="h4" gutterBottom sx={{ fontWeight: 700 }}>
                  {card.value.toLocaleString()}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {card.title}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Paper elevation={3} sx={{ p: 3, mt: 3 }}>
        <Typography variant="h6" gutterBottom>
          About KnowledgeVerse
        </Typography>
        <Typography variant="body2" paragraph>
          KnowledgeVerse is a decentralized knowledge graph platform that combines blockchain 
          technology, artificial intelligence, and graph databases to create an innovative 
          crowdsourced network for knowledge sharing and validation.
        </Typography>
        
        <Typography variant="subtitle1" gutterBottom sx={{ mt: 2 }}>
          Key Features:
        </Typography>
        <Box component="ul" sx={{ pl: 2 }}>
          <Typography component="li" variant="body2" sx={{ mb: 1 }}>
            <strong>Blockchain-based Validation:</strong> Knowledge contributions are validated 
            through a decentralized consensus mechanism with tokenized rewards.
          </Typography>
          <Typography component="li" variant="body2" sx={{ mb: 1 }}>
            <strong>AI-Powered Queries:</strong> Natural Language Processing (NLP) enables 
            intuitive knowledge discovery through conversational queries.
          </Typography>
          <Typography component="li" variant="body2" sx={{ mb: 1 }}>
            <strong>Graph Neural Networks:</strong> Advanced GNN models perform reasoning and 
            infer relationships between knowledge nodes.
          </Typography>
          <Typography component="li" variant="body2" sx={{ mb: 1 }}>
            <strong>Real-time Visualization:</strong> Interactive graph visualization shows 
            the structure and connections in the knowledge network.
          </Typography>
          <Typography component="li" variant="body2" sx={{ mb: 1 }}>
            <strong>Explainable AI:</strong> Transparent reasoning process helps users 
            understand how relationships are inferred.
          </Typography>
          <Typography component="li" variant="body2">
            <strong>Token Economy:</strong> Contributors earn tokens for validated knowledge, 
            creating a sustainable ecosystem for intellectual growth.
          </Typography>
        </Box>
      </Paper>
    </Box>
  );
};

export default Dashboard;
