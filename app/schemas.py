from pydantic import BaseModel, Field


class TextPiece(BaseModel):
    document_id: str = Field(..., example="1")
    text: str = Field(..., example="It`s a text piece.")
    piece_type: str = Field(..., example="Paragraph/Title")
    page_number: int = Field(..., example=5)
    document_name: str = Field(..., example="The first doc")
