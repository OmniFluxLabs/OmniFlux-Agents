import pytest
from unittest.mock import Mock, patch
from memory import RedisMemory


@pytest.fixture
def mock_redis_client():
    """Create a mock Redis client."""
    client = Mock()
    client.ping.return_value = True
    client.set.return_value = True
    client.setex.return_value = True
    client.get.return_value = '{"test": "data"}'
    client.delete.return_value = 1
    client.exists.return_value = 1
    client.rpush.return_value = 1
    client.lrange.return_value = ['{"item": 1}', '{"item": 2}']
    client.flushdb.return_value = True
    return client


@patch('memory.redis.Redis')
def test_redis_memory_init(mock_redis_class, mock_redis_client):
    """Test RedisMemory initialization."""
    mock_redis_class.return_value = mock_redis_client
    
    memory = RedisMemory(host="localhost", port=6379)
    
    assert memory.host == "localhost"
    assert memory.port == 6379
    assert memory.client is not None
    mock_redis_client.ping.assert_called_once()


@patch('memory.redis.Redis')
def test_redis_memory_set(mock_redis_class, mock_redis_client):
    """Test setting a value in Redis."""
    mock_redis_class.return_value = mock_redis_client
    
    memory = RedisMemory()
    result = memory.set("test_key", {"data": "value"})
    
    assert result is True
    mock_redis_client.set.assert_called_once()


@patch('memory.redis.Redis')
def test_redis_memory_get(mock_redis_class, mock_redis_client):
    """Test getting a value from Redis."""
    mock_redis_class.return_value = mock_redis_client
    
    memory = RedisMemory()
    result = memory.get("test_key")
    
    assert result == {"test": "data"}
    mock_redis_client.get.assert_called_once_with("test_key")


@patch('memory.redis.Redis')
def test_redis_memory_delete(mock_redis_class, mock_redis_client):
    """Test deleting a key from Redis."""
    mock_redis_class.return_value = mock_redis_client
    
    memory = RedisMemory()
    result = memory.delete("test_key")
    
    assert result is True
    mock_redis_client.delete.assert_called_once_with("test_key")


@patch('memory.redis.Redis')
def test_redis_memory_exists(mock_redis_class, mock_redis_client):
    """Test checking if a key exists."""
    mock_redis_class.return_value = mock_redis_client
    
    memory = RedisMemory()
    result = memory.exists("test_key")
    
    assert result is True
    mock_redis_client.exists.assert_called_once_with("test_key")


@patch('memory.redis.Redis')
def test_redis_memory_list_operations(mock_redis_class, mock_redis_client):
    """Test list operations in Redis."""
    mock_redis_class.return_value = mock_redis_client
    
    memory = RedisMemory()
    
    # Test append_to_list
    result = memory.append_to_list("test_list", {"item": "value"})
    assert result == 1
    mock_redis_client.rpush.assert_called_once()
    
    # Test get_list
    result = memory.get_list("test_list")
    assert len(result) == 2
    assert result[0] == {"item": 1}
    mock_redis_client.lrange.assert_called_once_with("test_list", 0, -1)


@patch('memory.redis.Redis')
def test_redis_memory_connection_error(mock_redis_class):
    """Test handling of connection errors."""
    mock_client = Mock()
    mock_client.ping.side_effect = Exception("Connection failed")
    mock_redis_class.return_value = mock_client
    
    with pytest.raises(ConnectionError):
        RedisMemory()


@patch('memory.redis.Redis')
def test_redis_memory_set_with_ttl(mock_redis_class, mock_redis_client):
    """Test setting a value with TTL."""
    mock_redis_class.return_value = mock_redis_client
    
    memory = RedisMemory()
    result = memory.set("test_key", {"data": "value"}, ttl=60)
    
    assert result is True
    mock_redis_client.setex.assert_called_once()
