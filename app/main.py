from typing import Optional

from fastapi import Body, FastAPI, Query, HTTPException
from fastapi.encoders import jsonable_encoder

from app.es import get_all_text_pieces, get_filtered_text_pieces, index_text_piece
from app.schemas import TextPiece

app = FastAPI()


# text_piece_db = [
#     {
#         "piece_id": 1,
#         "text": "Some random text",
#         "piece_type": "paragraph",
#         "page_number": 3,
#         "document_name": "First_Doc",
#     },
#     {
#         "piece_id": 2,
#         "text": "Random Title",
#         "piece_type": "title",
#         "page_number": 1,
#         "document_name": "First_Doc",
#     },
#     {
#         "piece_id": 3,
#         "text": "Another Random Title",
#         "piece_type": "title",
#         "page_number": 1,
#         "document_name": "Second_Doc",
#     },
# ]


@app.post(
    "/pieces/",
    summary="Adding a text piece into an elasticsearch index",
    response_description="The item is indexed",
)
def index_piece(piece: TextPiece = Body(...)):
    """
    Takes a TextPiece object and saves it
    to an elasticsearch index.
    """
    json_piece = jsonable_encoder(piece)
    index_text_piece(json_piece)
    return json_piece


@app.get(
    "/pieces/",
    summary="Searching among indexed text pieces.",
    response_description="Text pieces, matching the search criteria.",
)
def read_pieces(
    text: Optional[str] = Query(
        None, example="Random text piece...", description="Find similar text pieces"
    ),
    piece_type: Optional[str] = Query(
        None, example="title", description='Either "title" or "paragraph"'
    ),
    page_number: Optional[int] = Query(None, example=10),
    document_name: Optional[str] = Query(None, example="Random Doc"),
):
    """
    Allows to get the list of already indexed pieces,
    also provides filtering options.
    """
    query = dict()
    for param_key, param_value in zip(
        ("text", "piece_type", "page_number", "document_name"),
        (text, piece_type, page_number, document_name),
    ):
        if param_value:
            query[param_key] = param_value

    if not query:
        all_text_pieces = get_all_text_pieces()
        if all_text_pieces == "Nonexistent index":
            raise HTTPException(status_code=404,
                                detail="The index doesn`t exist yet.")
        else:
            return all_text_pieces
    else:
        filtered_text_pieces = get_filtered_text_pieces(query)
        if filtered_text_pieces == "Nonexistent index":
            raise HTTPException(status_code=404,
                                detail="The index doesn`t exist yet.")
        else:
            return filtered_text_pieces
