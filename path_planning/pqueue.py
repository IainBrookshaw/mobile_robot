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

    def pop(self, goal) -> Any:
        """
        Pops of the best node and returns it (the ranking is not returned)
        """
        if len(self._data) == 0:
            raise Exception

        tie_idx = self._have_ties()
        if 0 < tie_idx:
            best = self._break_tie(tie_idx, goal)
            self._data = self._data[tie_idx:]
        else:
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

    def _have_ties(self):
        first = self._data[0]
        tie_count = 0
        for d in range(1, len(self._data)):
            if self._data[d] == first:
                tie_count += 1
            else:
                break

        return tie_count

    def _break_tie(self, tie_end, goal):
        ties = self._data[0:tie_end]
        min_dist2 = 1e9
        best = None

        for t in ties:
            d_row = t[1].pose[0] - goal[0]
            d_col = t[1].pose[1] - goal[1]
            d2 = d_row*d_row + d_col*d_col

            if d2 < min_dist2:
                min_dist2 = d2
                best = t

        return best
