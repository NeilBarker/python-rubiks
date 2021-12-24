from py_rubiks.cube import Cube, CubeFace, EdgeRef, FaceRef, Move

import pytest


class TestCubeFace:
    def test_edge_accessors(self):
        initial_state = [
            ["R", "R", "R"],
            ["G", "G", "G"],
            ["B", "B", "B"],
        ]
        face = CubeFace(initial_state)

        assert face.top_edge == ["R", "R", "R"]
        assert face.bottom_edge == ["B", "B", "B"]
        assert face.left_edge == ["R", "G", "B"]
        assert face.right_edge == ["R", "G", "B"]

    @pytest.mark.parametrize(
        "steps, expected",
        (
            (1, [["B", "G", "R"], ["B", "G", "R"], ["B", "G", "R"],]),
            (2, [["B", "B", "B"], ["G", "G", "G"], ["R", "R", "R"],]),
            (3, [["R", "G", "B"], ["R", "G", "B"], ["R", "G", "B"],]),
        ),
        ids=("1 step", "2 steps", "3 steps"),
    )
    def test_rotation(self, steps, expected):
        initial_state = [
            ["R", "R", "R"],
            ["G", "G", "G"],
            ["B", "B", "B"],
        ]
        face = CubeFace(initial_state)
        rotated = face.rotate(steps)
        assert rotated.state == expected

    @pytest.mark.parametrize(
        "edge_ref, values, expected",
        (
            (
                EdgeRef.TOP,
                ["X", "Y", "Z"],
                [["X", "Y", "Z"], ["R", "R", "R"], ["R", "R", "R"],],
            ),
            (
                EdgeRef.BOTTOM,
                ["X", "Y", "Z"],
                [["R", "R", "R"], ["R", "R", "R"], ["X", "Y", "Z"],],
            ),
            (
                EdgeRef.LEFT,
                ["X", "Y", "Z"],
                [["X", "R", "R"], ["Y", "R", "R"], ["Z", "R", "R"],],
            ),
            (
                EdgeRef.RIGHT,
                ["X", "Y", "Z"],
                [["R", "R", "X"], ["R", "R", "Y"], ["R", "R", "Z"],],
            ),
        ),
        ids=("Top edge", "Bottom edge", "Left edge", "Right edge"),
    )
    def test_replace_edge(self, edge_ref, values, expected):
        initial_state = [
            ["R", "R", "R"],
            ["R", "R", "R"],
            ["R", "R", "R"],
        ]
        face = CubeFace(initial_state)
        updated = face.replace_edge(edge_ref, values)
        assert updated.state == expected

    @pytest.mark.parametrize(
        "edge_ref, expected",
        (
            (EdgeRef.TOP, [["G", "H", "I"], ["D", "E", "F"], ["A", "B", "C"],]),
            (EdgeRef.BOTTOM, [["G", "H", "I"], ["D", "E", "F"], ["A", "B", "C"],]),
            (EdgeRef.LEFT, [["C", "B", "A"], ["F", "E", "D"], ["I", "H", "G"],]),
            (EdgeRef.RIGHT, [["C", "B", "A"], ["F", "E", "D"], ["I", "H", "G"],]),
        ),
        ids=("Top edge", "Bottom edge", "Left edge", "Right edge"),
    )
    def test_mirror(self, edge_ref, expected):
        initial_state = [
            ["A", "B", "C"],
            ["D", "E", "F"],
            ["G", "H", "I"],
        ]
        face = CubeFace(initial_state)
        mirrored = face.mirror(edge_ref)
        assert mirrored.state == expected

    @pytest.mark.parametrize(
        "other, expected",
        (
            (CubeFace([["*", "*", "*"], ["*", "*", "*"], ["*", "*", "*"]]), True),
            (CubeFace([["Z", "Z", "Z"], ["Z", "Z", "Z"], ["Z", "Z", "Z"]]), False),
            (CubeFace([["A", "B", "C"], ["D", "E", "F"], ["G", "H", "I"]]), True),
            (CubeFace([["*", "*", "*"], ["D", "E", "F"], ["G", "H", "I"]]), True),
            (CubeFace([["*", "*", "*"], ["Z", "E", "F"], ["G", "H", "I"]]), False),
        ),
        ids=("All wildcards", "No matches", "Identical", "Partial match", "One wrong"),
    )
    def test_fuzzy_match(self, other, expected):
        initial_state = [
            ["A", "B", "C"],
            ["D", "E", "F"],
            ["G", "H", "I"],
        ]
        face = CubeFace(initial_state)
        assert face.fuzzy_match(other) is expected


