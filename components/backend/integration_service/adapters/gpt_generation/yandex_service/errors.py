from integration_service.application import errors


class IncorrectRequest(errors.Error):
    message_template = ('Некорректный запрос. Проверьте формат запроса. '
                        'Возможно, указан неправильный URI модели, превышена длина промта, '
                        'задано недопустимое значение параметра или нарушены этические '
                        'ограничения.')
    context = {'server_response': dict}


class RequestTimeout(errors.Error):
    message_template = ('Превышен срок выполнения запроса. '
                        'Проблемы в сети между клиентом и сервером. Попробуйте отправить запрос '
                        'повторно.')
    context = {'server_response': dict}


class PermissionDenied(errors.Error):
    message_template = ('Недостаточно прав для выполнения операции. '
                        'Проверьте наличие необходимых ролей у сервисного аккаунта или доступ к '
                        'модели.')
    context = {'server_response': dict}


class QuotaExceeded(errors.Error):
    message_template = ('Превышена квота запросов. '
                        'Подождите или обратитесь в техническую поддержку для увеличения квоты.')
    context = {'server_response': dict}


class UnImplemented(errors.Error):
    message_template = ('Проблема на стороне сервиса YandexGPT. '
                        'Обратитесь в техническую поддержку.')
    context = {'server_response': dict}


class InternalServiceError(errors.Error):
    message_template = ('Внутренняя ошибка сервиса YandexGPT. '
                        'Обратитесь в техническую поддержку.')
    context = {'server_response': dict}


class ServiceUnavailable(errors.Error):
    message_template = ('Сервис YandexGPT временно недоступен. '
                        'Попробуйте отправить запрос повторно позже.')
    context = {'server_response': dict}


class AuthenticationError(errors.Error):
    message_template = ('Ошибка авторизации. Проверьте IAM-токен или API-ключ, '
                        'а также срок их действия.')
    context = {'server_response': dict}


class UnknownError(errors.Error):
    message_template = ('Неизвестная ошибка. '
                        'Попробуйте позже или обратитесь в техническую поддержку.')
    context = {'server_response': dict}
