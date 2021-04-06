import pytest

from pyle38.commands.nearby import Nearby

key = "fleet"
id = "truck"
feature = {
    "type": "Feature",
    "geometry": {"type": "Point", "coordinates": [13.37, 52.25]},
    "properties": {"id": id},
}

expected = {"id": id, "object": feature}


@pytest.mark.parametrize(
    "format, precision, expected",
    [
        (
            "OBJECTS",
            None,
            [
                "NEARBY",
                [
                    key,
                    "MATCH",
                    "*",
                    "NOFIELDS",
                    "SPARSE",
                    1,
                    "DISTANCE",
                    "CURSOR",
                    0,
                    "LIMIT",
                    10,
                    "FENCE",
                    "DETECT",
                    "enter,exit",
                    "COMMANDS",
                    "del,set",
                    "POINT",
                    1.0,
                    1.0,
                    100,
                ],
            ],
        )
    ],
    ids=["OBJECTS"],
)
@pytest.mark.asyncio
async def test_command_nearby_compile(tile38, format, precision, expected):
    query = (
        Nearby(tile38.client, key)
        .match("*")
        .nofields()
        .sparse(1)
        .distance()
        .cursor(0)
        .limit(10)
        .fence()
        .detect(["enter", "exit"])
        .commands(["del", "set"])
        .point(1, 1, 100)
    )

    received = query.output(format, precision).compile()

    assert expected == received


@pytest.mark.asyncio
async def test_command_nearby_point(tile38):
    response = await tile38.set(key, id).object(feature).exec()
    assert response.ok

    response = await tile38.nearby(key).point(52.250212, 13.370871).asObjects()
    assert response.ok
    assert response.objects[0].dict() == expected


@pytest.mark.asyncio
async def test_command_nearby_point_with_radius(tile38):
    response = await tile38.set(key, id).object(feature).exec()
    assert response.ok

    response = await tile38.nearby(key).point(52.250212, 13.370871, 10).asObjects()
    assert response.ok
    assert len(response.objects) == 0


@pytest.mark.asyncio
async def test_command_nearby_return_points(tile38):
    response = await tile38.set(key, id).object(feature).exec()
    assert response.ok

    response = await tile38.nearby(key).point(52.250212, 13.370871).asPoints()
    assert response.ok
    assert response.points[0].dict() == {
        "id": id,
        "point": {"lat": 52.25, "lon": 13.37},
    }


@pytest.mark.asyncio
async def test_command_nearby_return_ids(tile38):
    response = await tile38.set(key, id).object(feature).exec()
    assert response.ok

    response = await tile38.nearby(key).point(52.250212, 13.370871).asIds()
    assert response.ok
    assert response.ids == [id]


@pytest.mark.asyncio
async def test_command_nearby_return_count(tile38):
    response = await tile38.set(key, id).object(feature).exec()
    assert response.ok

    response = await tile38.nearby(key).point(52.250212, 13.370871).asCount()
    assert response.ok
    assert response.count == 1


@pytest.mark.asyncio
async def test_command_nearby_return_hashes(tile38):
    response = await tile38.set(key, id).object(feature).exec()
    assert response.ok

    response = await tile38.nearby(key).point(52.250212, 13.370871).asHashes(5)
    assert response.ok
    assert response.hashes[0].dict() == {"id": id, "hash": "u3390"}


@pytest.mark.asyncio
async def test_command_nearby_return_bounds(tile38):
    response = await tile38.set(key, id).object(feature).exec()
    assert response.ok

    response = await tile38.nearby(key).point(52.250212, 13.370871).asBounds()
    assert response.ok
    assert response.bounds[0].dict() == {
        "id": id,
        "bounds": {
            "ne": {"lat": 52.25, "lon": 13.37},
            "sw": {"lat": 52.25, "lon": 13.37},
        },
    }