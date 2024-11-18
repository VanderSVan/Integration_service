from pydantic import BaseModel, Field


class PhoneResponse(BaseModel):
    source: str = Field(max_length=100, description="Исходный телефон одной строкой")
    type: str | None = Field(max_length=50, description="Тип телефона")
    phone: str | None = Field(max_length=50, description="Стандартизованный телефон одной строкой")
    country_code: str | None = Field(max_length=5, description="Код страны")
    city_code: str | None = Field(max_length=5, description="Код города / DEF-код")
    number: str | None = Field(max_length=10, description="Локальный номер телефона")
    extension: str | None = Field(max_length=10, description="Добавочный номер")
    provider: str | None = Field(max_length=100, description="Оператор связи (только для России)")
    country: str | None = Field(max_length=50, description="Страна")
    region: str | None = Field(max_length=100, description="Регион (только для России)")
    city: str | None = Field(max_length=100,
                             description="Город (только для стационарных телефонов)")
    timezone: str | None = Field(max_length=50, description=(
        "Часовой пояс города для России, часовой пояс страны — для иностранных телефонов. "
        "Если у страны несколько поясов, вернёт минимальный и максимальный через слеш: UTC+5/UTC+6")
                                 )
    qc_conflict: str | None = Field(max_length=5,
                                    description="Признак конфликта телефона с адресом")
    qc: str | None = Field(max_length=5, description="Код проверки")
