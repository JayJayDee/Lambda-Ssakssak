import boto3
from mypy_boto3_lambda import LambdaClient
from mypy_boto3_apigateway import APIGatewayClient

def lambda_(region: str | None) -> LambdaClient:
    if region: 
        return boto3.client('lambda', region_name = region)  
    return boto3.client('lambda')

def apigw(region: str | None) -> APIGatewayClient:
    if region: 
        return boto3.client('apigateway', region_name = region)  
    return boto3.client('apigateway')
