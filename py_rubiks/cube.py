"""Model of a Rubiks Cube."""

from __future__ import annotations

from copy import copy
from enum import Enum
from typing import Generator, List, Optional

import attr


FaceGrid = List[List[str]]  # 3 x 3 grid


class EdgeRef(Enum):
    TOP = 1
    RIGHT = 2
    BOTTOM = 3
    LEFT = 4


@attr.s(auto_attribs=True, frozen=True, slots=True)
class CubeFace:
    """Model class for a Rubiks Cube face.

    Each `CubeFace` is considered to be immutable, rotation operations will return new
    `CubeFace` instances.

    """

    state: FaceGrid

    @property
    def state_str(self) -> str:
        return "".join("".join(row) for row in self.state)

    @property
    def top_edge(self) -> List[str]:
        return self.state[0][:]

    @property
    def right_edge(self) -> List[str]:
        return [self.state[idx][-1] for idx in range(len(self.state))]

    @property
    def bottom_edge(self) -> List[str]:
        return self.state[-1][:]

    @property
    def left_edge(self) -> List[str]:
        return [self.state[idx][0] for idx in range(len(self.state))]

    def __copy__(self) -> CubeFace:
        copied_state = [row[:] for row in self.state]
        return CubeFace(copied_state)

    def rotate(self, steps: int) -> CubeFace:
        """Return a new `CubeFace` that's been rotated by the specifed number of steps.

        NOTE: The rotation is clockwise.

        Args:
            steps: The number of rotations to complete.

        """
        rotated_face = [row[:] for row in self.state]
        cube_length = len(self.state)
        index_range = cube_length - 1  # Account for 0 based indexing
        for _ in range(steps):
            previous_state = [row[:] for row in rotated_face]
            for row in range(cube_length):
                for col in range(cube_length):
                    rotated_face[row][col] = previous_state[index_range - col][row]
        return CubeFace(rotated_face)

    def mirror(self, about: EdgeRef) -> CubeFace:
        """Return a mirrored version of self about the specified edge."""
        if about == EdgeRef.TOP or about == EdgeRef.BOTTOM:
            mirrored = [row[:] for row in self.state]
            mirrored.reverse()
            return CubeFace(mirrored)
        else:
            mirrored = []
            for row in self.state:
                flipped = row[:]
                flipped.reverse()
                mirrored.append(flipped)
            return CubeFace(mirrored)

    def replace_edge(self, edge_ref: EdgeRef, values: List[str]) -> CubeFace:
        """Return a new `CubeFace` with the edge values replaced."""
        new_state = [row[:] for row in self.state]
        if edge_ref == EdgeRef.TOP:
            new_state[0] = values[:]
        elif edge_ref == EdgeRef.BOTTOM:
            new_state[-1] = values[:]
        elif edge_ref == EdgeRef.LEFT:
            for idx in range(len(new_state)):
                new_state[idx][0] = values[idx]
        else:
            for idx in range(len(new_state)):
                new_state[idx][-1] = values[idx]
        return CubeFace(new_state)

    def fuzzy_match(self, other: CubeFace) -> bool:
        if self.state == other.state:
            return True
        for row_idx in range(len(self.state)):
            my_row = self.state[row_idx]
            other_row = other.state[row_idx]
            if my_row == other_row:
                continue
            for col_idx in range(len(my_row)):
                my_colour = my_row[col_idx]
                other_colour = other_row[col_idx]
                if not any(
                    [my_colour == other_colour, my_colour == "*", other_colour == "*"]
                ):
                    return False
        return True


@attr.s(auto_attribs=True, frozen=True, slots=True)
class Move:
    """Model to track the move that was used to generate a cube state."""

    face_ref: FaceRef
    steps: int

    def is_reverse(self, other: Move) -> bool:
        """Return `True` if other would undo `self`."""
        if not self.face_ref == other.face_ref:
            return False
        if self.steps == 1 and other.steps == 3 or self.steps == 2 and other.steps == 2:
            return True
        return False


class FaceRef(Enum):
    F = "front"
    R = "right"
    B = "back"
    L = "left"
    U = "top"
    D = "bottom"


