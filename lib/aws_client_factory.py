import boto3
from typing import Literal

ClientKind = Literal['lambda']

def aws_client(kind: ClientKind, region: str | None):
    if kind == 'lambda':
        if region: 
            return boto3.client('lambda', region = region)
        return boto3.client('lambda')
