from dataclasses import dataclass
from typing import TypeVar, Union, Optional, Generic

T = TypeVar("T")


@dataclass
class Success(Generic[T]):
    data: Optional[T] = None
    status: str = "success"


@dataclass
class Error:
    error: str
    message: str
    status: str = "error"


Response = Union[Success[T], Error]
