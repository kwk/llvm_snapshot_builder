""" Tests for llvm_snapshot_builder """

import unittest
from llvm_snapshot_builder import CoprProjectRef


class TestCoprProjectRef(unittest.TestCase):
    """ Testcases for the CoprProjectRef class. """

    def test_ctor_with_string(self):
        """ Test that creation with a string works. """
        ref = CoprProjectRef("foo/bar")
        self.assertEqual(ref.owner, "foo")
        self.assertEqual(ref.name, "bar")
        self.assertEqual(str(ref), "foo/bar")

    def test_ctor_with_ref(self):
        """ Test that creation from another ref works. """
        orig = CoprProjectRef("foo/bar")
        ref = CoprProjectRef(orig)
        self.assertEqual(ref.owner, "foo")
        self.assertEqual(ref.name, "bar")
        self.assertEqual(str(ref), "foo/bar")


if __name__ == '__main__':
    unittest.main()
