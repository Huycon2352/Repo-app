import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import app


def test_home():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200


@patch("app.Redis")
def test_vote(mock_redis_class):
    mock_redis = MagicMock()
    mock_redis_class.return_value = mock_redis

    client = app.test_client()

    response = client.post(
        "/",
        data={"vote": "Cats"}
    )

    assert response.status_code == 200

    mock_redis_class.assert_called_once()
    mock_redis.rpush.assert_called_once()
