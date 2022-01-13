from typing import List, Optional

from elasticsearch import NotFoundError
from fastapi import FastAPI, Query, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.es import (get_all_text_pieces, get_filtered_text_pieces,
                    index_text_piece)
from app.schemas import TextPiece, NotFoundIndexSchema

TEXT_PIECE_PATH = "/pieces"

app = FastAPI()


@app.exception_handler(NotFoundError)
async def not_found_piece_exception_handler(
        request: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=404, content={"message": "The index doesn`t exist yet."}
    )


@app.post(
    TEXT_PIECE_PATH,
    summary="Adding a text piece into an elasticsearch index",
    response_description="The item is indexed",
    status_code=status.HTTP_201_CREATED,
    response_model=TextPiece,
)
def index_piece(piece: TextPiece):
    """Takes a TextPiece object and saves it
    to an elasticsearch index."""
    json_piece = jsonable_encoder(piece)
    return index_text_piece(json_piece)


@app.get(
    TEXT_PIECE_PATH,
    summary="Searching among indexed text pieces.",
    response_description="Text pieces, matching the search criteria.",
    status_code=status.HTTP_200_OK,
    response_model=List[TextPiece],
    responses={404: {"model": NotFoundIndexSchema}}
)
def read_pieces(
    text: Optional[str] = Query(
        None, example="Random text piece...",
        description="Find similar text pieces"
    ),
    piece_type: Optional[str] = Query(
        None, example="title", description='Either "title" or "paragraph"'
    ),
    page_number: Optional[int] = Query(None, example=10),
    document_name: Optional[str] = Query(None, example="Random Doc"),
):
    """Allows to get the list of already indexed pieces,
    also provides filtering options."""
    query = dict()
    for param_key, param_value in zip(
        ("text", "piece_type", "page_number", "document_name"),
        (text, piece_type, page_number, document_name),
    ):
        if param_value:
            query[param_key] = param_value

    if not query:
        return get_all_text_pieces()
    return get_filtered_text_pieces(query)
