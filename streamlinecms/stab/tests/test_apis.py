from pytest import fixture, mark


class TestStabGetItems:
    @fixture
    def target(self):
        return "/"

    def test_response_ok(self, target, client):
        from fastapi import status

        res = client.get(
            target,
        )

        assert res.status_code == status.HTTP_200_OK

    @mark.parametrize(
        "name, description",
        [
            ("", "name is not set"),
            ("streamline", "name is set"),
        ],
    )
    def test_data_ok(self, target, client, name, description):
        res = client.get(
            target,
            params={
                "name": name,
            },
        )

        actual = res.json()
        expected = {
            "name": name,
            "message": f"Hello, {name}!",
        }
        assert actual == expected, description
