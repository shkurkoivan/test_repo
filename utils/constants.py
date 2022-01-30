from enum import Enum


class STATUS_CODE(Enum):
    OK = 200
    BAD_REQUEST = 400
    UNAUTHORIZED = 401


class COLLECTION(Enum):
    ITEMS_MAX_CAPACITY = 500
