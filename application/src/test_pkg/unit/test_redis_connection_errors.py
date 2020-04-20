import pytest
import redis
from src.config import redis_conn

@pytest.fixture()
def redis_connection_params():
    return dict(redis_conn)

def redis_reconnect(redis_connection_params):
    red_cnx = redis_connection_params
    r = redis.Redis(red_cnx)
    r2 = redis.Redis(red_cnx)

    clients = r2.execute_command('')


def test_wrong_host(redis_connection_params):
    """Pass the wrong host name to the redis connection object"""

    redis_connection_params['host'] = 'wrong_host'
    with pytest.raises(redis.ConnectionError) as exception_info:
        r = redis.Redis(**redis_connection_params)
        r.get(1)

    err = exception_info.value
    print("\n\n" + err.args[0])

    assert "Error 11001 connecting to wrong_host:6379. getaddrinfo failed." in err.args[0]


def test_wrong_port(redis_connection_params):
    """Pass the wrong port number to the redis connection object"""

    redis_connection_params['port'] = 6377
    with pytest.raises(redis.TimeoutError) as exception_info:
        r = redis.Redis(**redis_connection_params)
        r.get(1)

    err = exception_info.value
    print("\n\n" + err.args[0])

    assert 'Timeout connecting to server' in err.args[0]