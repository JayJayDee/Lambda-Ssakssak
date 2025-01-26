from lib.lambda_version_gatherer import LambdaVersionGatherer
import lib.aws_factory as aws_factory

if __name__ == '__main__':
    client = aws_factory.lambda_('ap-northeast-2')
    all_lambda_versions = LambdaVersionGatherer(client=client).gather(num_threads=5)
    print(list(map(lambda x : x.str(), all_lambda_versions)))