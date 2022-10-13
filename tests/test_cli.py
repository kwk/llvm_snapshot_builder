""" Tests for llvm_snapshot_builder.cli """

import unittest
import uuid
import io
import contextlib
from contextlib import contextmanager
from tempfile import NamedTemporaryFile
from llvm_snapshot_builder.mixins.client_mixin import CoprClientMixin
from llvm_snapshot_builder.cli import main
from llvm_snapshot_builder import __version__
from llvm_snapshot_builder.cli import CMD_BUILD_PACKAGES, CMD_CANCEL_BUILDS, \
    CMD_CREATE_PACKAGES, CMD_CREATE_PROJECT, CMD_DELETE_PROJECT, CMD_PROJECT_EXISTS, \
    CMD_BUILD_ALL_PACKAGES

# TODO(kwk): Implement recipe tests as I did in Golang for fabric8-wit


class TestCLI(unittest.TestCase):
    """ Testcases for the CLI program shipping with this library. """

    def setUp(self) -> None:
        self.owner = CoprClientMixin().client.config["username"]

    @contextmanager
    def get_text_file(self, text: str) -> str:
        """
        Returns a temporary filename with the given text written to it.
        Use this as a context manager:

            with self.get_text_file(text="foo") as filename:
        """
        file_handle = NamedTemporaryFile(mode="w+", encoding="utf-8")
        file_handle.writelines(text)
        file_handle.flush()
        try:
            yield file_handle.name
        finally:
            file_handle.close()

    def test_project_exists(self):
        """ Test project-exists command. """
        self.assertTrue(main([CMD_PROJECT_EXISTS, "--proj", "@copr/copr"]))
        self.assertFalse(
            main([CMD_PROJECT_EXISTS, "--proj", f"@copr/{uuid.uuid4()}"]))

    def test_version(self):
        """ Test version flag command. """
        buf = io.StringIO()
        with self.assertRaises(SystemExit) as ex, contextlib.redirect_stdout(buf):
            main(["--version"])
        self.assertEqual(ex.exception.code, 0)
        self.assertEqual(
            f"llvm_snapshot_builder {__version__}\n",
            buf.getvalue())

    def test_create_project_ok(self):
        """ Test create-project command. """
        ref = f"{self.owner}/{uuid.uuid4()}"
        self.assertFalse(main([CMD_PROJECT_EXISTS, "--proj", ref]))

        with self.get_text_file(text="foobar description") as description:
            with self.get_text_file(text="foobar instructions") as instructions:
                self.assertTrue(
                    main([CMD_CREATE_PROJECT,
                          "--proj", ref,
                          "--description-file", description,
                          "--instructions-file", instructions,
                          "--delete-after-days", "0"]))

        self.assertTrue(main([CMD_PROJECT_EXISTS, "--proj", ref]))
        self.assertTrue(main([CMD_DELETE_PROJECT, "--proj", ref]))
        self.assertFalse(main([CMD_PROJECT_EXISTS, "--proj", ref]))

    def test_create_project_with_update(self):
        """ Test create-project command. """
        ref = f"{self.owner}/{uuid.uuid4()}"
        self.assertFalse(main([CMD_PROJECT_EXISTS, "--proj", ref]))

        with self.get_text_file(text="foobar description") as description:
            with self.get_text_file(text="foobar instructions") as instructions:
                self.assertTrue(
                    main([CMD_CREATE_PROJECT,
                          "--proj", ref,
                          "--description-file", description,
                          "--instructions-file", instructions,
                          "--delete-after-days", "0"]))

        self.assertTrue(main([CMD_PROJECT_EXISTS, "--proj", ref]))
        self.assertTrue(main([CMD_DELETE_PROJECT, "--proj", ref]))
        self.assertFalse(main([CMD_PROJECT_EXISTS, "--proj", ref]))

    def test_create_and_build_packages(self):
        """ Tests create-packages and build-packages commands. """
        ref = f"{self.owner}/{uuid.uuid4()}"
        self.assertFalse(main([CMD_PROJECT_EXISTS, "--proj", ref]))
        self.assertTrue(main([CMD_CREATE_PROJECT, "--proj", ref]))
        self.assertTrue(main([CMD_PROJECT_EXISTS, "--proj", ref]))
        self.assertTrue(
            main([CMD_CREATE_PACKAGES, "--proj", ref, "--packagenames", "llvm"]))
        with self.assertLogs(level='WARNING') as ctxmgr:
            # this should write a warning to the log because the package already
            # exists but is not updated due to the absence of --update.
            self.assertTrue(
                main([CMD_CREATE_PACKAGES, "--proj", ref, "--packagenames", "llvm"]))
        self.assertEqual(
            ctxmgr.output,
            ['WARNING:root:package already exists and is not updated: llvm'])
        # TODO(kwk): Test this when building with Python 3.10
        #            See https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertNoLogs
        # with self.assertNoLogs(level='WARNING'):
        #     self.assertTrue(
        # main([CMD_CREATE_PACKAGES, "--proj", ref, "--packagenames", "llvm",
        # "--update"]))
        self.assertTrue(
            main(["--debug", CMD_BUILD_PACKAGES, "--proj", ref, "--packagenames", "llvm"]))
        self.assertTrue(main([CMD_CANCEL_BUILDS, "--proj", ref]))
        self.assertTrue(main([CMD_DELETE_PROJECT, "--proj", ref]))
        self.assertFalse(main([CMD_PROJECT_EXISTS, "--proj", ref]))

    def test_create_and_build_all_packages(self):
        """ Tests create-packages and build-all-packages commands. """
        ref = f"{self.owner}/{uuid.uuid4()}"
        self.assertTrue(main([CMD_CREATE_PROJECT, "--proj", ref]))
        self.assertTrue(main([CMD_CREATE_PACKAGES, "--proj", ref]))
        self.assertTrue(main(["--debug", CMD_BUILD_ALL_PACKAGES, "--proj", ref]))
        self.assertTrue(main([CMD_CANCEL_BUILDS, "--proj", ref]))
        self.assertTrue(main([CMD_DELETE_PROJECT, "--proj", ref]))


if __name__ == '__main__':
    unittest.main()
