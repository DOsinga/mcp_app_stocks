# MCP Stock Tracker

A Model Context Protocol (MCP) server that provides real-time stock price tracking with an interactive dashboard.

## Features

- Real-time stock quotes using Alpha Vantage API
- Interactive web dashboard for tracking multiple stocks
- Auto-refresh every 30 seconds
- Beautiful, responsive UI with gradient design
- Track price changes, volume, and daily high/low
- Easy-to-use watchlist management

## Installation

### Install in Goose

[![Install in Goose](https://block.github.io/goose/img/extension-install-dark.svg)](https://block.github.io/goose/extension?cmd=uvx&arg=mcp-stock-tracker&id=mcp-stock-tracker&name=MCP%20Stock%20Tracker&description=Real-time%20stock%20price%20tracking%20with%20an%20interactive%20dashboard)

Or install manually: Go to `Advanced settings` -> `Extensions` -> `Add custom extension`. Name to your liking, use type `STDIO`, and set the `command` to `uvx mcp-stock-tracker`. Click "Add Extension".

### From PyPI

```bash
pip install mcp-stock-tracker
```

### From Source

```bash
git clone https://github.com/yourusername/mcp-stock-tracker.git
cd mcp-stock-tracker
pip install -e .
```

## Usage

### As a Standalone Script

You can run the server directly using `uvx`:

```bash
uvx stock_tracker.py
```

### As an Installed Package

After installation:

```bash
stock-tracker
```

### With Goose or Other MCP Clients

Configure your MCP client to use this server. The server provides:

- **Tool**: `get_stock_quote` - Fetch real-time stock data
- **Resource**: `ui://stock-tracker/dashboard` - Interactive dashboard UI

## Configuration

This server requires an Alpha Vantage API key to fetch stock data.

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ALPHA_VANTAGE_API_KEY` | **Yes** | Your Alpha Vantage API key |

### Getting an API Key

1. Visit <https://www.alphavantage.co/support/#api-key>
2. Sign up for a free API key
3. Set the environment variable before running the server

### Example Configuration

**Shell:**
```bash
export ALPHA_VANTAGE_API_KEY="your-api-key-here"
stock-tracker
```

**MCP Client Configuration (e.g., Claude Desktop, Goose):**
```json
{
  "mcpServers": {
    "stock-tracker": {
      "command": "stock-tracker",
      "env": {
        "ALPHA_VANTAGE_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

### Rate Limits

- **Free tier**: 25 requests/day
- **Premium tiers**: Higher limits available at <https://www.alphavantage.co/premium/>

## Dashboard Features

The interactive dashboard includes:

- **Add Stocks**: Enter any stock symbol to add to your watchlist
- **Live Updates**: Prices refresh automatically every 30 seconds
- **Price Changes**: Visual indicators showing gains (green) and losses (red)
- **Detailed Info**: View open, high, low, and volume data
- **Easy Management**: Remove stocks from your watchlist with one click

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/mcp-stock-tracker.git
cd mcp-stock-tracker

# Install with dev dependencies
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest
```

### Code Formatting

```bash
# Format code
black src/

# Lint code
ruff check src/
```

## Project Structure

```
mcp-stock-tracker/
├── src/
│   └── stock_tracker/
│       ├── __init__.py
│       └── server.py
├── tests/
├── pyproject.toml
├── README.md
├── LICENSE
└── .gitignore
```

## Requirements

- Python 3.10+
- mcp>=0.1.0
- httpx>=0.24.0

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter any issues or have questions:
- Open an issue on GitHub
- Check the documentation at https://github.com/yourusername/mcp-stock-tracker

## Acknowledgments

- Built with [FastMCP](https://github.com/jlowin/fastmcp)
- Stock data provided by [Alpha Vantage](https://www.alphavantage.co/)
