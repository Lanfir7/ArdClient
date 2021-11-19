class Gateway(object):
    def __init__(self, gateway):
        self.__gateway = gateway

    def ui(self):
        return self.__gateway.jvm.haven.purus.pbot.PBotAPI.ui()

    def pbotutils(self):
        return self.__gateway.jvm.haven.purus.pbot.PBotUtils


class Script:
    def run(self, gateway: Gateway, ScriptID, gvar):
        self.gateway = Gateway(gateway)
        gvar.skinBol = False
        gvar.cleanBol = False
        gvar.butcherBol = False
        gvar.boneBol = False
        window = self.gateway.pbotutils().PBotWindow(self.gateway.ui(), "Butcher", 110, 110, ScriptID)
        skinCheck = window.addCheckbox("skin", "Skin", gvar.skinBol, 5, 5)
        cleanCheck = window.addCheckbox("btnClick", "Clean", gvar.cleanBol, 5, 25)
        butcherCheck = window.addCheckbox("btnClick", "Butcher", gvar.butcherBol, 5, 45)
        boneCheck = window.addCheckbox("btnClick", "Collect bones", gvar.boneBol, 5, 65)
        start = window.addButton("btnClick", "Start", 100, 5, 85)


    def btnClick(self, gateway, ScriptID, gvar):
        self.ui = gateway.jvm.haven.purus.pbot.PBotAPI.ui()
        self.pbotutils = gateway.jvm.haven.purus.pbot.PBotUtils
        self.pbotutils.sysMsg(self.ui, "Skin {}".format(gvar.skinBol))

    def skin(self, gateway, ScriptID, gvar):
        if not gvar.skinBol:
            gvar.skinBol = True
        else:
            gvar.skinBol = False
        self.ui = gateway.jvm.haven.purus.pbot.PBotAPI.ui()
        self.pbotutils = gateway.jvm.haven.purus.pbot.PBotUtils
        self.pbotutils.sysMsg(self.ui, "Skin {}".format(gvar.skinBol))