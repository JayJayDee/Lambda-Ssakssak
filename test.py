import lib.aws_factory as aws_factory
from lib.restapi_mapper import RestApiMapper

if __name__ == '__main__':
    client = aws_factory.apigw('ap-northeast-2')
    all_rest_apis = RestApiMapper.fetch_all(client)
    print(list(map(lambda x : x.str(), all_rest_apis)))