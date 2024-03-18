from pydantic import BaseModel


class ImageData(BaseModel):
    """
    Схема для изображений
    """
    id: int
    original: str
    negative: str
