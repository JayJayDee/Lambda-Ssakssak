from typing import TypedDict
from typing_extensions import Unpack
from mypy_boto3_apigateway import APIGatewayClient
from mypy_boto3_apigateway.type_defs import RestApiTypeDef

class Constructor(TypedDict):
    rest_api_id: str
    rest_api_name: str

class RestApiMapper:
    
    def __init__(self, **kargs: Unpack[Constructor]):
        self._rest_api_id = kargs['rest_api_id']
        self._rest_api_name = kargs['rest_api_name']

    def str(self):
        return f'RestApi({self._rest_api_name})'

    @classmethod
    def fetch_all(cls, client: APIGatewayClient):
        next_position: str | None = None
        all_restapis: list[cls] = []

        while True:
            response = client.get_rest_apis(limit=500)
            items = response['items']
            mappers = list(map(lambda x : cls.from_boto3_response(x), items))
            all_restapis.extend(mappers)

            if 'position' in response:
                next_position = response['position']
            if next_position is None:
                break

        return all_restapis

    @classmethod
    def from_boto3_response(cls, apidef: RestApiTypeDef):
        return cls(
            rest_api_id=apidef['id'],
            rest_api_name=apidef['name']
        )
