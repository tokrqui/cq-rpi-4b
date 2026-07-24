from dataclasses import dataclass
from typing import Callable
import cadquery as cq


@dataclass
class ConnectorItem:
    name: str
    make_func: Callable
    position: tuple[float, float, float]
    rotation: tuple[float, float, float]