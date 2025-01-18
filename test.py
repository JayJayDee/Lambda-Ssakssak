from lib.lambda_mapper import LambdaMapper
from lib.lambda_version_mapper import LambdaVersionMapper
import lib.aws_factory as aws_factory

if __name__ == '__main__':
    client = aws_factory.lambda_('ap-northeast-2')
    lambdas = LambdaMapper.fetch_all(client)
    lambda_ = lambdas.pop(-1)
    versions = LambdaVersionMapper.from_lambda(lambda_, client)

    print(list(map(lambda x : x.str(), lambdas)))
    print(list(map(lambda x : x.str(), versions)))