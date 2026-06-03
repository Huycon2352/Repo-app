# import sys
# from pathlib import Path

# sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# from app import app


# def test_home():
#     client = app.test_client()
#     response = client.get("/")
#     assert response.status_code == 200

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import app


def test_home():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200


@patch("app.get_redis")
def test_vote(mock_get_redis):
    mock_redis = MagicMock()
    mock_get_redis.return_value = mock_redis

    client = app.test_client()

    response = client.post(
        "/",
        data={"vote": "Cats"}
    )

    assert response.status_code == 200

    mock_redis.rpush.assert_called_once()
