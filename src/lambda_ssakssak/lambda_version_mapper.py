from datetime import datetime
from typing import TypedDict, Literal
from typing_extensions import Unpack
from mypy_boto3_lambda import type_defs, LambdaClient
from lambda_mapper import LambdaMapper
from dateutil import parser as date_parser
from lib import arn_validators

LambdaVersionStatus = Literal['uninspected', 'mark_tobe_deleted', 'mark_tobe_retained']

class DurationInvalidException(Exception):
    pass

class InvalidOperationException(Exception):
    pass

class Constructor(TypedDict):
    func_name: str
    version_arn: str
    version: str
    last_modified_at: datetime
    status: LambdaVersionStatus

class LambdaVersionMapper:

    def __init__(self, **kargs: Unpack[Constructor]):
        self.__func_name = kargs['func_name']
        self.__version_arn = kargs['version_arn']
        self.__version = kargs['version']
        self.__status = kargs['status']
        self.__last_modified_at = kargs['last_modified_at']
        arn_validators.ensure_valid_version_arn(self.__version_arn)

    def str(self):
        return f'LambaVersionMapper({self.__func_name}:{self.__version})'
    
    def is_latest_version(self):
        if self.__version == '$LATEST':
            return True
        return False
    
    def mark_as_retained(self):
        """
        Marks this lambda version for retain. this version will NOT be deleted
        """
        self.__status = 'mark_tobe_retained'

    def mark_as_deleted(self):
        """
        Marks this lambda version for DELETE. this version will be deleted!
        """
        if self.__status == 'mark_tobe_retained':
            raise InvalidOperationException(f'{self.str()} is already mark as retained. cannot be changed to deleted')
        self.__status = 'mark_tobe_deleted'

    def is_can_be_mark_as_deleted(self):
        if self.__status != 'mark_tobe_retained':
            return True
        return False

    def is_to_be_deleted(self):
        """
        Returns whether this lambda version is to be deleted (True) or to be retained (False)
        """
        if self.__status == 'mark_tobe_deleted':
            return True
        return False
    
    @property()
    def last_modified_at(self):
        return self.__last_modified_at
    
    def is_last_modified_in_duration(self, d_from: datetime, d_to: datetime):
        """
        returns LastModifiedAt of this lambda version is in between d_from, d_to
        @param d_from duration start
        @param d_to duration end
        """
        if d_from >= d_to:
            raise DurationInvalidException('d_from must be past than d_to')
        return d_from <= self.__last_modified_at <= d_to

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
            func_name=funcdef['FunctionName'],
            version_arn=funcdef['FunctionArn'],
            last_modified_at=date_parser.parse(funcdef['LastModified']),
            version=funcdef['Version'],
            status='uninspected'
        )
        return version
