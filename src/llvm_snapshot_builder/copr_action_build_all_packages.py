"""
CoprActionBuildAllPackages
"""

from .copr_package_builder_mixin import CoprPackageBuilderMixin
from .copr_client_mixin import CoprClientMixin
from .copr_action import CoprAction
from .copr_action_make_or_edit_project import CoprActionMakeOrEditProject
from .copr_project_ref import CoprProjectRef


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
            proj: CoprProjectRef,
            chroots: list[str] = None,
            ** kwargs):
        """ Initializes the action. """
        if chroots is None:
            chroots = CoprActionMakeOrEditProject.default_chroots
        self.__chroots = chroots
        self.__proj = proj
        super().__init__(**kwargs)

    def run(self) -> bool:
        """ Runs the action. """

        p = self.__proj
        for chroot in self.__chroots:
            print(f"CHROOT: {chroot}")
            python_lit_build = self.build(p, "python-lit", [chroot])
            llvm_build = self.build(p, "llvm", [chroot], python_lit_build.id)
            self.build(p, "lld", [chroot], llvm_build.id)
            self.build(p, "mlir", [chroot], llvm_build.id)
            clang_build = self.build(p, "clang", [chroot], llvm_build.id)
            self.build(p, "libomp", [chroot], clang_build.id)
            self.build(p, "compiler-rt", [chroot], llvm_build.id)
        return True
