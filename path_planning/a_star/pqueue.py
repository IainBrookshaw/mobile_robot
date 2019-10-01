#! /usr/bin/env python3
"""
Mobile Robot Path Planning: Simple Priority Queue
Iain Brookshaw
Copyright (c), 2019. All Rights Reserved
MIT License
"""
from typing import Tuple, Dict, List, Callable, Any


class Pqueue:
    """
    This is a very simple implementation of a priority queue for the A*
    application. The stock queue.PriorityQueue does not have quite the
    accessibility that is needed.

    This implementation is rough, and may be sub-optimal
    """

    def __init__(self):
        self._data = []

    def insert(self, data: Tuple[float, Any]) -> None:
        if data not in self._data:
            self._data.append(data)
            self.resort()

    def pop(self) -> Any:
        """
        Pops of the best node and returns it (the ranking is not returned)
        """
        if len(self._data) == 0:
            raise Exception

        best = self._data[0][1]
        self._data = self._data[1:]
        return best

    def resort(self) -> None:
        self._data.sort()

    def remove(self, data: Tuple[float, Any]) -> None:
        self._data.remove(data)

    def size(self) -> int:
        return len(self._data)

    def contains(self, node: Any) -> bool:
        for d in self._data:
            if node in d:
                return True
        return False
