from typing import Any

from qdrant_client import models


def generate_must_clauses(filter_conditions: dict[str, Any]) -> list[models.FieldCondition]:
    
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
            ) for k, v in filter_conditions.items()
        ]
        
    return []