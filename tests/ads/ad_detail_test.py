import pytest

from ads.serializers import AdDetailSerializer


@pytest.mark.django_db
def test_detail_ad(client, ad, user):

    response = client.get(f"/ad/{ad.pk}/")

    assert response.status_code == 200
    assert response.data == AdDetailSerializer(ad).data
