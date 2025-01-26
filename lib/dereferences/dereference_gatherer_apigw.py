from typing import TypedDict
from typing_extensions import Unpack
from mypy_boto3_apigateway import APIGatewayClient

class Constructor(TypedDict):
    client: APIGatewayClient

class GatherParam(TypedDict):
    num_threads: int

class DereferenceGathererApiGw:

    def __init__(self, **kargs: Unpack[Constructor]):
        self._client = kargs['client']

    def gather(self, **kargs: Unpack[GatherParam]):
        num_threads = kargs['num_threads']
        num_threads # TODO: do something with num_threads
