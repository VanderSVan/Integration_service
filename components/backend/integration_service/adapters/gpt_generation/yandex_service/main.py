import aiohttp

from integration_service.application import interfaces
from . import errors, schemas


class YandexGPTGenerator(interfaces.GPTGenerator):
    def __init__(self,
                 api_url: str,
                 api_key: str,
                 folder_id: str,
                 promt: str = "Найди ошибки в тексте и исправь их",
                 max_tokens: int = 2000,
                 temperature: float = 0.6,
                 model_uri: str = "gpt://{}/yandexgpt-lite"
                 ) -> None:
        self.api_url = api_url
        self.api_key = api_key
        self.folder_id = folder_id
        self.promt = promt
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.model_uri = model_uri.format(folder_id)

    @property
    def headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}"
        }

    async def generate(self, message: str) -> schemas.YandexGPTResponse:
        request_data = schemas.YandexGPTRequest(
            modelUri=self.model_uri,
            completionOptions=schemas.CompletionOptions(
                stream=False,
                temperature=self.temperature,
                maxTokens=str(self.max_tokens)
            ),
            messages=[
                schemas.Message(role="system", text=self.promt),
                schemas.Message(role="user", text=message)
            ]
        )

        async with aiohttp.ClientSession() as session:
            async with session.post(self.api_url,
                                    json=request_data.dict(),
                                    headers=self.headers
                                    ) as response:
                response_data = await response.json()
                match response.status:
                    case 200:
                        return schemas.YandexGPTResponse(**response_data)
                    case 400:
                        raise errors.IncorrectRequest(server_response=response_data)
                    case 401:
                        raise errors.AuthenticationError(server_response=response_data)
                    case 403:
                        raise errors.PermissionDenied(server_response=response_data)
                    case 429:
                        raise errors.QuotaExceeded(server_response=response_data)
                    case 500:
                        raise errors.InternalServiceError(server_response=response_data)
                    case 501:
                        raise errors.UnImplemented(server_response=response_data)
                    case 503:
                        raise errors.ServiceUnavailable(server_response=response_data)
                    case 504:
                        raise errors.RequestTimeout(server_response=response_data)
                    case _:
                        raise errors.UnknownError(server_response=response_data)
