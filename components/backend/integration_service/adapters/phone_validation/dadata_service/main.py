import aiohttp

from integration_service.application import interfaces
from . import errors, schemas


class DadataPhoneValidator(interfaces.PhoneValidator):
    def __init__(self, api_url: str, api_key: str, secret_key: str) -> None:
        self.api_key = api_key
        self.secret_key = secret_key
        self.api_url = api_url

    @property
    def headers(self) -> dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Token {self.api_key}",
            "X-Secret": self.secret_key
        }

    async def validate(self, phone: str) -> schemas.PhoneResponse:
        async with aiohttp.ClientSession() as session:
            async with session.post(self.api_url, json=[phone], headers=self.headers) as response:

                response_data = await response.json()
                match response.status:
                    case 200:
                        return schemas.PhoneResponse(**response_data[0])
                    case 400:
                        raise errors.IncorrectRequest(server_response=response_data)
                    case 401:
                        raise errors.IncorrectCredentials(server_response=response_data)
                    case 403:
                        raise errors.InsufficientFunds(server_response=response_data)
                    case 405:
                        raise errors.IncorrectRequestMethod(server_response=response_data)
                    case 429:
                        raise errors.TooManyRequests(server_response=response_data)
                    case _ if 500 <= response.status < 600:
                        raise errors.InternalServiceError(server_response=response_data)
                    case _:
                        raise errors.UnknownError(server_response=response_data)
