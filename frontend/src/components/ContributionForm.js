import React, { useState } from 'react';
import {
  Paper,
  Typography,
  TextField,
  Button,
  Box,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
  CircularProgress
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import api from '../services/api';

const ContributionForm = ({ onSuccess }) => {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [category, setCategory] = useState('general');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!title.trim() || !content.trim()) {
      setMessage({ type: 'error', text: 'Please fill in all fields' });
      return;
    }

    try {
      setLoading(true);
      setMessage(null);

      const response = await api.post('/knowledge', {
        title,
        content,
        category
      });

      setMessage({
        type: 'success',
        text: `Knowledge submitted successfully! Node ID: ${response.data.node_id}`
      });

      // Reset form
      setTitle('');
      setContent('');
      setCategory('general');

      if (onSuccess) {
        onSuccess();
      }

      setLoading(false);
    } catch (error) {
      console.error('Submission error:', error);
      setMessage({
        type: 'error',
        text: error.response?.data?.error || 'Failed to submit knowledge'
      });
      setLoading(false);
    }
  };

  return (
    <Paper elevation={3} sx={{ p: 3, maxWidth: 800, mx: 'auto' }}>
      <Typography variant="h5" gutterBottom>
        Contribute Knowledge
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Share your knowledge with the community. Validated contributions earn token rewards!
      </Typography>

      {message && (
        <Alert severity={message.type} sx={{ mb: 3 }} onClose={() => setMessage(null)}>
          {message.text}
        </Alert>
      )}

      <Box component="form" onSubmit={handleSubmit}>
        <TextField
          fullWidth
          label="Title"
          variant="outlined"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          margin="normal"
          required
        />

        <TextField
          fullWidth
          label="Content"
          variant="outlined"
          value={content}
          onChange={(e) => setContent(e.target.value)}
          margin="normal"
          multiline
          rows={6}
          required
          placeholder="Describe your knowledge contribution in detail..."
        />

        <FormControl fullWidth margin="normal">
          <InputLabel>Category</InputLabel>
          <Select
            value={category}
            label="Category"
            onChange={(e) => setCategory(e.target.value)}
          >
            <MenuItem value="general">General</MenuItem>
            <MenuItem value="science">Science</MenuItem>
            <MenuItem value="technology">Technology</MenuItem>
            <MenuItem value="mathematics">Mathematics</MenuItem>
            <MenuItem value="history">History</MenuItem>
            <MenuItem value="philosophy">Philosophy</MenuItem>
            <MenuItem value="arts">Arts</MenuItem>
          </Select>
        </FormControl>

        <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end' }}>
          <Button
            type="submit"
            variant="contained"
            size="large"
            startIcon={loading ? <CircularProgress size={20} /> : <SendIcon />}
            disabled={loading || !title.trim() || !content.trim()}
          >
            Submit Knowledge
          </Button>
        </Box>
      </Box>
    </Paper>
  );
};

export default ContributionForm;
