from typing import Any

from qdrant_client import QdrantClient, models


def generate_must_clauses(
    filter_conditions: dict[str, Any] | None
) -> list[models.FieldCondition]:
    """
    Generate a list of Qdrant FieldCondition objects based on filter conditions.

    Args:
        filter_conditions (dict[str, Any]): A dictionary containing filter conditions in the format: (attribute_name, value).

    Returns:
        list[models.FieldCondition]: A list of Qdrant FieldCondition objects based on the provided filter conditions.

    """

    # if it is not None or it is not an empty dict
    if filter_conditions:
        return [
            models.FieldCondition(
                key=k,
                match=models.MatchValue(value=v),
            )
            for k, v in filter_conditions.items()
        ]

    return []


def populate_db_test(
    qdrant_client: QdrantClient,
    collection_name: str,
    vectors: list[list[int]],
    payloads: list[dict[str, Any] | None] | None = None,
):
    points: list = []
    point_id = 0
    for p, v in zip(payloads or [None] * len(vectors), vectors):
        point = models.PointStruct(id=point_id, vector=list(map(float, v)))
        if p:
            point.payload = p
        points.append(point)
        point_id += 1
    qdrant_client.upsert(collection_name=collection_name, points=points)
