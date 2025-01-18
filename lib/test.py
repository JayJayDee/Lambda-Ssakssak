from mypy_boto3_lambda import LambdaClient
from lambda_version import LambdaVersion
import aws_factory

def fetch_all_lambda_versions(client: LambdaClient):
    next_marker: str | None = None
    fetched_all_versions: list[LambdaVersion] = []

    while next_marker is None:
        response = client.list_functions(
            **({'Marker': next_marker} if next_marker is not None else {})
        )
        next_marker = response['NextMarker']
        raw_functions = response['Functions']
        versions = list(map(lambda x : LambdaVersion.from_boto3_response(x), raw_functions))
        fetched_all_versions.extend(versions)

    return fetched_all_versions

if __name__ == '__main__':
    client = aws_factory.lambda_('ap-northeast-2')
    all_lambda_versions = fetch_all_lambda_versions(client)

    print(list(map(lambda x : x.str(), all_lambda_versions)))
