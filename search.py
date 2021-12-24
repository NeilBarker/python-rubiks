import time
from typing import List, Set

from py_rubiks.cube import Cube, CubeFace
from py_rubiks.tree import Node


GOAL_CUBE = Cube(
    front=CubeFace([["B", "B", "B"], ["B", "B", "B"], ["B", "B", "B"],]),
    right=CubeFace([["R", "R", "R"], ["R", "R", "R"], ["R", "R", "R"],]),
    back=CubeFace([["G", "G", "G"], ["G", "G", "G"], ["G", "G", "G"],]),
    left=CubeFace([["O", "O", "O"], ["O", "O", "O"], ["O", "O", "O"],]),
    top=CubeFace([["Y", "Y", "Y"], ["Y", "Y", "Y"], ["Y", "Y", "Y"],]),
    bottom=CubeFace([["W", "W", "W"], ["W", "W", "W"], ["W", "W", "W"],]),
)


# INITIAL_CUBE = Cube(
#     front=CubeFace([["B", "B", "B"], ["B", "B", "B"], ["B", "B", "B"],]),
#     right=CubeFace([["Y", "R", "R"], ["Y", "R", "R"], ["Y", "R", "R"],]),
#     back=CubeFace([["G", "G", "G"], ["G", "G", "G"], ["G", "G", "G"],]),
#     left=CubeFace([["O", "O", "W"], ["O", "O", "W"], ["O", "O", "W"],]),
#     top=CubeFace([["Y", "Y", "Y"], ["Y", "Y", "Y"], ["O", "O", "O"],]),
#     bottom=CubeFace([["R", "R", "R"], ["W", "W", "W"], ["W", "W", "W"],]),
# )


INITIAL_CUBE = Cube(
    front=CubeFace([["G", "O", "G"], ["R", "Y", "W"], ["B", "Y", "B"],]),
    right=CubeFace([["O", "W", "R"], ["B", "R", "G"], ["Y", "Y", "O"],]),
    back=CubeFace([["B", "O", "G"], ["W", "W", "R"], ["B", "Y", "G"],]),
    left=CubeFace([["Y", "Y", "O"], ["B", "O", "G"], ["W", "W", "Y"],]),
    top=CubeFace([["R", "G", "W"], ["R", "G", "O"], ["W", "B", "Y"],]),
    bottom=CubeFace([["O", "G", "R"], ["R", "B", "O"], ["R", "B", "W"],]),
)


def depth_limited_search(tree: Node) -> Node:
    visited_nodes: Set[str] = set()
    frontier: List[Node] = [tree]

    while frontier:
        node = frontier.pop()
        node.visited = True

        if node.depth == 30:
            node.prune()
            continue

        state_str = node.cube.state_str
        if state_str not in visited_nodes:
            if node.cube == GOAL_CUBE:
                return node

            visited_nodes.add(state_str)
            for successor in node.cube.successors():
                successor_node = Node(successor)
                node.add(successor_node)
                frontier.append(successor_node)

    raise RuntimeError("No solution found")


if __name__ == "__main__":
    start_time = time.time()

    root = Node(INITIAL_CUBE)
    goal_node = depth_limited_search(root)

    print(f"Found solution in {time.time() - start_time} seconds")
    print(f"at depth: {goal_node.depth}")

    for node in goal_node.backtrace():
        if node.cube.from_move:
            print(
                f"{node.cube.from_move.face_ref} --> turns: {node.cube.from_move.steps}"
            )
        else:
            print("Something went wrong...")
