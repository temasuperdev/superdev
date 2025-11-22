import os
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.database import database, metadata, engine


@pytest.fixture(autouse=True)
def prepare_db():
    # Create tables for tests (uses same dev.db file)
    metadata.create_all(engine)
    yield
    # Optionally remove dev.db after tests
    try:
        os.remove("./dev.db")
    except OSError:
        pass


@pytest.mark.asyncio
async def test_create_and_get_user():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await database.connect()
        response = await client.post("/users/", json={"name": "Alice", "email": "alice@example.com"})
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Alice"
        user_id = data["id"]

        resp = await client.get(f"/users/{user_id}")
        assert resp.status_code == 200
        assert resp.json()["email"] == "alice@example.com"
        await database.disconnect()
