async def test_ping(api_client):
    response = await api_client.get("/api/v1/ping")
    assert response.status == 200

    body = await response.json()
    assert body["message"] == "Pong!"


async def test_ping_db(api_client):
    response = await api_client.get("/api/v1/ping_db")
    assert response.status == 200

    body = await response.json()
    assert body["message"] == "Pong db!"
