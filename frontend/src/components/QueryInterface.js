import React, { useState } from 'react';
import {
  Paper,
  Typography,
  TextField,
  Button,
  Box,
  CircularProgress,
  Card,
  CardContent,
  Chip,
  Divider
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import api from '../services/api';

const QueryInterface = () => {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState([]);
  const [queryInfo, setQueryInfo] = useState(null);

  const handleSearch = async () => {
    if (!query.trim()) return;

    try {
      setLoading(true);
      const response = await api.post('/search', { query });
      
      setResults(response.data.results || []);
      setQueryInfo(response.data.query_info || null);
      setLoading(false);
    } catch (error) {
      console.error('Search error:', error);
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  return (
    <Paper elevation={3} sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>
        AI-Powered Knowledge Query
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Ask questions in natural language. Our AI will understand and search the knowledge graph.
      </Typography>

      <Box sx={{ display: 'flex', gap: 2, mb: 3 }}>
        <TextField
          fullWidth
          variant="outlined"
          placeholder="e.g., What is machine learning? How is AI related to neural networks?"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyPress={handleKeyPress}
        />
        <Button
          variant="contained"
          size="large"
          startIcon={loading ? <CircularProgress size={20} /> : <SearchIcon />}
          onClick={handleSearch}
          disabled={loading || !query.trim()}
          sx={{ minWidth: 120 }}
        >
          Search
        </Button>
      </Box>

      {queryInfo && (
        <Box sx={{ mb: 3 }}>
          <Typography variant="subtitle2" gutterBottom>
            Query Analysis:
          </Typography>
          <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
            <Chip label={`Intent: ${queryInfo.intent}`} size="small" color="primary" />
            {queryInfo.entities && queryInfo.entities.map((entity, idx) => (
              <Chip
                key={idx}
                label={`${entity.type}: ${entity.text}`}
                size="small"
                variant="outlined"
              />
            ))}
          </Box>
        </Box>
      )}

      <Divider sx={{ my: 2 }} />

      {loading && (
        <Box display="flex" justifyContent="center" p={4}>
          <CircularProgress />
        </Box>
      )}

      {!loading && results.length > 0 && (
        <Box>
          <Typography variant="h6" gutterBottom>
            Found {results.length} results:
          </Typography>
          {results.map((result, index) => (
            <Card key={index} sx={{ mb: 2 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  {result.title || `Knowledge Node ${result.id}`}
                </Typography>
                <Typography variant="body2" color="text.secondary" paragraph>
                  {result.content || 'No content available'}
                </Typography>
                <Box sx={{ display: 'flex', gap: 1, alignItems: 'center' }}>
                  <Chip
                    label={result.category || 'general'}
                    size="small"
                    color="primary"
                    variant="outlined"
                  />
                  {result.similarity && (
                    <Chip
                      label={`Relevance: ${(result.similarity * 100).toFixed(1)}%`}
                      size="small"
                      color="success"
                    />
                  )}
                  {result.is_validated && (
                    <Chip label="✓ Validated" size="small" color="success" />
                  )}
                  <Chip
                    label={`${result.validations || 0} validations`}
                    size="small"
                  />
                </Box>
              </CardContent>
            </Card>
          ))}
        </Box>
      )}

      {!loading && results.length === 0 && query && (
        <Box textAlign="center" p={4}>
          <Typography color="text.secondary">
            No results found. Try a different query.
          </Typography>
        </Box>
      )}
    </Paper>
  );
};

export default QueryInterface;
