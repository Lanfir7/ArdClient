import itertools
from typing import Optional
from __pbot.PBotSession import PBotSession
from __pbot.PBotWindow import PBotWindow
from __pbot.PBotInventory import PBotInventory
from __pbot.PBotItem import PBotItem
from __pbot.PBotGob import PBotGob
from __pbot.PBotSession import PBotSession
from __pbot.PBotUtils import PBotUtils
from __pbot.PBotCharacterAPI import PBotCharacterAPI
import sys, os, threading, time

class Script:
    area = None
    cb_gob: PBotGob = None
    cb_ok = threading.Event()
    water_in_cauldron = False
    player_start = []
    count_all_tea_pods = 0
    stockpile_of_tea = False

    def getWInv(self, wnd: PBotWindow) -> Optional[PBotInventory]:
        if wnd != None:
            inv = wnd.get_inventories()
            if len(inv) > 0:
                return inv[0]
        return None

    def run(self, sess: PBotSession):
        self.session = sess
        self._PBotGobAPI = sess.PBotGobAPI
        self._PBotCharacterAPI = sess.PBotCharacterAPI
        self._PBotUtils = sess.PBotUtils
        self._PBotWindowAPI = sess.PBotWindowAPI
        self.player = sess.PBotGobAPI.get_player()

        inv = self._PBotUtils.player_inventory()
        for itm in inv.get_inventory_items_by_resnames("lib/layspr"):
            self.count_all_tea_pods += 1
        self.player_start = self.player.get_coords()
        self._PBotUtils.select_area(self.area_cb)
        self._PBotUtils.sys_msg("Укажи зону работы ЛКМ выделяя зону {}".format(self.player_start))
        self.cb_ok.wait()
        self.cb_ok.clear()
        time.sleep(0.2)
        for gob in self._PBotGobAPI.gobs_in_area(*self.area[0], *self.area[1]):
            resname = gob.get_resname()
            if resname.startswith("gfx/terobjs/stockpile-leaf"):
                self.stockpile_of_tea = True
        while self.stockpile_of_tea:
            if self._PBotCharacterAPI.get_speed() == 0:
                self._PBotUtils.sys_msg('Вы остановили бот')
                break
            self.fill_cauldron()
            self.stand_to_cauldron()
            self.craft()
            self.sliv_tea()
            self.check_stamina()
            self.check_stockpile_of_tea()

    def check_stockpile_of_tea(self):
        for gob in self._PBotGobAPI.gobs_in_area(*self.area[0], *self.area[1]):
            resname = gob.get_resname()
            if resname.startswith("gfx/terobjs/stockpile-leaf"):
                self._PBotUtils.sys_msg('Мало листьев, останавливаюсь')
                self.stockpile_of_tea = True

    def sliv_tea(self):
        for barrel in self._PBotGobAPI.gobs_in_area(*self.area[0], *self.area[1]):
            resname = barrel.get_overlay_names()
            if "gfx/terobjs/barrel-tea" in resname:
                barrel.pf_click(1, 0)
                time.sleep(1)
                self._PBotUtils.pf_wait()
                invs = [self._PBotUtils.player_inventory()]
                for inv in filter(None, invs):
                    for itm in filter(lambda x: x != None and str(x.get_contents_name()).endswith("Tea"), itertools.chain(inv.get_inventory_items_by_resnames(".*"), self._PBotCharacterAPI.get_equipment())):
                        itm.take_item()
                        locat = itm.get_inv_loc()
                        time.sleep(0.2)
                        barrel.item_click(0)
                        time.sleep(0.2)

                        if locat[0] > 9:
                            locat_x = locat[0]-2
                        elif locat[0] > 4:
                            locat_x = locat[0]-1
                        else:
                            locat_x = locat[0]

                        if locat[1] > 9:
                            locat_y = locat[1]-5
                        elif locat[1] > 4:
                            locat_y = locat[1]-1
                        else:
                            locat_y = locat[1]
                        inv.drop_item_to_inventory(locat_x, locat_y)
                        time.sleep(0.2)

    def check_stamina(self):
        if self._PBotCharacterAPI.get_stamina() < 70:
            invs = [self._PBotUtils.player_inventory(), self.getWInv(self._PBotWindowAPI.get_window("Belt"))]
            for inv in filter(None, invs):
                for itm in filter(lambda x: x != None and str(x.get_contents_name()).endswith("of Water"), itertools.chain(inv.get_inventory_items_by_resnames(".*"), self._PBotCharacterAPI.get_equipment())):
                    itm.activate_item()
                    menu = self._PBotUtils.get_flowermenu(5000)
                    if menu != None:
                        menu.choose_petal("Drink")
                        time.sleep(0.2)
                        self._PBotUtils.wait_for_hourglass(3*1000)
                        return


    def craft(self):
        for gob in self._PBotGobAPI.gobs_in_area(*self.area[0], *self.area[1]):
            resname = gob.get_resname()
            if resname.startswith("gfx/terobjs/stockpile-leaf"):
                gob.do_click(3, 0)
                time.sleep(0.2)
                count_epmty_tea_pods = 1
                while count_epmty_tea_pods > 0 or self.stockpile_of_tea:
                    self.check_stockpile_of_tea()
                    self._PBotUtils.craft_item("tea", 0)
                    time.sleep(0.2)
                    self._PBotUtils.wait_for_hourglass(3*1000)
                    count_epmty_tea_pods = self.count_full_tea_pods()
                    self.stockpile_of_tea = self.check_stockpile_of_tea()
                    self.check_stamina()

    def count_full_tea_pods(self):
        count_tea_pods = 0
        inv = self._PBotUtils.player_inventory()
        for itm in filter(lambda x: x != None and str(x.get_contents_name()).endswith("Tea"), itertools.chain(inv.get_inventory_items_by_resnames(".*"), self._PBotCharacterAPI.get_equipment())):
            count_tea_pods += 1
        return self.count_all_tea_pods - count_tea_pods

    def stand_to_cauldron(self):
        for gob in self._PBotGobAPI.gobs_in_area(*self.area[0], *self.area[1]):
            resname = gob.get_resname()
            if resname.startswith("gfx/terobjs/cauldron"):
                gob.pf_click(3, 0)
                self._PBotUtils.pf_wait()
                menu = self._PBotUtils.get_flowermenu(2*1000)
                if menu is not None:
                    menu.choose_petal("Open")
                    time.sleep(1.0)

    def fill_cauldron(self):
        for gob in self._PBotGobAPI.gobs_in_area(*self.area[0], *self.area[1]):
            resname = gob.get_overlay_names()
            if "gfx/terobjs/barrel-water" in resname:
                gob.pf_click(1, 0)
                self._PBotUtils.pf_wait()
                self._PBotCharacterAPI.do_act(["carry"])
                time.sleep(0.2)
                barrel_place = gob.get_coords()
                gob.do_click(1, 0)
                time.sleep(0.2)
                for gob in self._PBotGobAPI.gobs_in_area(*self.area[0], *self.area[1]):
                    resname = gob.get_resname()
                    if resname.startswith("gfx/terobjs/cauldron"):
                        gob.pf_click(3, 0)
                        time.sleep(0.5)
                        self._PBotUtils.pf_wait()
                        self._PBotUtils.map_click(barrel_place[0], barrel_place[1], 3)
                        time.sleep(0.5)
                        self._PBotUtils.map_click(self.player_start[0], self.player_start[1], 1)
                        time.sleep(1.0)
                        return

    def area_cb(self, a, b):
        self.area = (a, b)
        self.cb_ok.set()


