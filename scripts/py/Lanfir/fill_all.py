import itertools
import time
from __pbot.PBotSession import PBotSession
from __pbot.PBotWindow import PBotWindow
from __pbot.PBotInventory import PBotInventory
from typing import Optional
#Forage script v1.0 by Frostz

#Randomly walks around, searches and picks up herbs avoiding aggressive mobs
#Change to crawl speed to stop the script

class Script:
    def run(self, sess: PBotSession):
        self.session = sess
        self._PBotGobAPI = sess.PBotGobAPI
        self._PBotCharacterAPI = sess.PBotCharacterAPI
        self._PBotUtils = sess.PBotUtils
        self._PBotWindowAPI = sess.PBotWindowAPI
        self.player = sess.PBotGobAPI.get_player()

        self._PBotUtils.select_area(self.cb)


    def cb(self, a, b):
        # Chop trees
        trees = 0
        stumps = 0
        self.session.PBotUtils.sys_msg("start {} {}".format(a, b))
        for gob in self._PBotGobAPI.gobs_in_area(*a, *b):
            resname = gob.get_resname()
            if resname.startswith("gfx/terobjs/ttub"):
                continue
            else:
                if self._PBotGobAPI.find_gob_by_id(gob.get_id()) == None:
                    continue
                gob.pf_click(3, 0)
                time.sleep(0.5)
                while self.player.is_moving():
                    time.sleep(0.5)
                wnd_name = gob.window_name_for_gob()
                wnd = self._PBotWindowAPI.get_window(wnd_name, 1000*5)
                invs = wnd.get_inventories()
                if len(invs) < 1:
                    return
                for x in range(invs[0].free_slots()):
                    invs[0].xfer_to()
        #         menu = self._PBotUtils.get_flowermenu(1000*30)
        #         if menu == None:
        #             self._PBotCharacterAPI.msg_to_chat("Area Chat", "Flowermenu timeout!")
        #             continue
        #         menu.choose_petal("Chop")
        #         timeout = time.time()
        #         while self._PBotGobAPI.find_gob_by_id(gob.get_id()) != None:
        #             time.sleep(0.5)
        #             if self._PBotCharacterAPI.get_stamina() < 70:
        #                 self.drink()
        #
        #             if timeout-time.time() > 30:
        #                 self._PBotCharacterAPI.msg_to_chat("Area Chat", "Timeout exceeded! Stopping, probably ran out of water")
        #                 return
        #         trees += 1
        # # Remove stumps
        # for gob in self._PBotGobAPI.gobs_in_area(*a, *b):
        #     if self._PBotCharacterAPI.get_energy() < 30:
        #         self._PBotCharacterAPI.msg_to_chat("Area Chat", "Energy is too low, stopping!")
        #         return
        #     resname = gob.get_resname()
        #     if not resname.startswith("gfx/terobjs/trees/") or not resname.endswith("stump"):
        #         continue
        #     else:
        #         if self._PBotGobAPI.find_gob_by_id(gob.get_id()) == None:
        #             continue
        #         self._PBotCharacterAPI.do_act(list(["destroy"]))
        #         gob.pf_click()
        #         timeout = time.time()
        #         while self._PBotGobAPI.find_gob_by_id(gob.get_id()) != None:
        #             time.sleep(0.5)
        #             if self._PBotCharacterAPI.get_stamina() < 70:
        #                 self.drink()
        #
        #             if timeout-time.time() > 60:
        #                 self._PBotCharacterAPI.msg_to_chat("Area Chat", "Timeout exceeded! Stopping, probably ran out of water")
        #                 return
        #         stumps += 1
        # self._PBotCharacterAPI.msg_to_chat("Area Chat", "Finished. Got rid of {} trees and {} stumps".format(trees, stumps))