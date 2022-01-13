from enum import Enum

from pydantic import BaseModel, Field


class PieceType(str, Enum):
    paragraph = "paragraph"
    title = "title"


class TextPiece(BaseModel):
    document_id: str = Field(..., example="1")
    text: str = Field(..., example="It`s a text piece.")
    piece_type: PieceType = Field(..., example=PieceType.title)
    page_number: int = Field(..., example=5)
    document_name: str = Field(..., example="The first doc")
