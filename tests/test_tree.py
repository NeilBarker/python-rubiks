from unittest.mock import Mock
import weakref

from py_rubiks.tree import Node


class TestNode:
    def test_depth(self):
        # Test root
        root = Node(Mock())
        assert root.depth == 0

        # Add successive layers
        parent = root
        for depth in range(1, 11):
            first_child = Node(Mock())
            parent.add(first_child)
            assert first_child.depth == depth

            second_child = Node(Mock())
            parent.add(second_child)
            assert second_child.depth == depth

            parent = first_child

    def test_backtrace_for_root_returns_empty_list(self):
        root = Node(Mock())
        assert root.backtrace() == []

    def test_backtrace_produces_correct_path_for_tree(self):
        root = Node(Mock())

        # Add successive layers
        expected_path = []
        parent = root
        for _ in range(1, 11):
            first_child = Node(Mock())
            parent.add(first_child)

            expected_path.append(first_child)

            second_child = Node(Mock())
            parent.add(second_child)

            parent = first_child

        expected_path.reverse()  # Start from the leaf
        assert parent.backtrace() == expected_path

    def test_references(self):
        """Test that when the reference to the parent is deleted, the child is gc'd."""
        # Setup tree
        parent = Node(Mock())
        child = Node(Mock())
        parent.add(child)

        # Drop strong references to child
        was_deleted = Mock()
        weakref.finalize(child, was_deleted, "child deleted")
        parent.children = []
        child = None

        was_deleted.assert_called_once_with("child deleted")

    def test_delete(self):
        # Setup tree
        parent = Node(Mock())
        child = Node(Mock())
        parent.add(child)
        child.add(Node(Mock()))
        assert len(child.children) == 1

        was_deleted = Mock()
        weakref.finalize(child, was_deleted, "child deleted")

        child.delete()
        assert len(child.children) == 0
        child = None

        was_deleted.assert_called_once_with("child deleted")
        assert len(parent.children) == 0
