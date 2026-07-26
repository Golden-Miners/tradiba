from tradiba.frontend_api.charts import ChartDataService

def test_chart_data_service():
    service = ChartDataService()
    
    candles = service.get_candlesticks("BTC/USD", "1H")
    assert len(candles) > 0
    assert "close" in candles[0]
    
    overlays = service.get_ict_overlays("BTC/USD")
    assert "order_blocks" in overlays
    assert "fvg" in overlays
