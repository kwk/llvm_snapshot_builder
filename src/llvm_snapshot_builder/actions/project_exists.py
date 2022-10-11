"""
CoprActionProjectExists
"""

from copr.v3 import CoprNoResultException
from ..mixins.client_mixin import CoprClientMixin
from ..copr_project_ref import CoprProjectRef
from .action import CoprAction


class CoprActionProjectExists(CoprAction, CoprClientMixin):
    """ Checks if a project exists. """

    def __init__(self, proj: CoprProjectRef, **kwargs):
        """
        Initialize the action.

        Args:
            proj (CoprProjectRef): project to check
        """
        self.__proj = proj
        super().__init__(**kwargs)

    def run(self) -> bool:
        """ Runs the action. """
        try:
            self.client.project_proxy.get(self.__proj.owner, self.__proj.name)
        except CoprNoResultException:
            print("no")
            return False
        print("yes")
        return True