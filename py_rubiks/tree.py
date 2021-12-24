from __future__ import annotations

import weakref
from functools import cached_property
from typing import List, Optional

import attr

from py_rubiks.cube import Cube


@attr.s(auto_attribs=True)
class Node:
    cube: Cube

    parent: Optional[Node] = attr.ib(init=False, repr=False, default=None)
    children: List[Node] = attr.ib(factory=list, init=False, repr=False)
    visited: bool = attr.ib(default=False, init=False)

    @cached_property
    def depth(self) -> int:
        """Return the depth of `self` in the tree, this is zero-indexed."""
        if self.parent:
            return 1 + self.parent.depth
        return 0

    @property
    def is_fully_visited(self) -> bool:
        if not self.visited:
            return False
        for child in self.children:
            if not child.is_fully_visited:
                return False
        return True

    def add(self, child: Node) -> None:
        child.parent = weakref.proxy(self)
        self.children.append(child)

    def backtrace(self) -> List[Node]:
        """Return the path back up to the root from `self`, not including the root."""
        if not self.parent:
            return []
        path: List[Node] = [self]
        path.extend(self.parent.backtrace())
        return path

    def delete(self) -> None:
        """Break the reference cycle to allow `self` and all children to be gc'd."""
        if self.parent:
            self.parent.children.remove(self)
        self.children = []

    def highest_fully_visited_node(self) -> Optional[Node]:
        if parent := self.parent:
            if parent.is_fully_visited:
                return parent.highest_fully_visited_node()
            else:
                return self
        else:
            if self.is_fully_visited:
                return self
            else:
                return None

    def prune(self, previous: Optional[Node] = None) -> None:
        if not self.parent:
            return None
        if self.is_fully_visited:
            self.parent.prune(self)
        else:
            if previous:
                previous.delete()
