from integration_service.application import errors


class IncorrectRequest(errors.Error):
    message_template = 'Некорректный запрос. Проверьте формат отправленных данных.'
    context = {'server_response': dict}


class IncorrectCredentials(errors.Error):
    message_template = 'Отсутствует API-ключ или секретный ключ, либо они неверны.'
    context = {'server_response': dict}


class InsufficientFunds(errors.Error):
    message_template = ('Не подтверждена почта. '
                        'Или недостаточно средств для обработки запроса, пополните баланс.')
    context = {'server_response': dict}


class IncorrectRequestMethod(errors.Error):
    message_template = 'Неправильный метод запроса. Используйте POST.'
    context = {'server_response': dict}


class TooManyRequests(errors.Error):
    message_template = 'Превышен лимит запросов. Попробуйте позже.'
    context = {'server_response': dict}


class InternalServiceError(errors.Error):
    message_template = 'Внутренняя ошибка сервиса `dadata.ru`. Попробуйте позже.'
    context = {'server_response': dict}


class UnknownError(errors.Error):
    message_template = 'Неизвестная ошибка. Попробуйте позже.'
    context = {'server_response': dict}
