from .base import Error


class TargetNamesError(Error):
    message_template = 'The name of the publication queues is not specified.'
