"""
Stock Tracker MCP Server
Provides real-time stock price tracking with an interactive dashboard.
"""

import os
from mcp.server.fastmcp import FastMCP
import httpx
from datetime import datetime

# Initialize MCP server
mcp = FastMCP("stock-tracker")

# API Configuration
# Get API key from environment or use demo key
API_KEY = os.environ.get("ALPHA_VANTAGE_API_KEY", "demo")

# Dashboard HTML
STOCK_DASHBOARD_HTML = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Stock Tracker</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
        }
        .header {
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }
        .header h1 {
            font-size: 32px;
            font-weight: 600;
            margin-bottom: 10px;
        }
        .search-box {
            background: white;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .search-input {
            display: flex;
            gap: 10px;
        }
        input {
            flex: 1;
            padding: 12px 16px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.2s;
        }
        input:focus {
            outline: none;
            border-color: #667eea;
        }
        button {
            padding: 12px 24px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 500;
            cursor: pointer;
            transition: background 0.2s;
        }
        button:hover {
            background: #5568d3;
        }
        button:active {
            transform: scale(0.98);
        }
        .stocks-grid {
            display: grid;
            gap: 15px;
        }
        .stock-card {
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }
        .stock-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        }
        .stock-header {
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 15px;
        }
        .stock-symbol {
            font-size: 24px;
            font-weight: 700;
            color: #1a1a1a;
        }
        .stock-name {
            font-size: 14px;
            color: #666;
            margin-top: 4px;
        }
        .remove-btn {
            padding: 6px 12px;
            font-size: 14px;
            background: #ff3b30;
        }
        .remove-btn:hover {
            background: #ff6259;
        }
        .stock-price {
            font-size: 36px;
            font-weight: 700;
            color: #1a1a1a;
            margin-bottom: 8px;
        }
        .stock-change {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 600;
        }
        .positive {
            background: #e8f5e9;
            color: #2e7d32;
        }
        .negative {
            background: #ffebee;
            color: #c62828;
        }
        .stock-details {
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #e0e0e0;
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
            font-size: 14px;
        }
        .detail-item {
            color: #666;
        }
        .detail-value {
            color: #1a1a1a;
            font-weight: 600;
        }
        .loading {
            text-align: center;
            color: white;
            padding: 20px;
        }
        .error {
            background: #ffebee;
            color: #c62828;
            padding: 12px 16px;
            border-radius: 8px;
            margin-bottom: 15px;
        }
        .empty-state {
            text-align: center;
            color: white;
            padding: 40px 20px;
        }
        .empty-state h3 {
            font-size: 20px;
            margin-bottom: 10px;
        }
        .last-updated {
            text-align: center;
            color: rgba(255,255,255,0.8);
            font-size: 12px;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📈 Stock Tracker</h1>
            <p>Track your favorite stocks in real-time</p>
        </div>

        <div class="search-box">
            <div class="search-input">
                <input
                    type="text"
                    id="symbol-input"
                    placeholder="Enter stock symbol (e.g., AAPL, MSFT, GOOGL)"
                    onkeypress="if(event.key==='Enter') addStock()"
                >
                <button onclick="addStock()">Add Stock</button>
            </div>
        </div>

        <div id="error" class="error" style="display: none;"></div>
        <div id="loading" class="loading" style="display: none;">Loading...</div>
        <div id="stocks-container"></div>
        <div id="last-updated" class="last-updated"></div>
    </div>

    <script type="module">
        let watchlist = [];

        async function addStock() {
            const input = document.getElementById('symbol-input');
            const symbol = input.value.trim().toUpperCase();

            if (!symbol) return;

            if (watchlist.some(s => s.symbol === symbol)) {
                showError('Stock already in watchlist');
                return;
            }

            input.value = '';
            showLoading(true);
            hideError();

            try {
                if (window.mcp) {
                    const result = await window.mcp.callTool('get_stock_quote', { symbol });

                    if (result.structuredContent && result.structuredContent.symbol) {
                        watchlist.push(result.structuredContent);
                        renderWatchlist();
                    } else {
                        showError('Failed to fetch stock data');
                    }
                } else {
                    showError('MCP not available - run in Goose');
                }
            } catch (error) {
                showError(error.message || 'Failed to fetch stock');
            } finally {
                showLoading(false);
            }
        }

        async function removeStock(symbol) {
            watchlist = watchlist.filter(s => s.symbol !== symbol);
            renderWatchlist();
        }

        async function refreshAll() {
            if (!window.mcp || watchlist.length === 0) return;

            showLoading(true);

            for (let i = 0; i < watchlist.length; i++) {
                try {
                    const result = await window.mcp.callTool('get_stock_quote', {
                        symbol: watchlist[i].symbol
                    });
                    if (result.structuredContent) {
                        watchlist[i] = result.structuredContent;
                    }
                } catch (error) {
                    console.error('Failed to refresh', watchlist[i].symbol, error);
                }
            }

            renderWatchlist();
            showLoading(false);
        }

        function renderWatchlist() {
            const container = document.getElementById('stocks-container');

            if (watchlist.length === 0) {
                container.innerHTML = `
                    <div class="empty-state">
                        <h3>No stocks in watchlist</h3>
                        <p>Add a stock symbol above to get started</p>
                    </div>
                `;
                document.getElementById('last-updated').textContent = '';
                return;
            }

            container.innerHTML = `
                <div class="stocks-grid">
                    ${watchlist.map(stock => `
                        <div class="stock-card">
                            <div class="stock-header">
                                <div>
                                    <div class="stock-symbol">${stock.symbol}</div>
                                    <div class="stock-name">${stock.name || stock.symbol}</div>
                                </div>
                                <button class="remove-btn" onclick="removeStock('${stock.symbol}')">Remove</button>
                            </div>
                            <div class="stock-price">${stock.price.toFixed(2)}</div>
                            <span class="stock-change ${stock.change >= 0 ? 'positive' : 'negative'}">
                                ${stock.change >= 0 ? '▲' : '▼'}
                                ${Math.abs(stock.change).toFixed(2)}
                                (${stock.change_percent.toFixed(2)}%)
                            </span>
                            <div class="stock-details">
                                <div class="detail-item">
                                    Open: <span class="detail-value">${stock.open.toFixed(2)}</span>
                                </div>
                                <div class="detail-item">
                                    High: <span class="detail-value">${stock.high.toFixed(2)}</span>
                                </div>
                                <div class="detail-item">
                                    Low: <span class="detail-value">${stock.low.toFixed(2)}</span>
                                </div>
                                <div class="detail-item">
                                    Volume: <span class="detail-value">${(stock.volume / 1000000).toFixed(2)}M</span>
                                </div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            `;

            document.getElementById('last-updated').textContent =
                `Last updated: ${new Date().toLocaleTimeString()}`;
        }

        function showError(message) {
            const errorDiv = document.getElementById('error');
            errorDiv.textContent = message;
            errorDiv.style.display = 'block';
        }

        function hideError() {
            document.getElementById('error').style.display = 'none';
        }

        function showLoading(show) {
            document.getElementById('loading').style.display = show ? 'block' : 'none';
        }

        window.addStock = addStock;
        window.removeStock = removeStock;

        // Auto-refresh every 30 seconds
        setInterval(refreshAll, 30000);

        // Initial load with some demo stocks
        window.addEventListener('mcp-ready', async () => {
            const demoSymbols = ['AAPL', 'MSFT', 'GOOGL'];
            for (const symbol of demoSymbols) {
                try {
                    const result = await window.mcp.callTool('get_stock_quote', { symbol });
                    if (result.structuredContent) {
                        watchlist.push(result.structuredContent);
                    }
                } catch (e) {
                    console.log('Could not load demo stock', symbol);
                }
            }
            renderWatchlist();
        });
    </script>
</body>
</html>"""


@mcp.resource("ui://stock-tracker/dashboard")
def get_dashboard() -> str:
    """Stock tracking dashboard UI"""
    return STOCK_DASHBOARD_HTML


@mcp.tool()
async def get_stock_quote(symbol: str) -> dict:
    """
    Get real-time stock quote for a symbol

    Args:
        symbol: Stock ticker symbol (e.g., AAPL, MSFT, GOOGL)

    Returns:
        Dictionary containing stock quote data including price, change, volume, etc.
    """
    async with httpx.AsyncClient() as client:
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}"
        response = await client.get(url)
        data = response.json()

        if "Global Quote" not in data or not data["Global Quote"]:
            raise ValueError(f"Invalid symbol or API limit reached: {symbol}")

        quote = data["Global Quote"]

        return {
            "symbol": quote["01. symbol"],
            "name": quote["01. symbol"],  # Alpha Vantage doesn't include name in quote
            "price": float(quote["05. price"]),
            "change": float(quote["09. change"]),
            "change_percent": float(quote["10. change percent"].rstrip("%")),
            "open": float(quote["02. open"]),
            "high": float(quote["03. high"]),
            "low": float(quote["04. low"]),
            "volume": int(quote["06. volume"]),
            "latest_trading_day": quote["07. latest trading day"]
        }


def main():
    """Main entry point for the stock tracker server"""
    mcp.run()


if __name__ == "__main__":
    main()
