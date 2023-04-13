import pytest


@pytest.mark.django_db
def test_create_selection(client, user, ad, user_token):
    response = client.post(
        "/selection/create/",
        {
            "id": 1,
            "name": "Подборка Миши",
            "owner": user.id,
            "items": [
                ad.id
            ]
        }, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + user_token)

    assert response.status_code == 201
    assert response.data == {
            "id": 1,
            "name": "Подборка Миши",
            "owner": user.id,
            "items": [
                ad.id
            ]
        }