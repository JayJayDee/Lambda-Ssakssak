import boto3
from mypy_boto3_lambda import LambdaClient

def lambda_(region: str | None) -> LambdaClient:
    if region: 
        return boto3.client('lambda', region_name = region)  
    return boto3.client('lambda')
