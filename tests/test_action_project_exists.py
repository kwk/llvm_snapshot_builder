""" Tests for llvm_snapshot_builder """

import unittest
import uuid
from llvm_snapshot_builder.actions.project_exists import CoprActionProjectExists


class TestCoprActionProjectExists(unittest.TestCase):
    """ Testcases for the CoprActionProjectExists class. """

    def test_not_existing_project(self):
        """ Test that a non-existing project is detected as such. """
        action = CoprActionProjectExists(f"@copr/{uuid.uuid4()}")
        self.assertFalse(action.run())

    def test_existing_project(self):
        """ Test that @copr/copr project can be found. """
        action = CoprActionProjectExists("@copr/copr")
        self.assertTrue(action.run())


if __name__ == '__main__':
    unittest.main()
