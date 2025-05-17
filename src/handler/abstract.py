from typing import Generic
from typing import TypeVar

TRequest  = TypeVar('TRequest')
TResponse = TypeVar('TResponse')

class RequestHandler(Generic[TRequest, TResponse]):
    def handle(self, request: TRequest) -> TResponse:
        raise NotImplementedError
    