class TestMove:
    @pytest.mark.parametrize(
        "left, right, expected",
        (
            (Move(FaceRef.F, 1), Move(FaceRef.R, 3), False),
            (Move(FaceRef.F, 1), Move(FaceRef.F, 3), True),
            (Move(FaceRef.F, 2), Move(FaceRef.F, 2), True),
        ),
        ids=("Different faces", "True reverse 1", "True reverse 2"),
    )
    def test_is_reverse(self, left, right, expected):
        assert left.is_reverse(right) is expected


initial_cube_state = [
    CubeFace([["O", "O", "O"], ["O", "O", "O"], ["O", "O", "O"],]),  # Front
    CubeFace([["G", "G", "G"], ["G", "G", "G"], ["G", "G", "G"],]),  # Right
    CubeFace([["R", "R", "R"], ["R", "R", "R"], ["R", "R", "R"],]),  # Back
    CubeFace([["B", "B", "B"], ["B", "B", "B"], ["B", "B", "B"],]),  # Left
    CubeFace([["W", "W", "W"], ["W", "W", "W"], ["W", "W", "W"],]),  # Top
    CubeFace([["Y", "Y", "Y"], ["Y", "Y", "Y"], ["Y", "Y", "Y"],]),  # Bottom
]

shuffled_cube_state = [  # Using numbers to make assertions easier
    CubeFace([["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"],]),  # Front
    CubeFace([["10", "11", "12"], ["13", "14", "15"], ["16", "17", "18"],]),  # Right
    CubeFace([["19", "20", "21"], ["22", "23", "24"], ["25", "26", "27"],]),  # Back
    CubeFace([["28", "29", "30"], ["31", "32", "33"], ["34", "35", "36"],]),  # Left
    CubeFace([["37", "38", "39"], ["40", "41", "42"], ["43", "44", "45"],]),  # Top
    CubeFace([["46", "47", "48"], ["49", "50", "51"], ["52", "53", "54"],]),  # Bottom
]


