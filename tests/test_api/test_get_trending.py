async def test_get_trendings(api_client, test_trendings):
    trending_date = test_trendings[0].create_datetime.date().isoformat()

    response = await api_client.get(f"/api/v1/trending/{trending_date}")
    assert response.status == 200

    body = await response.json()
    request_gifs = sorted(body["trendings"], key=lambda x: x["gif_id"])
    db_gifs = sorted(test_trendings, key=lambda x: str(x.gif_id))

    for request_gif, db_gif in zip(request_gifs, db_gifs):
        assert request_gif["gif_id"] == str(db_gif.gif_id)
        assert request_gif["title"] == db_gif.title
        assert request_gif["url"] == db_gif.url
