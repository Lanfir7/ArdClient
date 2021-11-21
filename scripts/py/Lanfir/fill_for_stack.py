import itertools
import time
from __pbot.PBotSession import PBotSession
from __pbot.PBotWindow import PBotWindow
from __pbot.PBotInventory import PBotInventory
from typing import Optional

import sys, os, threading, time
sys.path.insert(0, os.path.abspath('..'))

from __pbot.PBotSession import PBotSession
from __pbot.PBotGob import PBotGob

class Script:
    area = None
    ignore = []
    cb_gob: PBotGob = None
    cb_ok = threading.Event()

    def area_cb(self, a, b):
        self.area1 = (a,b)
        self.cb_ok.set()

    def area_cc(self, a, b):
        self.area2 = (a,b)
        self.cb_ok.set()

    def run(self, sess: PBotSession):
        # sess.close_session()
        # sess = sess.new_session("AHaPXuCT", "Denisdenis@231", "Lanfir")
        # time.sleep(1.5)
        self.session = sess
        self._PBotGobAPI = sess.PBotGobAPI
        self._PBotCharacterAPI = sess.PBotCharacterAPI
        self._PBotUtils = sess.PBotUtils
        self._PBotWindowAPI = sess.PBotWindowAPI
        self.player = sess.PBotGobAPI.get_player()

        sess.PBotUtils.select_area(self.area_cb)
        sess.PBotUtils.sys_msg("Укажи ОТКУДА мне брать ЛКМ выделяя зону")
        self.cb_ok.wait()
        self.cb_ok.clear()

        sess.PBotUtils.select_area(self.area_cc)
        sess.PBotUtils.sys_msg("Укажи КУДА складывать ЛКМ выделяя зону")
        self.cb_ok.wait()
        self.cb_ok.clear()

        self.cb()

    def check_inventar(self):
        free = self._PBotUtils.player_inventory().free_slots()
        items = len(self._PBotUtils.player_inventory().get_inventory_items())
        self._PBotUtils.sys_msg("Свободно в инвентаре {} предметов {}".format(free, items))
        if items < 2:
            TheEnd = True
            for gob in self._PBotGobAPI.gobs_in_area(*self.area1[0], *self.area1[1]):
                if self._PBotUtils.player_inventory().free_slots() < 2:
                    continue
                elif not gob.get_id():
                    TheEnd = True
                    continue
                elif gob.get_id() in self.ignore:
                    TheEnd = True
                    continue
                else:
                    TheEnd = False
                    gob.pf_click(3, 1)
                    time.sleep(0.5)
                    self._PBotUtils.pf_wait()
                    while self.player.is_moving():
                        time.sleep(0.5)
                    gob.pf_click(3, 0)
                    wnd_name = gob.window_name_for_gob()
                    if wnd_name:
                        wnd = self._PBotWindowAPI.get_window(wnd_name, 1000*5)
                        invs = wnd.get_inventories()
                        have_item = len(invs[0].get_inventory_items())
                        self._PBotUtils.sys_msg("Предметов В {}".format(have_item))
                        if have_item < 1:
                            self.ignore.append(gob.get_id())

        else:
            TheEnd = False
        return TheEnd

    def make_stockpiles(self):
        itms = self._PBotUtils.player_inventory().get_inventory_items()
        itm = itms.pop()
        itm.take_item(True)
        self._PBotUtils.make_pile()
        x = min(self.area[0][0], self.area[1][0]) + 5.5
        y = min(self.area[0][1], self.area[1][1]) + 5.5
        x_lim = max(self.area[0][0], self.area[1][0])
        y_lim = max(self.area[0][1], self.area[1][1])
        self._PBotUtils.placeThing(x, y)
        while self._PBotGobAPI.get_gob_by_coords(x, y) is None:
            time.sleep(0.025)
        while self._PBotGobAPI.get_gob_by_coords(x, y).get_resname() is None:
            time.sleep(0.025)
        bb = self._PBotGobAPI.get_gob_by_coords(x, y).get_boundingbox_rect()
        for itm in itms:
            x += abs(bb[0][0]) + abs(bb[1][0])
            if x >= x_lim:
                y += abs(bb[0][1]) + abs(bb[1][1])
                x = min(self.area[0][0], self.area[1][0]) + 5.5
            if y >= y_lim:
                break
            loc_found = False
            for loc in [[bb[0][0] + 5.5, 0], [bb[1][0] - 5.5, 0], [0, bb[0][1] + 5.5], [0, bb[1][1] - 5.5]]:
                self._PBotUtils.pf_left_click(x + loc[0], y + loc[1])
                if self._PBotUtils.pf_wait():
                    loc_found = True
                    break
            if not loc_found:
                return
            itm.take_item(True)
            self._PBotUtils.make_pile()
            self._PBotUtils.placeThing(x, y)
            while self._PBotGobAPI.get_gob_by_coords(x, y) is None:
                time.sleep(0.025)

    def cb(self):
        self._PBotUtils.sys_msg("start {} {}".format(self.area1, self.area2))
        for gob in self._PBotGobAPI.gobs_in_area(*self.area2[0], *self.area2[1]):
            resname = gob.get_resname()
            if resname.startswith("gfx/terobjs/tt2ub"):
                continue
            else:
                notFull = True
                while notFull:
                    TheEnd = self.check_inventar()
                    if TheEnd:
                        self._PBotUtils.sys_msg("Закончил")
                        break
                    wnd_name = gob.window_name_for_gob()
                    if wnd_name is None:
                        self.give_to_pile(gob)
                    else:
                        self.give_to_window(gob, wnd_name)
                    items = len(self._PBotUtils.player_inventory().get_inventory_items())
                    if items > 0:
                        notFull = False
        self._PBotUtils.sys_msg("Закончил")

    def give_to_pile(self, gob):
        gob.pf_click(3, 0)
        self._PBotUtils.pf_wait()
        wnd = self._PBotWindowAPI.get_window("Stockpile", 1000*3600)
        rem = wnd.get_stockpile_total_capacity()-wnd.get_stockpile_used_capacity()
        wnd.put_item_from_inventory_to_stockpile(rem)
        wnd.close()
        time.sleep(0.3)

    def give_to_window(self, gob, wnd_name):
        gob.pf_click(3, 0)
        self._PBotUtils.pf_wait()
        time.sleep(0.3)
        wnd = self._PBotWindowAPI.get_window(wnd_name, 1000*5)
        invs = wnd.get_inventories()
        if len(invs) < 1:
            return
        for x in range(invs[0].free_slots()):
            invs[0].xfer_to()
        self._PBotUtils.sys_msg("Предметов В {}".format(len(invs[0].get_inventory_items())))
        time.sleep(0.3)
