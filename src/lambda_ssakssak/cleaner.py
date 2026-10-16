from typing import TypedDict
from typing_extensions import Unpack
from mypy_boto3_lambda import LambdaClient
from lambda_ssakssak.lambda_version_gatherer import LambdaVersionGatherer
from lambda_ssakssak.lambda_version_chooser import LambdaVersionChooser
from lambda_ssakssak.lambda_version_mapper import LambdaVersionMapper

class LambdaCleanOptions(TypedDict):
    client: LambdaClient
    dry_run: bool
    keep: int
    num_threads: int

def _alias_version_arns(client: LambdaClient, versions: list[LambdaVersionMapper]) -> set[str]:
    """ARNs of versions pointed to by aliases (AWS refuses to delete them)."""
    arns: set[str] = set()
    paginator = client.get_paginator('list_aliases')
    for func_name in {v.func_name for v in versions}:
        for page in paginator.paginate(FunctionName=func_name):
            for alias in page['Aliases']:
                targets = [alias['FunctionVersion']]
                routing = alias.get('RoutingConfig', {}).get('AdditionalVersionWeights', {})
                targets.extend(routing.keys())
                for v in versions:
                    if v.func_name == func_name and v.version in targets:
                        arns.add(v.version_arn)
    return arns

def run_cleaner(**kargs: Unpack[LambdaCleanOptions]):
    client = kargs['client']
    dry_run = kargs['dry_run']

    versions = LambdaVersionGatherer(client=client).gather(num_threads=kargs['num_threads'])

    chooser = LambdaVersionChooser(versions=versions)
    chooser.mark_retain_latest()
    chooser.mark_retain_recent(kargs['keep'])
    chooser.mark_retain_by_arns(_alias_version_arns(client, versions))
    chooser.mark_deleted_all()

    targets = sorted(
        (v for v in versions if v.is_to_be_deleted()),
        key=lambda v: (v.func_name, int(v.version)),
    )

    print(f'{len(targets)} of {len(versions)} versions to be deleted')
    for v in targets:
        if dry_run:
            print(f'[dry-run] {v.func_name}:{v.version} (last modified {v.last_modified_at.isoformat()})')
            continue
        client.delete_function(FunctionName=v.func_name, Qualifier=v.version)
        print(f'[deleted] {v.func_name}:{v.version}')
