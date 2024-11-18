from pydantic import BaseModel, Field


class Message(BaseModel):
    role: str = Field(..., description="Роль отправителя сообщения, например 'assistant'")
    text: str = Field(..., description="Текстовое содержимое сообщения")


class _Alternative(BaseModel):
    message: Message = Field(description="Сообщение, содержащее роль и текст")
    status: str = Field(description="Статус ответа, например 'ALTERNATIVE_STATUS_TRUNCATED_FINAL'")


class _Usage(BaseModel):
    inputTextTokens: str = Field(description="Количество токенов в входном тексте")
    completionTokens: str = Field(description="Количество токенов в сгенерированном тексте")
    totalTokens: str = Field(description="Общее количество токенов")


class _Result(BaseModel):
    alternatives: list[_Alternative] = Field(description="Список альтернативных ответов")
    usage: _Usage = Field(description="Информация о количестве использованных токенов")
    modelVersion: str = Field(description="Версия модели")


class CompletionOptions(BaseModel):
    stream: bool = Field(description="Включает потоковую передачу частично сгенерированного текста")
    temperature: float = Field(description="Креативность и случайность ответов модели, от 0 до 1")
    maxTokens: str = Field(description="Максимальное количество токенов для генерации")


class YandexGPTRequest(BaseModel):
    modelUri: str = Field(description="Идентификатор модели для генерации ответа")
    completionOptions: CompletionOptions = Field(description="Опции конфигурации генерации текста")
    messages: list[Message] = Field(description="Список сообщений, задающих контекст для модели")


class YandexGPTResponse(BaseModel):
    result: _Result
