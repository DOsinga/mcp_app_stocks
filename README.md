# MCP Stock Tracker

A Model Context Protocol (MCP) server that provides real-time stock price tracking with an interactive dashboard.

## Installation

### Goose

[![Install in Goose](https://block.github.io/goose/img/extension-install-dark.svg)](https://block.github.io/goose/extension?cmd=uvx&arg=mcp-stock-tracker&id=mcp-stock-tracker&name=MCP%20Stock%20Tracker&description=Real-time%20stock%20price%20tracking%20with%20an%20interactive%20dashboard&env=ALPHA_VANTAGE_API_KEY)

Or install manually: Go to `Advanced settings` -> `Extensions` -> `Add custom extension`. Name to your liking, use type `STDIO`, and set the `command` to `uvx mcp-stock-tracker`. Click "Add Extension".

### Other MCP Clients (Claude Desktop, etc.)

Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "stock-tracker": {
      "command": "uvx",
      "args": ["mcp-stock-tracker"],
      "env": {
        "ALPHA_VANTAGE_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

## Getting an API Key

This server requires an Alpha Vantage API key to fetch stock data.

1. Visit <https://www.alphavantage.co/support/#api-key>
2. Sign up for a free API key (25 requests/day)
3. Premium tiers with higher limits available at <https://www.alphavantage.co/premium/>

## Features

- Real-time stock quotes via Alpha Vantage API
- Interactive web dashboard for tracking multiple stocks
- Auto-refresh every 30 seconds
- Visual price change indicators (green/red)
- Track price, volume, and daily high/low

## Tools

| Tool | Description |
|------|-------------|
| `get_stock_quote` | Fetch real-time stock data for a symbol |

## Resources

| Resource | Description |
|----------|-------------|
| `ui://stock-tracker/dashboard` | Interactive dashboard UI |

## Development

```bash
git clone https://github.com/DOsinga/mcp_app_stocks.git
cd mcp_app_stocks
pip install -e ".[dev]"
```

## License

MIT License
