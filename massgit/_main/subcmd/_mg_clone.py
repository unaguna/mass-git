from ._cmn import SubCmd


class MgCloneCmd(SubCmd):
    def name(self) -> str:
        return "mg-clone"

    def help(self) -> str:
        return "Clone defined repos"
