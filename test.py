import lib.aws_factory as aws_factory
from lib.lambda_version_gatherer import LambdaVersionGatherer
from lib.lambda_version_mapper import LambdaVersionMapper

if __name__ == '__main__':
    client = aws_factory.lambda_('ap-northeast-2')
    # all_versions = LambdaVersionGatherer(client=client).gather(num_threads=5)
    # first_version = all_versions[0]

    function_qualifier = 'arn:aws:lambda:ap-northeast-2:693059789307:function:withbecon-Prod-webRTCPolicyApiHandler'

    func = client.get_function(
        FunctionName=function_qualifier,
        Qualifier='44'
    )
    func_config = func['Configuration']
    version = LambdaVersionMapper.from_boto3_response(func_config)
    print(version.str())