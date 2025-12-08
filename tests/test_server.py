"""Tests for the stock tracker server"""

import pytest
from stock_tracker.server import mcp, get_stock_quote


def test_mcp_instance():
    """Test that MCP instance is created"""
    assert mcp is not None
    assert mcp.name == "stock-tracker"


@pytest.mark.asyncio
async def test_get_stock_quote_structure():
    """Test that get_stock_quote returns expected structure"""
    # Note: This test uses the demo API key which has limited symbols
    try:
        result = await get_stock_quote("IBM")
        assert "symbol" in result
        assert "price" in result
        assert "change" in result
        assert "volume" in result
    except ValueError as e:
        # API limit reached is acceptable in tests
        if "API limit" not in str(e):
            raise


@pytest.mark.asyncio
async def test_get_stock_quote_invalid_symbol():
    """Test that invalid symbols raise appropriate errors"""
    with pytest.raises(ValueError):
        await get_stock_quote("INVALIDSYMBOL12345")
