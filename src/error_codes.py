from enum import IntEnum


class ErrorCode(IntEnum):
    OK = 0
    ZT_SERVICE_NOT_RUNNING = 1
    ZT_NO_ACCESS_TOKEN = 2
    ZT_NOT_INSTALLED = 127
