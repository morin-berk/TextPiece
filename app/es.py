import os
from typing import List, Union

from dotenv import find_dotenv, load_dotenv
from elasticsearch import Elasticsearch

load_dotenv(find_dotenv())

INDEX_NAME = "fastapi_project"
ES_HOST = os.environ.get("ES_HOST")
ES_PORT = os.environ.get("ES_PORT")

es = Elasticsearch(host=ES_HOST, port=ES_PORT)

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
    es.index(index=INDEX_NAME, body=data, id=data["document_id"])


def get_all_text_pieces() -> Union[List[dict], str]:
    """Returns all TextPieces from the storage."""
    results = es.search(index=INDEX_NAME, body={"query": {"match_all": {}}})
    return [doc["_source"] for doc in results["hits"]["hits"]]


def get_filtered_text_pieces(query: dict) -> Union[List[dict], str]:
    """Returns TextPieces that matches the search criteria,
    given in the query param. If nothing matches, returns an empty list."""
    query_body = {"query": {"bool": {}}}

    for key, value in query.items():
        if key == "text":
            query_body["query"]["bool"].update(
                {
                    "must": {
                        "match": {key: {"query": value, "fuzziness": "auto"}}
                    }
                }
            )
        else:
            query_body["query"]["bool"].setdefault("filter", [])
            query_body["query"]["bool"]["filter"].append(
                {"term": {key: value}}
            )

    results = es.search(index=INDEX_NAME, body=query_body)
    return [doc["_source"] for doc in results["hits"]["hits"]]
