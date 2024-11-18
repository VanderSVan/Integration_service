from pydantic import BaseModel, Field


class EmailResponse(BaseModel):
    source: str = Field(..., max_length=100, description="Исходный email")
    email: str = Field(..., max_length=100, description="Стандартизованный email")
    local: str = Field(..., max_length=100,
                       description="Локальная часть адреса (то, что до «собачки»)")
    domain: str = Field(..., max_length=100, description="Домен (то, что после «собачки»)")
    type: str = Field(..., max_length=10, description="Тип адреса")
    qc: str = Field(..., max_length=5, description="Код проверки")
