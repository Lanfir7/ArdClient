import itertools
from typing import Optional
import sys, os, threading, time
from __py_api.PBotWindow import PBotWindow
from __py_api.PBotInventory import PBotInventory
from __py_api.PBotWindowAPI import PBotWindowAPI
from __py_api.PBotCharacterAPI import PBotCharacterAPI
from __py_api.PBotUtils import PBotUtils
from __py_api.PBotGobAPI import PBotGobAPI
from __py_api.variables import Vars

class Script(Vars):
    def getWInv(self, wnd: PBotWindow) -> Optional[PBotInventory]:
        if wnd != None:
            inv = wnd.get_inventories()
            if len(inv) > 0:
                return inv[0]
        return None

    def run(self):
        self.PBotUtils = PBotUtils(self.gw, self.ui)
        self.PBotGobAPI = PBotGobAPI(self.gw, self.ui)
        self.PBotWindowAPI = PBotWindowAPI(self.gw, self.ui)
        self.PBotCharacterAPI = PBotCharacterAPI(self.gw, self.ui)
        self.player = self.PBotGobAPI.get_player()
        barrel = self.PBotGobAPI.select_gob()
        # barrel = self.PBotGobAPI.get_closest_gob_by_resname("barrel")
        items = self.PBotUtils.player_inventory().get_inventory_items()
        self.PBotUtils.sys_msg("start {}".format(items))
        invs = [self.PBotUtils.player_inventory(), self.getWInv(self.PBotWindowAPI.get_window("Belt"))]
        for inv in filter(None, invs):
            for itm in filter(lambda x: x != None and str(x.get_contents_name()).endswith("Tea"), itertools.chain(inv.get_inventory_items_by_resnames(".*"), self.PBotCharacterAPI.get_equipment())):
                # itm.activate_item()
                # itm.take_item()
                itm.take_item()
                locat = itm.get_inv_loc()
                self.PBotUtils.sys_msg("Взял {}".format(locat))
                # itm.itemact()
                time.sleep(0.2)
                barrel.item_click(0)
                # sess.PBotUtils.sys_msg("Слил")
                time.sleep(0.2)

                if locat[0] > 9:
                    locat_x = locat[0]-2
                elif locat[0] > 4:
                    locat_x = locat[0]-1
                else:
                    locat_x = locat[0]
                self.PBotUtils.sys_msg("Взял {}".format(locat_x))

                if locat[1] > 9:
                    locat_y = locat[1]-5
                elif locat[1] > 4:
                    locat_y = locat[1]-1
                else:
                    locat_y = locat[1]
                inv.drop_item_to_inventory(locat_x, locat_y)
                # sess.PBotUtils.sys_msg("Положил")
                time.sleep(0.2)


