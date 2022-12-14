""" Tests for llvm_snapshot_builder """

import unittest
import uuid
from copr.v3.exceptions import CoprNoResultException
from llvm_snapshot_builder.actions.create_project import CoprActionCreateProject
from llvm_snapshot_builder.mixins.client_mixin import CoprClientMixin
from llvm_snapshot_builder.actions.delete_project import CoprActionDeleteProject
from llvm_snapshot_builder.copr_project_ref import CoprProjectRef
from llvm_snapshot_builder.actions.project_exists import CoprActionProjectExists


class TestCoprActionCreateProject(unittest.TestCase):
    """ Testcases for the CoprActionProjectExists class. """

    @property
    def owner(self):
        """ Returns the proper Copr owner for the test. """
        return CoprClientMixin().client.config["username"]

    def test_create_no_such_user(self):
        """ Test that we cannot create project under a non-existend user. """
        owner = uuid.uuid4()
        # TODO(kwk): Do we want to throw an exception or return False?
        # TODO(kwk): I'd say we throw it but allow utils to catch it.
        with self.assertRaises(CoprNoResultException) as ex:
            self.assertFalse( CoprActionCreateProject(proj=f"{owner}/copr").run())
        self.assertEqual(str(ex.exception), f"No such user `{owner}'")

    def test_create_ok(self):
        """ Test that we can create a new project and delete it. """
        ref = CoprProjectRef(f"{self.owner}/{uuid.uuid4()}")
        try:
            self.assertTrue(CoprActionCreateProject(proj=ref).run())
            self.assertTrue(CoprActionProjectExists(proj=ref).run())
        finally:
            CoprActionDeleteProject(proj=ref).run()
            self.assertFalse(CoprActionProjectExists(proj=ref).run())


if __name__ == '__main__':
    unittest.main()
