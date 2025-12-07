
class LambdaNotationInvalidException(Exception):
    pass

class LambdaVersionNotationInvalidException(Exception):
    pass

def ensure_valid_lambda_arn(lambda_arn: str):
    """
    Ensures given lambda  arn expression is valid (note: not a VERSION ARN)
    """
    is_start_with_arn = lambda_arn.startswith('arn:aws:lambda')
    if not is_start_with_arn:
        raise LambdaNotationInvalidException('not a valid lambda arn')

def ensure_valid_version_arn(version_arn: str):
    """
    Ensures given lambda version arn expression is valid (note: not a LAMBDA ARN)
    """
    ensure_valid_lambda_arn(version_arn)
    splited_with_colon = version_arn.split(':')
    is_end_with_vernum = splited_with_colon[-1].isnumeric()
    is_version_latest = splited_with_colon[-1] == '$LATEST'
    if not is_end_with_vernum and not is_version_latest:
        raise LambdaVersionNotationInvalidException('not a valid lambda version arn.')
    