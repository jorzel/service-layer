from setup import create_app


def test_up_endpoint():
    flask_app = create_app()

    with flask_app.test_client() as test_client:
        response = test_client.get("/")
        assert response.status_code == 200
        assert response.json == {"up": True}
