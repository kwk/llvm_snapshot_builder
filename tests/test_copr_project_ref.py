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

    def test_ctor_invalid_owner_project(self):
        """ Test that creation with an invalid owner fails. """
        with self.assertRaises(ValueError) as ex:
            CoprProjectRef("foo")
        self.assertEqual(str(ex.exception),
                         "not enough values to unpack (expected 2, got 1)")

    def test_ctor_empty_owner_and_project(self):
        """ Test that creation with an empty owner and project fails. """
        with self.assertRaises(ValueError) as ex:
            CoprProjectRef("/")
        self.assertEqual(str(ex.exception), "ownername MUST NOT be empty")

    def test_ctor_empty_project(self):
        """ Test that creation with an empty project fails. """
        with self.assertRaises(ValueError) as ex:
            CoprProjectRef("foo/")
        self.assertEqual(str(ex.exception), "projectname MUST NOT be empty")

    def test_ctor_empty_ownername(self):
        """ Test that creation with an empty ownername fails. """
        with self.assertRaises(ValueError) as ex:
            CoprProjectRef("/bar")
        self.assertEqual(str(ex.exception), "ownername MUST NOT be empty")

    def test_ctor_with_ref_object(self):
        """ Test that creation from another CoprProjectRef object works. """
        orig = CoprProjectRef("foo/bar")
        ref = CoprProjectRef(orig)
        self.assertEqual(ref.owner, orig.owner)
        self.assertEqual(ref.name, orig.name)
        self.assertEqual(str(ref), f"{orig.owner}/{orig.name}")

    def test_ref_property(self):
        """ Test the ref property works. """
        orig = CoprProjectRef("foo/bar")
        self.assertEqual(orig.ref, "foo/bar")


if __name__ == '__main__':
    unittest.main()