class TestCube:
    @pytest.mark.parametrize(
        "steps, expected",
        (
            (
                1,
                Cube(
                    *[  # type: ignore
                        CubeFace(
                            [["O", "O", "O"], ["O", "O", "O"], ["O", "O", "O"],]
                        ),  # Front
                        CubeFace(
                            [["W", "G", "G"], ["W", "G", "G"], ["W", "G", "G"],]
                        ),  # Right
                        CubeFace(
                            [["R", "R", "R"], ["R", "R", "R"], ["R", "R", "R"],]
                        ),  # Back
                        CubeFace(
                            [["B", "B", "Y"], ["B", "B", "Y"], ["B", "B", "Y"],]
                        ),  # Left
                        CubeFace(
                            [["W", "W", "W"], ["W", "W", "W"], ["B", "B", "B"],]
                        ),  # Top
                        CubeFace(
                            [["G", "G", "G"], ["Y", "Y", "Y"], ["Y", "Y", "Y"],]
                        ),  # Bottom
                    ]
                ),
            ),
            (
                2,
                Cube(
                    *[  # type: ignore
                        CubeFace(
                            [["O", "O", "O"], ["O", "O", "O"], ["O", "O", "O"],]
                        ),  # Front
                        CubeFace(
                            [["B", "G", "G"], ["B", "G", "G"], ["B", "G", "G"],]
                        ),  # Right
                        CubeFace(
                            [["R", "R", "R"], ["R", "R", "R"], ["R", "R", "R"],]
                        ),  # Back
                        CubeFace(
                            [["B", "B", "G"], ["B", "B", "G"], ["B", "B", "G"],]
                        ),  # Left
                        CubeFace(
                            [["W", "W", "W"], ["W", "W", "W"], ["Y", "Y", "Y"],]
                        ),  # Top
                        CubeFace(
                            [["W", "W", "W"], ["Y", "Y", "Y"], ["Y", "Y", "Y"],]
                        ),  # Bottom
                    ]
                ),
            ),
            (
                3,
                Cube(
                    *[  # type: ignore
                        CubeFace(
                            [["O", "O", "O"], ["O", "O", "O"], ["O", "O", "O"],]
                        ),  # Front
                        CubeFace(
                            [["Y", "G", "G"], ["Y", "G", "G"], ["Y", "G", "G"],]
                        ),  # Right
                        CubeFace(
                            [["R", "R", "R"], ["R", "R", "R"], ["R", "R", "R"],]
                        ),  # Back
                        CubeFace(
                            [["B", "B", "W"], ["B", "B", "W"], ["B", "B", "W"],]
                        ),  # Left
                        CubeFace(
                            [["W", "W", "W"], ["W", "W", "W"], ["G", "G", "G"],]
                        ),  # Top
                        CubeFace(
                            [["B", "B", "B"], ["Y", "Y", "Y"], ["Y", "Y", "Y"],]
                        ),  # Bottom
                    ]
                ),
            ),
        ),
        ids=("1 step", "2 steps", "3 steps"),
    )
    def test_front_face_layer_rotation(self, steps, expected):
        initial_cube = Cube(*initial_cube_state)
        rotated = initial_cube.rotate_layer(FaceRef.F, steps)
        assert rotated == expected

    def test_rotate_cube_for_front_face(self):
        initial_cube = Cube(*shuffled_cube_state)
        rotated = initial_cube.rotate_cube(FaceRef.F)
        assert rotated == initial_cube
        assert rotated.universal_front_face == FaceRef.F

    def test_rotate_cube_for_right_face(self):
        initial_cube = Cube(*shuffled_cube_state)
        rotated = initial_cube.rotate_cube(FaceRef.R)
        assert rotated.front == initial_cube.right
        assert rotated.right == initial_cube.back
        assert rotated.back == initial_cube.left
        assert rotated.left == initial_cube.front
        assert rotated.top.state == [
            ["43", "40", "37"],
            ["44", "41", "38"],
            ["45", "42", "39"],
        ]
        assert rotated.bottom.state == [
            ["48", "51", "54"],
            ["47", "50", "53"],
            ["46", "49", "52"],
        ]
        assert rotated.universal_front_face == FaceRef.L

    def test_rotate_cube_for_back_face(self):
        initial_cube = Cube(*shuffled_cube_state)
        rotated = initial_cube.rotate_cube(FaceRef.B)
        assert rotated.front == initial_cube.back
        assert rotated.right == initial_cube.left
        assert rotated.back == initial_cube.front
        assert rotated.left == initial_cube.right
        assert rotated.top.state == [
            ["45", "44", "43"],
            ["42", "41", "40"],
            ["39", "38", "37"],
        ]
        assert rotated.bottom.state == [
            ["54", "53", "52"],
            ["51", "50", "49"],
            ["48", "47", "46"],
        ]
        assert rotated.universal_front_face == FaceRef.B

    def test_rotate_cube_for_left_face(self):
        initial_cube = Cube(*shuffled_cube_state)
        rotated = initial_cube.rotate_cube(FaceRef.L)
        assert rotated.front == initial_cube.left
        assert rotated.right == initial_cube.front
        assert rotated.back == initial_cube.right
        assert rotated.left == initial_cube.back
        assert rotated.top.state == [
            ["39", "42", "45"],
            ["38", "41", "44"],
            ["37", "40", "43"],
        ]
        assert rotated.bottom.state == [
            ["52", "49", "46"],
            ["53", "50", "47"],
            ["54", "51", "48"],
        ]
        assert rotated.universal_front_face == FaceRef.R

    def test_rotate_cube_for_top_face(self):
        initial_cube = Cube(*shuffled_cube_state)
        rotated = initial_cube.rotate_cube(FaceRef.U)
        assert rotated.front == initial_cube.top
        assert rotated.right.state == [
            ["12", "15", "18"],
            ["11", "14", "17"],
            ["10", "13", "16"],
        ]
        assert rotated.back.state == [
            ["52", "53", "54"],
            ["49", "50", "51"],
            ["46", "47", "48"],
        ]
        assert rotated.left.state == [
            ["34", "31", "28"],
            ["35", "32", "29"],
            ["36", "33", "30"],
        ]
        assert rotated.top.state == [
            ["27", "26", "25"],
            ["24", "23", "22"],
            ["21", "20", "19"],
        ]
        assert rotated.bottom == initial_cube.front
        assert rotated.universal_front_face == FaceRef.D

    def test_rotate_cube_for_bottom_face(self):
        initial_cube = Cube(*shuffled_cube_state)
        rotated = initial_cube.rotate_cube(FaceRef.D)
        assert rotated.front == initial_cube.bottom
        assert rotated.right.state == [
            ["16", "13", "10"],
            ["17", "14", "11"],
            ["18", "15", "12"],
        ]
        assert rotated.back.state == [
            ["45", "44", "43"],
            ["42", "41", "40"],
            ["39", "38", "37"],
        ]
        assert rotated.left.state == [
            ["30", "33", "36"],
            ["29", "32", "35"],
            ["28", "31", "34"],
        ]
        assert rotated.top == initial_cube.front
        assert rotated.bottom.state == [
            ["25", "26", "27"],
            ["22", "23", "24"],
            ["19", "20", "21"],
        ]
        assert rotated.universal_front_face == FaceRef.U

    @pytest.mark.parametrize(
        "face_ref, steps, expected",
        (
            (
                FaceRef.R,
                1,
                Cube(
                    *[  # type: ignore
                        CubeFace(
                            [["O", "O", "Y"], ["O", "O", "Y"], ["O", "O", "Y"],]
                        ),  # Front
                        CubeFace(
                            [["G", "G", "G"], ["G", "G", "G"], ["G", "G", "G"],]
                        ),  # Right
                        CubeFace(
                            [["W", "R", "R"], ["W", "R", "R"], ["W", "R", "R"],]
                        ),  # Back
                        CubeFace(
                            [["B", "B", "B"], ["B", "B", "B"], ["B", "B", "B"],]
                        ),  # Left
                        CubeFace(
                            [["W", "W", "O"], ["W", "W", "O"], ["W", "W", "O"],]
                        ),  # Top
                        CubeFace(
                            [["Y", "Y", "R"], ["Y", "Y", "R"], ["Y", "Y", "R"],]
                        ),  # Bottom
                    ]
                ),
            ),
            (
                FaceRef.R,
                2,
                Cube(
                    *[  # type: ignore
                        CubeFace(
                            [["O", "O", "R"], ["O", "O", "R"], ["O", "O", "R"],]
                        ),  # Front
                        CubeFace(
                            [["G", "G", "G"], ["G", "G", "G"], ["G", "G", "G"],]
                        ),  # Right
                        CubeFace(
                            [["O", "R", "R"], ["O", "R", "R"], ["O", "R", "R"],]
                        ),  # Back
                        CubeFace(
                            [["B", "B", "B"], ["B", "B", "B"], ["B", "B", "B"],]
                        ),  # Left
                        CubeFace(
                            [["W", "W", "Y"], ["W", "W", "Y"], ["W", "W", "Y"],]
                        ),  # Top
                        CubeFace(
                            [["Y", "Y", "W"], ["Y", "Y", "W"], ["Y", "Y", "W"],]
                        ),  # Bottom
                    ]
                ),
            ),
            (
                FaceRef.R,
                3,
                Cube(
                    *[  # type: ignore
                        CubeFace(
                            [["O", "O", "W"], ["O", "O", "W"], ["O", "O", "W"],]
                        ),  # Front
                        CubeFace(
                            [["G", "G", "G"], ["G", "G", "G"], ["G", "G", "G"],]
                        ),  # Right
                        CubeFace(
                            [["Y", "R", "R"], ["Y", "R", "R"], ["Y", "R", "R"],]
                        ),  # Back
                        CubeFace(
                            [["B", "B", "B"], ["B", "B", "B"], ["B", "B", "B"],]
                        ),  # Left
                        CubeFace(
                            [["W", "W", "R"], ["W", "W", "R"], ["W", "W", "R"],]
                        ),  # Top
                        CubeFace(
                            [["Y", "Y", "O"], ["Y", "Y", "O"], ["Y", "Y", "O"],]
                        ),  # Bottom
                    ]
                ),
            ),
            (
                FaceRef.B,
                1,
                Cube(
                    *[  # type: ignore
                        CubeFace(
                            [["O", "O", "O"], ["O", "O", "O"], ["O", "O", "O"],]
                        ),  # Front
                        CubeFace(
                            [["G", "G", "Y"], ["G", "G", "Y"], ["G", "G", "Y"],]
                        ),  # Right
                        CubeFace(
                            [["R", "R", "R"], ["R", "R", "R"], ["R", "R", "R"],]
                        ),  # Back
                        CubeFace(
                            [["W", "B", "B"], ["W", "B", "B"], ["W", "B", "B"],]
                        ),  # Left
                        CubeFace(
                            [["G", "G", "G"], ["W", "W", "W"], ["W", "W", "W"],]
                        ),  # Top
                        CubeFace(
                            [["Y", "Y", "Y"], ["Y", "Y", "Y"], ["B", "B", "B"],]
                        ),  # Bottom
                    ]
                ),
            ),
            (
                FaceRef.B,
                2,
                Cube(
                    *[  # type: ignore
                        CubeFace(
                            [["O", "O", "O"], ["O", "O", "O"], ["O", "O", "O"],]
                        ),  # Front
                        CubeFace(
                            [["G", "G", "B"], ["G", "G", "B"], ["G", "G", "B"],]
                        ),  # Right
                        CubeFace(
                            [["R", "R", "R"], ["R", "R", "R"], ["R", "R", "R"],]
                        ),  # Back
                        CubeFace(
                            [["G", "B", "B"], ["G", "B", "B"], ["G", "B", "B"],]
                        ),  # Left
                        CubeFace(
                            [["Y", "Y", "Y"], ["W", "W", "W"], ["W", "W", "W"],]
                        ),  # Top
                        CubeFace(
                            [["Y", "Y", "Y"], ["Y", "Y", "Y"], ["W", "W", "W"],]
                        ),  # Bottom
                    ]
                ),
            ),
            (
                FaceRef.B,
                3,
                Cube(
                    *[  # type: ignore
                        CubeFace(
                            [["O", "O", "O"], ["O", "O", "O"], ["O", "O", "O"],]
                        ),  # Front
                        CubeFace(
                            [["G", "G", "W"], ["G", "G", "W"], ["G", "G", "W"],]
                        ),  # Right
                        CubeFace(
                            [["R", "R", "R"], ["R", "R", "R"], ["R", "R", "R"],]
                        ),  # Back
                        CubeFace(
                            [["Y", "B", "B"], ["Y", "B", "B"], ["Y", "B", "B"],]
                        ),  # Left
                        CubeFace(
                            [["B", "B", "B"], ["W", "W", "W"], ["W", "W", "W"],]
                        ),  # Top
                        CubeFace(
                            [["Y", "Y", "Y"], ["Y", "Y", "Y"], ["G", "G", "G"],]
                        ),  # Bottom
                    ]
                ),
            ),
            (
                FaceRef.L,
                1,
                Cube(
                    *[  # type: ignore
                        CubeFace(
                            [["W", "O", "O"], ["W", "O", "O"], ["W", "O", "O"],]
                        ),  # Front
                        CubeFace(
                            [["G", "G", "G"], ["G", "G", "G"], ["G", "G", "G"],]
                        ),  # Right
                        CubeFace(
                            [["R", "R", "Y"], ["R", "R", "Y"], ["R", "R", "Y"],]
                        ),  # Back
                        CubeFace(
                            [["B", "B", "B"], ["B", "B", "B"], ["B", "B", "B"],]
                        ),  # Left
                        CubeFace(
                            [["R", "W", "W"], ["R", "W", "W"], ["R", "W", "W"],]
                        ),  # Top
                        CubeFace(
                            [["O", "Y", "Y"], ["O", "Y", "Y"], ["O", "Y", "Y"],]
                        ),  # Bottom
                    ]
                ),
            ),
            (
                FaceRef.L,
                2,
                Cube(
                    *[  # type: ignore
                        CubeFace(
                            [["R", "O", "O"], ["R", "O", "O"], ["R", "O", "O"],]
                        ),  # Front
                        CubeFace(
                            [["G", "G", "G"], ["G", "G", "G"], ["G", "G", "G"],]
                        ),  # Right
                        CubeFace(
                            [["R", "R", "O"], ["R", "R", "O"], ["R", "R", "O"],]
                        ),  # Back
                        CubeFace(
                            [["B", "B", "B"], ["B", "B", "B"], ["B", "B", "B"],]
                        ),  # Left
                        CubeFace(
                            [["Y", "W", "W"], ["Y", "W", "W"], ["Y", "W", "W"],]
                        ),  # Top
                        CubeFace(
                            [["W", "Y", "Y"], ["W", "Y", "Y"], ["W", "Y", "Y"],]
                        ),  # Bottom
                    ]
                ),
            ),
            (
                FaceRef.L,
                3,
                Cube(
                    *[  # type: ignore
                        CubeFace(
                            [["Y", "O", "O"], ["Y", "O", "O"], ["Y", "O", "O"],]
                        ),  # Front
                        CubeFace(
                            [["G", "G", "G"], ["G", "G", "G"], ["G", "G", "G"],]
                        ),  # Right
                        CubeFace(
                            [["R", "R", "W"], ["R", "R", "W"], ["R", "R", "W"],]
                        ),  # Back
                        CubeFace(
                            [["B", "B", "B"], ["B", "B", "B"], ["B", "B", "B"],]
                        ),  # Left
                        CubeFace(
                            [["O", "W", "W"], ["O", "W", "W"], ["O", "W", "W"],]
                        ),  # Top
                        CubeFace(
                            [["R", "Y", "Y"], ["R", "Y", "Y"], ["R", "Y", "Y"],]
                        ),  # Bottom
                    ]
                ),
            ),
            (
                FaceRef.U,
                1,
                Cube(
                    *[  # type: ignore
                        CubeFace(
                            [["G", "G", "G"], ["O", "O", "O"], ["O", "O", "O"],]
                        ),  # Front
                        CubeFace(
                            [["R", "R", "R"], ["G", "G", "G"], ["G", "G", "G"],]
                        ),  # Right
                        CubeFace(
                            [["B", "B", "B"], ["R", "R", "R"], ["R", "R", "R"],]
                        ),  # Back
                        CubeFace(
                            [["O", "O", "O"], ["B", "B", "B"], ["B", "B", "B"],]
                        ),  # Left
                        CubeFace(
                            [["W", "W", "W"], ["W", "W", "W"], ["W", "W", "W"],]
                        ),  # Top
                        CubeFace(
                            [["Y", "Y", "Y"], ["Y", "Y", "Y"], ["Y", "Y", "Y"],]
                        ),  # Bottom
                    ]
                ),
            ),
            (
                FaceRef.U,
                2,
                Cube(
                    *[  # type: ignore
                        CubeFace(
                            [["R", "R", "R"], ["O", "O", "O"], ["O", "O", "O"],]
                        ),  # Front
                        CubeFace(
                            [["B", "B", "B"], ["G", "G", "G"], ["G", "G", "G"],]
                        ),  # Right
                        CubeFace(
                            [["O", "O", "O"], ["R", "R", "R"], ["R", "R", "R"],]
                        ),  # Back
                        CubeFace(
                            [["G", "G", "G"], ["B", "B", "B"], ["B", "B", "B"],]
                        ),  # Left
                        CubeFace(
                            [["W", "W", "W"], ["W", "W", "W"], ["W", "W", "W"],]
                        ),  # Top
                        CubeFace(
                            [["Y", "Y", "Y"], ["Y", "Y", "Y"], ["Y", "Y", "Y"],]
                        ),  # Bottom
                    ]
                ),
            ),
            (
                FaceRef.U,
                3,
                Cube(
                    *[  # type: ignore
                        CubeFace(
                            [["B", "B", "B"], ["O", "O", "O"], ["O", "O", "O"],]
                        ),  # Front
                        CubeFace(
                            [["O", "O", "O"], ["G", "G", "G"], ["G", "G", "G"],]
                        ),  # Right
                        CubeFace(
                            [["G", "G", "G"], ["R", "R", "R"], ["R", "R", "R"],]
                        ),  # Back
                        CubeFace(
                            [["R", "R", "R"], ["B", "B", "B"], ["B", "B", "B"],]
                        ),  # Left
                        CubeFace(
                            [["W", "W", "W"], ["W", "W", "W"], ["W", "W", "W"],]
                        ),  # Top
                        CubeFace(
                            [["Y", "Y", "Y"], ["Y", "Y", "Y"], ["Y", "Y", "Y"],]
                        ),  # Bottom
                    ]
                ),
            ),
            (
                FaceRef.D,
                1,
                Cube(
                    *[  # type: ignore
                        CubeFace(
                            [["O", "O", "O"], ["O", "O", "O"], ["B", "B", "B"],]
                        ),  # Front
                        CubeFace(
                            [["G", "G", "G"], ["G", "G", "G"], ["O", "O", "O"],]
                        ),  # Right
                        CubeFace(
                            [["R", "R", "R"], ["R", "R", "R"], ["G", "G", "G"],]
                        ),  # Back
                        CubeFace(
                            [["B", "B", "B"], ["B", "B", "B"], ["R", "R", "R"],]
                        ),  # Left
                        CubeFace(
                            [["W", "W", "W"], ["W", "W", "W"], ["W", "W", "W"],]
                        ),  # Top
                        CubeFace(
                            [["Y", "Y", "Y"], ["Y", "Y", "Y"], ["Y", "Y", "Y"],]
                        ),  # Bottom
                    ]
                ),
            ),
            (
                FaceRef.D,
                2,
                Cube(
                    *[  # type: ignore
                        CubeFace(
                            [["O", "O", "O"], ["O", "O", "O"], ["R", "R", "R"],]
                        ),  # Front
                        CubeFace(
                            [["G", "G", "G"], ["G", "G", "G"], ["B", "B", "B"],]
                        ),  # Right
                        CubeFace(
                            [["R", "R", "R"], ["R", "R", "R"], ["O", "O", "O"],]
                        ),  # Back
                        CubeFace(
                            [["B", "B", "B"], ["B", "B", "B"], ["G", "G", "G"],]
                        ),  # Left
                        CubeFace(
                            [["W", "W", "W"], ["W", "W", "W"], ["W", "W", "W"],]
                        ),  # Top
                        CubeFace(
                            [["Y", "Y", "Y"], ["Y", "Y", "Y"], ["Y", "Y", "Y"],]
                        ),  # Bottom
                    ]
                ),
            ),
            (
                FaceRef.D,
                3,
                Cube(
                    *[  # type: ignore
                        CubeFace(
                            [["O", "O", "O"], ["O", "O", "O"], ["G", "G", "G"],]
                        ),  # Front
                        CubeFace(
                            [["G", "G", "G"], ["G", "G", "G"], ["R", "R", "R"],]
                        ),  # Right
                        CubeFace(
                            [["R", "R", "R"], ["R", "R", "R"], ["B", "B", "B"],]
                        ),  # Back
                        CubeFace(
                            [["B", "B", "B"], ["B", "B", "B"], ["O", "O", "O"],]
                        ),  # Left
                        CubeFace(
                            [["W", "W", "W"], ["W", "W", "W"], ["W", "W", "W"],]
                        ),  # Top
                        CubeFace(
                            [["Y", "Y", "Y"], ["Y", "Y", "Y"], ["Y", "Y", "Y"],]
                        ),  # Bottom
                    ]
                ),
            ),
        ),
        ids=(
            "Right - 1 step",
            "Right - 2 steps",
            "Right - 3 steps",
            "Back - 1 step",
            "Back - 2 steps",
            "Back - 3 steps",
            "Left - 1 step",
            "Left - 2 steps",
            "Left - 3 steps",
            "Top - 1 step",
            "Top - 2 steps",
            "Top - 3 steps",
            "Bottom - 1 step",
            "Bottom - 2 steps",
            "Bottom - 3 steps",
        ),
    )
    def test_right_face_layer_rotation(self, face_ref, steps, expected):
        initial_cube = Cube(*initial_cube_state)
        rotated = initial_cube.rotate_layer(face_ref, steps)
        assert rotated == expected

    @pytest.mark.parametrize(
        "other, expected",
        (
            (
                Cube(
                    *[  # type: ignore
                        CubeFace([["O", "O", "O"], ["O", "O", "O"], ["O", "O", "O"],]),
                        CubeFace([["G", "G", "G"], ["G", "G", "G"], ["G", "G", "G"],]),
                        CubeFace([["R", "R", "R"], ["R", "R", "R"], ["R", "R", "R"],]),
                        CubeFace([["B", "B", "B"], ["B", "B", "B"], ["B", "B", "B"],]),
                        CubeFace([["W", "W", "W"], ["W", "W", "W"], ["W", "W", "W"],]),
                        CubeFace([["Y", "Y", "Y"], ["Y", "Y", "Y"], ["Y", "Y", "Y"],]),
                    ],
                ),
                True,
            ),
            (
                Cube(
                    *[  # type: ignore
                        CubeFace([["*", "*", "*"], ["*", "*", "*"], ["*", "*", "*"],]),
                        CubeFace([["*", "*", "*"], ["*", "*", "*"], ["*", "*", "*"],]),
                        CubeFace([["*", "*", "*"], ["*", "*", "*"], ["*", "*", "*"],]),
                        CubeFace([["*", "*", "*"], ["*", "*", "*"], ["*", "*", "*"],]),
                        CubeFace([["*", "*", "*"], ["*", "*", "*"], ["*", "*", "*"],]),
                        CubeFace([["*", "*", "*"], ["*", "*", "*"], ["*", "*", "*"],]),
                    ],
                ),
                True,
            ),
            (
                Cube(
                    *[  # type: ignore
                        CubeFace([["*", "*", "*"], ["O", "O", "O"], ["O", "O", "O"],]),
                        CubeFace([["G", "G", "G"], ["*", "*", "*"], ["G", "G", "G"],]),
                        CubeFace([["R", "R", "R"], ["R", "R", "R"], ["*", "*", "*"],]),
                        CubeFace([["B", "B", "B"], ["*", "*", "*"], ["B", "B", "B"],]),
                        CubeFace([["*", "*", "*"], ["W", "W", "W"], ["W", "W", "W"],]),
                        CubeFace([["Y", "Y", "Y"], ["*", "*", "*"], ["Y", "Y", "Y"],]),
                    ],
                ),
                True,
            ),
            (
                Cube(
                    *[  # type: ignore
                        CubeFace([["*", "*", "*"], ["O", "O", "O"], ["O", "O", "O"],]),
                        CubeFace([["G", "G", "G"], ["*", "*", "*"], ["G", "G", "G"],]),
                        CubeFace([["Z", "R", "R"], ["R", "R", "R"], ["*", "*", "*"],]),
                        CubeFace([["B", "B", "B"], ["*", "*", "*"], ["B", "B", "B"],]),
                        CubeFace([["*", "*", "*"], ["W", "W", "W"], ["W", "W", "W"],]),
                        CubeFace([["Y", "Y", "Y"], ["*", "*", "*"], ["Y", "Y", "Y"],]),
                    ],
                ),
                False,
            ),
            (
                Cube(
                    *[  # type: ignore
                        CubeFace([["Z", "*", "*"], ["O", "O", "O"], ["O", "O", "O"],]),
                        CubeFace([["G", "G", "G"], ["*", "*", "*"], ["G", "G", "G"],]),
                        CubeFace([["R", "R", "R"], ["R", "R", "R"], ["*", "*", "*"],]),
                        CubeFace([["B", "B", "B"], ["*", "*", "*"], ["B", "B", "B"],]),
                        CubeFace([["*", "*", "*"], ["W", "W", "W"], ["W", "W", "W"],]),
                        CubeFace([["Y", "Y", "Y"], ["*", "*", "*"], ["Y", "Y", "Y"],]),
                    ],
                ),
                False,
            ),
            (
                Cube(
                    *[  # type: ignore
                        CubeFace([["*", "*", "*"], ["O", "O", "O"], ["O", "O", "O"],]),
                        CubeFace([["G", "G", "G"], ["*", "*", "*"], ["G", "Z", "G"],]),
                        CubeFace([["R", "R", "R"], ["R", "R", "R"], ["*", "*", "*"],]),
                        CubeFace([["B", "B", "B"], ["*", "*", "*"], ["B", "B", "B"],]),
                        CubeFace([["*", "*", "*"], ["W", "W", "W"], ["W", "W", "W"],]),
                        CubeFace([["Y", "Y", "Y"], ["*", "*", "*"], ["Y", "Y", "Y"],]),
                    ],
                ),
                False,
            ),
            (
                Cube(
                    *[  # type: ignore
                        CubeFace([["*", "*", "*"], ["O", "O", "O"], ["O", "O", "O"],]),
                        CubeFace([["G", "G", "G"], ["*", "*", "*"], ["G", "G", "G"],]),
                        CubeFace([["R", "R", "R"], ["R", "R", "R"], ["*", "*", "*"],]),
                        CubeFace([["B", "B", "B"], ["*", "*", "Z"], ["B", "B", "B"],]),
                        CubeFace([["*", "*", "*"], ["W", "W", "W"], ["W", "W", "W"],]),
                        CubeFace([["Y", "Y", "Y"], ["*", "*", "*"], ["Y", "Y", "Y"],]),
                    ],
                ),
                False,
            ),
            (
                Cube(
                    *[  # type: ignore
                        CubeFace([["*", "*", "*"], ["O", "O", "O"], ["O", "O", "O"],]),
                        CubeFace([["G", "G", "G"], ["*", "*", "*"], ["G", "G", "G"],]),
                        CubeFace([["R", "R", "R"], ["R", "R", "R"], ["*", "*", "*"],]),
                        CubeFace([["B", "B", "B"], ["*", "*", "*"], ["B", "B", "B"],]),
                        CubeFace([["*", "Z", "*"], ["W", "W", "W"], ["W", "W", "W"],]),
                        CubeFace([["Y", "Y", "Y"], ["*", "*", "*"], ["Y", "Y", "Y"],]),
                    ],
                ),
                False,
            ),
            (
                Cube(
                    *[  # type: ignore
                        CubeFace([["*", "*", "*"], ["O", "O", "O"], ["O", "O", "O"],]),
                        CubeFace([["G", "G", "G"], ["*", "*", "*"], ["G", "G", "G"],]),
                        CubeFace([["R", "R", "R"], ["R", "R", "R"], ["*", "*", "*"],]),
                        CubeFace([["B", "B", "B"], ["*", "*", "*"], ["B", "B", "B"],]),
                        CubeFace([["*", "*", "*"], ["W", "W", "W"], ["W", "W", "W"],]),
                        CubeFace([["Y", "Y", "Y"], ["*", "*", "*"], ["Z", "Y", "Y"],]),
                    ],
                ),
                False,
            ),
        ),
        ids=(
            "Identical",
            "All wildcards",
            "Partial match",
            "Non-matching back",
            "Non-matching front",
            "Non-matching right",
            "Non-matching left",
            "Non-matching top",
            "Non-matching bottom",
        ),
    )
    def test_fuzzy_match(self, other, expected):
        cube = Cube(*initial_cube_state)
        assert cube.fuzzy_match(other) is expected

    def test_successors(self):
        """There should be 18 successor cubes from the initial state."""
        cube = Cube(*initial_cube_state)
        successors = list(cube.successors())
        assert len(successors) == 18

        # None of the successors should be the same as another
        for successor in successors:
            for comparator in successors:
                if successor is comparator:
                    continue
                assert successor != comparator

        # The successors should produce fewer moves as moves from the same face are
        # ignored
        successor = successors[0]
        successors = list(successor.successors())
        assert len(successors) == 15
