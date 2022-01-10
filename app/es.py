from typing import List, Union

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError

INDEX_NAME = "fastapi_project"

es = Elasticsearch("http://localhost:9200")

mapping = {
    "properties": {
        "document_id": {"type": "integer"},
        "text": {"type": "text"},
        "piece_type": {"type": "text"},
        "page_number": {"type": "integer"},
        "document_name": {"type": "text"},
    }
}


def index_text_piece(data: dict) -> None:
    """Saves a TextPiece object to elasticsearch index."""
    es.index(index=INDEX_NAME, document=data, id=data["document_id"])


def get_all_text_pieces() -> Union[List[dict], str]:
    """Returns all TextPieces from the storage."""
    try:
        results = es.search(index=INDEX_NAME, query={"match_all": {}})
    except NotFoundError:
        return "Nonexistent index"
    else:
        return [doc["_source"] for doc in results["hits"]["hits"]]


def get_filtered_text_pieces(query: dict) -> Union[List[dict], str]:
    """Returns TextPieces that matches the search criteria,
    given in the query param. If nothing matches, returns an empty list."""
    query_body = {"bool": {"must": []}}
    for key, value in query.items():
        if key == "text":
            query_body["bool"]["must"].append(
                {"match": {key: {"query": value, "fuzziness": "auto"}}}
            )
        else:
            query_body["bool"]["must"].append({"match": {key: value}})
    try:
        results = es.search(index=INDEX_NAME, query=query_body)
    except NotFoundError:
        return "Nonexistent index"
    else:
        return [doc["_source"] for doc in results["hits"]["hits"]]
