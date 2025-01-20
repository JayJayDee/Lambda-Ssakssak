from typing import TypedDict, Literal
from typing_extensions import Unpack
from mypy_boto3_lambda import type_defs, LambdaClient
from lib.lambda_mapper import LambdaMapper
import lib.arn_validators as arn_validators

LambdaVersionStatus = Literal['uninspected', 'has_deps', 'has_no_deps']

class Constructor(TypedDict):
    version_arn: str
    version: str
    status: LambdaVersionStatus

class LambdaVersionMapper:

    def __init__(self, **kargs: Unpack[Constructor]):
        self._version_arn = kargs['version_arn']
        self._version = kargs['version']
        self._status = kargs['status']
        arn_validators.ensure_valid_version_arn(self._version_arn)

    def str(self):
        return f'LambaVersionMapper({self._version_arn})'
    
    def is_latest_version(self):
        if self._version == '$LATEST':
            return True
        return False
    
    def inspect_with_apigw(self):
        pass
    
    @classmethod
    def from_lambda(cls, lambda_mapper: LambdaMapper, client: LambdaClient):
        lambda_arn = lambda_mapper.lambda_arn
        next_marker: str | None = None
        all_versions: list[LambdaVersionMapper] = []

        while True:
            response = client.list_versions_by_function(**({
                'FunctionName': lambda_arn,
                'Marker': next_marker
            } if next_marker is not None else {
                'FunctionName': lambda_arn
            }))
            next_marker = response['NextMarker'] if 'NextMarker' in response else None
            raw_versions = response['Versions']
            versions = list(map(lambda x : LambdaVersionMapper.from_boto3_response(x), raw_versions))
            all_versions.extend(versions)

            if next_marker is None:
                break

        return all_versions

    @classmethod
    def from_boto3_response(cls, funcdef: type_defs.FunctionConfigurationTypeDef):
        """
        make LambdaVersion instances from boto3 response
        """
        version = LambdaVersionMapper(
            version_arn=funcdef['FunctionArn'],
            version=funcdef['Version'],
            status='uninspected'
        )
        return version
