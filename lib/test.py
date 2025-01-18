import boto3
import aws_factory

if __name__ == '__main__':
    client = aws_factory.lambda_('ap-northeast-2')
    response = client.list_functions()
