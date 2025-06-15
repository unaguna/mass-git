from ._cmn import SubCmd


class MgInitCmd(SubCmd):
    def name(self) -> str:
        return "mg-init"

    def help(self) -> str:
        return "Initialize massgit"
