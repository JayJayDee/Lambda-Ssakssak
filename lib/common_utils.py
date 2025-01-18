
# Ensures given version arn is valid
def ensure_valid_version_arn(version_arn: str):
    is_start_with = version_arn.startswith('arn:aws:lambda')