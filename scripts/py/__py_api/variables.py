class Vars:
    def __init__(self, scriptid, gw):
        self.scriptid = scriptid
        self.gw = gw
        self.ui = self.ui()
        #
        # self.pbotutils = self.gw.jvm.haven.purus.pbot.PBotUtils

    def PBotAPI(self):
        return self.gw.jvm.haven.purus.pbot.PBotAPI

    # current ui
    def ui(self):
        return self.PBotAPI().ui()
    #
    # def uis(self):
    #     return self.PBotAPI().uis()
    #
    # def Utils(self):
    #     return self.gw.jvm.haven.purus.pbot.PBotUtils
    #
    # def sys_msg(self, text):
    #     self.gw.jvm.haven.purus.pbot.PBotUtils.sysMsg(self.ui, text)
    #
    # def CharacterAPI(self):
    #     return self.gw.jvm.haven.purus.pbot.PBotCharacterAPI
    #
    # def Discord(self):
    #     return self.gw.jvm.haven.purus.pbot.PBotDiscord
    #
    # def GobAPI(self):
    #     return self.gw.jvm.haven.purus.pbot.PBotGobAPI
    #
    # def WindowAPI(self):
    #     return self.gw.jvm.haven.purus.pbot.PBotWindowAPI
