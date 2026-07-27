from tradiba.security.auth.api_keys import ApiKeyManager, ApiKeyScope

def test_api_key_lifecycle():
    manager = ApiKeyManager()
    
    result = manager.generate_api_key("u1", "TradingBot", [ApiKeyScope.MARKET_READ, ApiKeyScope.ORDERS_WRITE])
    key_id = result["key_id"]
    secret = result["secret"]
    
    # Valid usage
    assert manager.validate_api_key(key_id, secret, ApiKeyScope.MARKET_READ) is True
    
    # Invalid scope
    assert manager.validate_api_key(key_id, secret, ApiKeyScope.PORTFOLIO_READ) is False
    assert manager.validate_api_key(key_id, secret, ApiKeyScope.PORTFOLIO_READ) is False
    
    # Invalid secret
    assert manager.validate_api_key(key_id, "wrong_secret", ApiKeyScope.MARKET_READ) is False