@attr.s(auto_attribs=True, frozen=True, slots=True)
class Cube:
    """Model class for a Rubiks cube.

    Each `Cube` is considered to be immutable, rotation operations will return new
    `Cube` instances.

    If the `Cube` is being instantiated from a cube rotation, the `universal_front_face`
    attribute should reference the face that was the original front face. This allows
    the cube to be rotated back to its original orientation.

    """

    front: CubeFace
    right: CubeFace
    back: CubeFace
    left: CubeFace
    top: CubeFace
    bottom: CubeFace

    universal_front_face: Optional[FaceRef] = attr.ib(cmp=False, default=None)
    from_move: Optional[Move] = attr.ib(cmp=False, default=None)

    @property
    def state_str(self) -> str:
        return "".join(
            face.state_str
            for face in [
                self.front,
                self.right,
                self.back,
                self.left,
                self.top,
                self.bottom,
            ]
        )

    def __copy__(self) -> Cube:
        return Cube(
            copy(self.front),
            copy(self.right),
            copy(self.back),
            copy(self.left),
            copy(self.top),
            copy(self.bottom),
            copy(self.universal_front_face),
            copy(self.from_move),
        )

    def rotate_layer(self, face_ref: FaceRef, steps: int) -> Cube:
        """Return a new `Cube` where the specified layer has been rotated `steps` times.

        If the non-facing layer is required to be rotated, the cube is rotated such that
        the required layer is the facing layer. The facing layer is then rotated and
        the cube is rotated back to its original orientation before returning.

        NOTE: The face rotation is clockwise.

        Args:
            steps: The number of rotations to complete.

        Returns:
            A new `Cube` where the required layer has been rotated `steps` times.

        """
        rotated = copy(self)

        if face_ref == FaceRef.F:

            for _ in range(steps):
                previous = copy(rotated)

                new_front = rotated.front.rotate(steps)

                # Front has borders with top, right, bottom, left

                # Right edge of left face becomes bottom edge of top face
                new_top = rotated.top.replace_edge(
                    EdgeRef.BOTTOM, previous.left.right_edge
                )

                # Bottom edge of top face becomes left edge of the right face
                new_right = rotated.right.replace_edge(
                    EdgeRef.LEFT, previous.top.bottom_edge
                )

                # Left edge of right face becomes top edge of bottom face
                new_bottom = rotated.bottom.replace_edge(
                    EdgeRef.TOP, previous.right.left_edge
                )

                # Top edge of bottom face becomes right edge of left face
                new_left = rotated.left.replace_edge(
                    EdgeRef.RIGHT, previous.bottom.top_edge
                )

                # 'Update' the frozen rotated `Cube`
                rotated = attr.evolve(
                    rotated,
                    front=new_front,
                    top=new_top,
                    right=new_right,
                    bottom=new_bottom,
                    left=new_left,
                )

        else:
            # Rotate the cube such that the specified face is the front face
            # then rotate the front layer, and finally rotate the cube back to it's
            # original orientation
            rotated = self.rotate_cube(face_ref)
            rotated = rotated.rotate_layer(FaceRef.F, steps)
            rotated = rotated.rotate_cube(rotated.universal_front_face)  # type: ignore

        return rotated

    def rotate_cube(self, face_ref: FaceRef) -> Cube:
        """Return a new `Cube` such that the specified face is the front face."""
        # Faces in the axis of cube rotation rotate with the cube.
        # Other faces are either mirrored or cloned depending on their index reference
        if face_ref == FaceRef.F:
            dup = attr.evolve(copy(self), universal_front_face=FaceRef.F)
            return dup
        elif face_ref == FaceRef.R:
            return Cube(
                front=copy(self.right),
                right=copy(self.back),
                back=copy(self.left),
                left=copy(self.front),
                top=self.top.rotate(1),  # Right edge becomes bottom edge
                bottom=self.bottom.rotate(3),  # Right edge becomes top edge
                universal_front_face=FaceRef.L,  # Original front is new left
            )
        elif face_ref == FaceRef.B:
            return Cube(
                front=copy(self.back),
                right=copy(self.left),
                back=copy(self.front),
                left=copy(self.right),
                top=self.top.rotate(2),  # Top edge becomes bottom edge
                bottom=self.bottom.rotate(2),
                universal_front_face=FaceRef.B,
            )
        elif face_ref == FaceRef.L:
            return Cube(
                front=copy(self.left),
                right=copy(self.front),
                back=copy(self.right),
                left=copy(self.back),
                top=self.top.rotate(3),  # Top edge becomes left edge
                bottom=self.bottom.rotate(1),  # Left edge becomes top edge
                universal_front_face=FaceRef.R,
            )
        elif face_ref == FaceRef.U:
            return Cube(
                front=copy(self.top),
                right=self.right.rotate(3),  # Top edge becomes left edge
                back=self.bottom.mirror(EdgeRef.TOP),  # Top edge becomes bottom edge
                left=self.left.rotate(1),  # Top edge becomes left edge
                top=self.back.mirror(EdgeRef.TOP).mirror(
                    EdgeRef.LEFT
                ),  # Top edge becomes bottom edge - double mirror to account for index
                # reference flip
                bottom=copy(self.front),
                universal_front_face=FaceRef.D,
            )
        else:  # Bottom
            return Cube(
                front=copy(self.bottom),
                right=self.right.rotate(1),  # Bottom edge becomes left edge
                back=self.top.mirror(EdgeRef.TOP).mirror(
                    EdgeRef.LEFT
                ),  # Top edge becomes bottom edge
                left=self.left.rotate(3),  # Top edge becomes left edge
                top=copy(self.front),
                bottom=self.back.mirror(EdgeRef.BOTTOM),  # Top edge becomes bottom edge
                universal_front_face=FaceRef.U,
            )

    def successors(self) -> Generator[Cube, None, None]:
        """Yield successor cubes from the current state.

        This function will not yield the parent of the current state.

        Each face can be rotated 3 times which means the root node has 18 successors.

        Yields:
            Successor `Cube` instances.

        """
        for face_ref in FaceRef:
            for step in range(1, 4):
                if self.from_move:
                    if self.from_move.face_ref == face_ref:
                        continue
                successor = self.rotate_layer(face_ref, step)
                successor = attr.evolve(successor, from_move=Move(face_ref, step))
                yield successor

    def fuzzy_match(self, other: Cube) -> bool:
        """Return `True` if self's faces match the other's faces.

        This is a fuzzy match as the other's state can include wildcards.

        Args:
            other: pass.

        Returns:
            True or False.

        """
        if not self.front.fuzzy_match(other.front):
            return False
        if not self.right.fuzzy_match(other.right):
            return False
        if not self.back.fuzzy_match(other.back):
            return False
        if not self.left.fuzzy_match(other.left):
            return False
        if not self.top.fuzzy_match(other.top):
            return False
        if not self.bottom.fuzzy_match(other.bottom):
            return False
        return True
