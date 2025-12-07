from typing import TypedDict
from typing_extensions import Unpack
from mypy_boto3_lambda import LambdaClient
from lambda_mapper import LambdaMapper
from lambda_version_mapper import LambdaVersionMapper
from queue import Queue
from threading import Thread, Lock

class Constructor(TypedDict):
    client: LambdaClient

class GatherParam(TypedDict):
    num_threads: int

class LambdaVersionGatherer:
    """
    Module for gathering all lambda versions within AWS Region
    usage: LambdaVersionGatherer(client).gather(num_threads=10)
    """

    def __init__(self, **kargs: Unpack[Constructor]):
        """
        client: LambdaClient
        """
        self.__client = kargs['client']

    def gather(self, **kargs: Unpack[GatherParam]):
        """
        Gethers all lambda function versions from aws
        @param num_threads number of thread for LambdaVersionGatherer
        """
        num_threads_from_param = kargs['num_threads']
        num_threads = 5
        if num_threads_from_param:
            num_threads = num_threads_from_param
        
        all_lambdas = self.__gather_lambdas()
        all_versions = self.__gather_versions(all_lambdas, num_threads)
        return all_versions

    def __gather_lambdas(self):
        all_lambdas = LambdaMapper.fetch_all(self.__client)
        return all_lambdas
    
    def __gather_versions(self, all_lambdas: list[LambdaMapper], num_threads: int):
        """
        Gather all lambda versions from lambda functions runs within thread.
        @param all_lambdas lambda functions
        @param num_threads number of threads for processing
        """
        queue = Queue()
        for elem in all_lambdas:
            queue.put(elem)

        all_versions: list[LambdaVersionMapper] = []
        lock_for_versions = Lock()

        def version_read_thread(lambda_: LambdaMapper):
            versions = LambdaVersionMapper.from_lambda(lambda_, self.__client)
            with lock_for_versions:
                all_versions.extend(versions)
            print(f'lambda versions gathered, size: {len(all_versions)}')
        
        while True:
            is_empty: bool = False
            threads: list[Thread] = []

            for _ in range(num_threads):
                if queue.empty():
                    is_empty = queue.empty()
                    break
                lambda_: LambdaMapper = queue.get()
                threads.append(Thread(
                    target=version_read_thread,
                    args=[lambda_]
                ))
            
            if len(threads) > 0:
                for t in threads:
                    t.start()
                for t in threads:
                    t.join()

            if is_empty:
                break

        return all_versions
