from mypy_boto3_lambda import LambdaClient
from lib.lambda_version_mapper import LambdaVersionMapper
import aws_factory

def fetch_all_lambda_versions(client: LambdaClient):
    next_marker: str | None = None
    fetched_all_versions: list[LambdaVersionMapper] = []

    while next_marker is None:
        response = client.list_functions(
            **({'Marker': next_marker} if next_marker is not None else {})
        )
        next_marker = response['NextMarker']
        raw_functions = response['Functions']
        versions = list(map(lambda x : LambdaVersionMapper.from_boto3_response(x), raw_functions))
        fetched_all_versions.extend(versions)

    return fetched_all_versions

if __name__ == '__main__':
    client = aws_factory.lambda_('ap-northeast-2')
    all_lambda_versions = fetch_all_lambda_versions(client)

    lastest_filtered = filter(lambda x : not x.is_latest_version(), all_lambda_versions)
    stringified = map(lambda x : x.str(), lastest_filtered)
    print(list(stringified))
