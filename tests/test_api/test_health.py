async def test_ping(api_client):
    response = await api_client.get("/api/v1/ping")
    assert response.status == 200

    body = await response.json()
    assert body["message"] == "Pong!"
