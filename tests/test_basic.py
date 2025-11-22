import os
import importlib
import pytest
from httpx import AsyncClient, ASGITransport


@pytest.mark.asyncio
async def test_create_and_get_user(tmp_path):
    # Use a temporary sqlite file for isolation
    db_file = tmp_path / "test.db"
    os.environ["DATABASE_URL"] = f"sqlite:///{db_file}"

    # Reload app.database so it picks up the env var
    import app.database as database_module

    importlib.reload(database_module)
    # Reload main so it uses the updated database module
    import app.main as main_module

    importlib.reload(main_module)

    app = main_module.app
    database = database_module.database

    # Connect first, then ensure tables exist on the same database file
    await database.connect()
    database_module.metadata.create_all(database_module.engine)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/users/", json={"name": "Alice", "email": "alice@example.com"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Alice"
        user_id = data["id"]

        resp = await client.get(f"/users/{user_id}")
        assert resp.status_code == 200
        assert resp.json()["email"] == "alice@example.com"
        await database.disconnect()
