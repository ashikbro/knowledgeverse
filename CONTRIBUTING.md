# Contributing to KnowledgeVerse

First off, thank you for considering contributing to KnowledgeVerse! It's people like you that make KnowledgeVerse such a great tool for decentralized knowledge sharing.

## Code of Conduct

This project and everyone participating in it is governed by our commitment to creating a welcoming and inclusive environment. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title** for the issue
* **Describe the exact steps which reproduce the problem**
* **Provide specific examples to demonstrate the steps**
* **Describe the behavior you observed after following the steps**
* **Explain which behavior you expected to see instead and why**
* **Include screenshots and animated GIFs** if relevant
* **Include your environment details** (OS, browser, versions)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title**
* **Provide a step-by-step description of the suggested enhancement**
* **Provide specific examples to demonstrate the steps**
* **Describe the current behavior** and **explain which behavior you expected to see instead**
* **Explain why this enhancement would be useful**

### Pull Requests

* Fill in the required template
* Do not include issue numbers in the PR title
* Follow the Python and JavaScript style guides
* Include thoughtfully-worded, well-structured tests
* Document new code based on the Documentation Style Guide
* End all files with a newline

## Development Process

### Setting Up Your Development Environment

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
```bash
git clone https://github.com/your-username/knowledgeverse.git
cd knowledgeverse
```

3. **Create a branch** for your changes:
```bash
git checkout -b feature/your-feature-name
```

4. **Install dependencies**:
```bash
# Backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
cd ..
```

5. **Set up environment variables**:
```bash
cp .env.example .env
# Edit .env with your configuration
```

### Development Workflow

1. **Make your changes** in your feature branch
2. **Test your changes** thoroughly:
```bash
# Backend tests
pytest tests/

# Frontend tests
cd frontend && npm test
```

3. **Lint your code**:
```bash
# Backend (if you have pylint installed)
pylint backend/

# Frontend
cd frontend && npm run lint
```

4. **Commit your changes**:
```bash
git add .
git commit -m "Description of your changes"
```

5. **Push to your fork**:
```bash
git push origin feature/your-feature-name
```

6. **Create a Pull Request** on GitHub

### Commit Message Guidelines

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line

Examples:
```
Add semantic search functionality

- Implement sentence embeddings
- Add similarity scoring
- Update search API endpoint

Fixes #123
```

## Style Guides

### Python Style Guide

* Follow PEP 8
* Use 4 spaces for indentation
* Use docstrings for all public functions, classes, and modules
* Maximum line length: 100 characters
* Use type hints where appropriate

Example:
```python
def process_query(query: str) -> Dict[str, Any]:
    """
    Process natural language query.
    
    Args:
        query: User's natural language query
    
    Returns:
        Processed query information including intent and entities
    """
    # Implementation here
    pass
```

### JavaScript/React Style Guide

* Use 2 spaces for indentation
* Use functional components with hooks
* Use meaningful variable names
* Add PropTypes or TypeScript types
* Follow Airbnb React/JSX Style Guide

Example:
```javascript
const QueryInterface = ({ onSearch }) => {
  const [query, setQuery] = useState('');
  
  const handleSearch = async () => {
    // Implementation here
  };
  
  return (
    <Box>
      {/* Component JSX */}
    </Box>
  );
};
```

### Git Commit Messages

* Use the present tense
* Keep the first line under 50 characters
* Add a blank line before the body
* Wrap the body at 72 characters
* Use the body to explain what and why vs. how

## Testing Guidelines

### Backend Tests

* Write unit tests for all new functions
* Use pytest for testing
* Mock external dependencies
* Aim for >80% code coverage

Example:
```python
def test_blockchain_submission():
    """Test knowledge submission to blockchain"""
    bc = MockBlockchainManager()
    result = bc.submit_knowledge("test_hash")
    
    assert result['node_id'] is not None
    assert result['status'] == 1
```

### Frontend Tests

* Write component tests using React Testing Library
* Test user interactions
* Mock API calls
* Test error states

Example:
```javascript
test('submits knowledge on form submission', async () => {
  render(<ContributionForm />);
  
  fireEvent.change(screen.getByLabelText('Title'), {
    target: { value: 'Test Knowledge' }
  });
  
  fireEvent.click(screen.getByText('Submit'));
  
  await waitFor(() => {
    expect(screen.getByText(/submitted successfully/i)).toBeInTheDocument();
  });
});
```

## Documentation Guidelines

* Use clear and concise language
* Include code examples where relevant
* Keep documentation up-to-date with code changes
* Use proper Markdown formatting
* Include diagrams for complex concepts

## Specific Contribution Areas

### Adding New AI Models

1. Place model code in `backend/ai/`
2. Implement a consistent interface
3. Add model documentation
4. Include training instructions
5. Provide example usage

### Adding New Smart Contracts

1. Write contract in `contracts/`
2. Add comprehensive tests
3. Include deployment scripts
4. Document all functions
5. Perform security audit

### Adding New Frontend Components

1. Create component in `frontend/src/components/`
2. Use Material-UI for consistency
3. Make it responsive
4. Add PropTypes/TypeScript
5. Include component documentation

### Improving Documentation

1. Check for outdated information
2. Add missing examples
3. Improve clarity
4. Fix typos and grammar
5. Add diagrams or screenshots

## Community

### Getting Help

* **GitHub Issues**: For bugs and feature requests
* **GitHub Discussions**: For questions and general discussion
* **Discord** (if available): For real-time chat

### Recognition

Contributors are recognized in several ways:

* Listed in CONTRIBUTORS.md
* Mentioned in release notes
* Showcased in project README
* Given credit in documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

Don't hesitate to ask questions! You can:

* Open an issue with your question
* Start a discussion on GitHub Discussions
* Reach out to maintainers directly

Thank you for contributing to KnowledgeVerse! 🚀
