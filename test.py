from lib.lambda_version_gatherer import LambdaVersionGatherer
import lib.aws_factory as aws_factory

if __name__ == '__main__':
    client = aws_factory.lambda_('ap-northeast-2')
    gatherer = LambdaVersionGatherer(client=client).gather(num_threads=5)
