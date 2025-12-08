import React, { useState, useEffect } from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Container,
  Box,
  Tab,
  Tabs,
  ThemeProvider,
  createTheme,
  CssBaseline
} from '@mui/material';
import GraphVisualization from './components/GraphVisualization';
import QueryInterface from './components/QueryInterface';
import Dashboard from './components/Dashboard';
import ContributionForm from './components/ContributionForm';
import api from './services/api';
import './styles/App.css';

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#00bcd4',
    },
    secondary: {
      main: '#ff4081',
    },
    background: {
      default: '#0a1929',
      paper: '#1a2332',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h4: {
      fontWeight: 700,
    },
  },
});

function TabPanel({ children, value, index }) {
  return (
    <div hidden={value !== index} style={{ paddingTop: '20px' }}>
      {value === index && <Box>{children}</Box>}
    </div>
  );
}

function App() {
  const [tabValue, setTabValue] = useState(0);
  const [stats, setStats] = useState({});
  const [userInfo, setUserInfo] = useState(null);

  useEffect(() => {
    loadStats();
    checkConnection();
  }, []);

  const loadStats = async () => {
    try {
      const response = await api.get('/stats');
      setStats(response.data);
    } catch (error) {
      console.error('Error loading stats:', error);
    }
  };

  const checkConnection = async () => {
    try {
      const response = await api.get('/health');
      console.log('Backend status:', response.data);
    } catch (error) {
      console.error('Backend connection error:', error);
    }
  };

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ flexGrow: 1, minHeight: '100vh' }}>
        <AppBar position="static" elevation={0}>
          <Toolbar>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1, fontWeight: 700 }}>
              🧠 KnowledgeVerse
            </Typography>
            <Typography variant="body2" sx={{ mr: 2 }}>
              Decentralized Knowledge Graph
            </Typography>
          </Toolbar>
        </AppBar>

        <Container maxWidth="xl" sx={{ mt: 2 }}>
          <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
            <Tabs value={tabValue} onChange={handleTabChange} centered>
              <Tab label="Graph Visualization" />
              <Tab label="AI Query" />
              <Tab label="Contribute" />
              <Tab label="Dashboard" />
            </Tabs>
          </Box>

          <TabPanel value={tabValue} index={0}>
            <GraphVisualization />
          </TabPanel>

          <TabPanel value={tabValue} index={1}>
            <QueryInterface />
          </TabPanel>

          <TabPanel value={tabValue} index={2}>
            <ContributionForm onSuccess={loadStats} />
          </TabPanel>

          <TabPanel value={tabValue} index={3}>
            <Dashboard stats={stats} />
          </TabPanel>
        </Container>
      </Box>
    </ThemeProvider>
  );
}

export default App;
