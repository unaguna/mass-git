from ._cmn import SubCmd


class MgLsReposCmd(SubCmd):
    def name(self) -> str:
        return "mg-ls-repos"

    def help(self) -> str:
        return "Show information about repos"
