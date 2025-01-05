import threading
from typing import TypedDict, Optional, cast
from typing_extensions import Unpack

THREAD_LOCAL = threading.local()

class Context(TypedDict):
    aws_region: str

class ContextStorage():
    def put(self, **kargs: Unpack[Context]) -> None:
        if hasattr(THREAD_LOCAL, 'datas') is False:
            THREAD_LOCAL.datas = {}
        THREAD_LOCAL.datas.update(**kargs)

    def get(self) -> Optional[Context]:
        if hasattr(THREAD_LOCAL, 'datas') is False:
            return None
        storage = cast(Context, THREAD_LOCAL.datas)
        return storage

storage = ContextStorage()

def get_ctx() -> ContextStorage:
    return storage
