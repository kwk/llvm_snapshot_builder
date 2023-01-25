"""
CoprActionBuildAllPackages
"""

import logging
from typing import Union
from ..mixins.package_builder_mixin import CoprPackageBuilderMixin
from ..mixins.client_mixin import CoprClientMixin
from .action import CoprAction
from .create_project import CoprActionCreateProject
from ..copr_project_ref import CoprProjectRef


class CoprActionBuildAllPackages(
        CoprClientMixin,
        CoprPackageBuilderMixin,
        CoprAction):
    """
    Builds everyting for the given chroots and creates optimal Copr batches.
    See https://docs.pagure.org/copr.copr/user_documentation.html#build-batches.

    NOTE: We kick-off builds for each chroot individually so that an x86_64 build
    doesn't have to wait for a potentially slower s390x build.
    """

    def __init__(
            self,
            proj: Union[CoprProjectRef, str],
            chroots: list[str] = None,
            timeout: int = None,
            without_tests:bool = True,
            ** kwargs):
        """
        Initializes the action.

        Args:
            proj (Union[CoprProjectRef, str]): the Copr project to use
            chroots (list): Chroots to build in. Defaults to default chroots from CoprActionMakeOrEditProject.
            timeout (int): the number of seconds until to timeout the individual builds
            without_tests (bool): will add --without=check to the mock chroot (default: False)
        """
        if len(chroots) == 0:
            logging.info(f"no chroots given, using default chroots {CoprActionCreateProject.default_chroots}")
            chroots = CoprActionCreateProject.default_chroots
        self.__chroots = chroots
        self.__proj = CoprProjectRef(proj)
        self.__timeout = timeout
        self.__without_tests = without_tests
        super().__init__(**kwargs)

    def run(self) -> bool:
        """ Runs the action. """

        # pylint: disable=invalid-name
        for chroot in self.__chroots:
            without_options = None
            with_options = "snapshot_build"
            if self.__without_tests:
                without_options = "tests"
            self.adjust_chroot(
                proj=self.__proj,
                chroot=chroot,
                with_options=with_options,
                without_options=without_options)
            params = {
                "proj": self.__proj,
                "chroots": [chroot],
                "timeout": self.__timeout,
            }
            logging.info(f"build all packages in chroot: {chroot}")
            python_lit_build = self.build(package_name="python-lit", **params)
            llvm_build = self.build(package_name="llvm", build_after_id=python_lit_build.id, **params)
            self.build(package_name="lld", build_after_id=llvm_build.id, **params)
            self.build(package_name="mlir", build_after_id=llvm_build.id, **params)
            clang_build = self.build(package_name="clang", **params, build_after_id=llvm_build.id)
            self.build(package_name="libomp", build_after_id=clang_build.id, **params)
            self.build(package_name="compiler-rt", build_after_id=clang_build.id,**params)
        # pylint: enable=invalid-name
        return True
