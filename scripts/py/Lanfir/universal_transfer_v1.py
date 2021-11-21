import itertools
import time
# from __pbot.PBotSession import PBotSession
# from __pbot.PBotInventory import PBotInventory
from typing import Optional
from PBotWindowAPI import PBotWindowAPI
from PBotUtils import PBotUtils
from PBotGobAPI import PBotGobAPI
from __pbot.variables import Vars
import sys, os, threading, time
sys.path.insert(0, os.path.abspath('..'))

# from __pbot.PBotSession import PBotSession
# from __pbot.PBotGob import PBotGob

class Script(Vars):
    area = None
    ignore = []
    # cb_gob: PBotGob = None
    cb_ok = threading.Event()
    x, y, x_lim, y_lim, bb = 0, 0, 0, 0, 0
    gobs_otkuda = []
    gobs_kuda = []

    def area_cb(self, a, b):
        self.area1 = (a,b)
        self.cb_ok.set()

    def area_cc(self, a, b):
        self.area2 = (a,b)
        self.cb_ok.set()

    def run(self):
        self.PBotUtils = PBotUtils(self.gw, self.ui)
        self.PBotGobAPI = PBotGobAPI(self.gw, self.ui)
        self.PBotWindowAPI = PBotWindowAPI(self.gw, self.ui)
        self.player = self.PBotGobAPI.get_player()
        # sess.close_session()
        # sess = sess.new_session("AHaPXuCT", "Denisdenis@231", "Lanfir")
        # time.sleep(1.5)
        # self.session = PBotSession(self.gw.jvm.haven.purus.pbot)
        # self.PBotGobAPI = self.session.PBotGobAPI
        # self._PBotCharacterAPI = self.session.PBotCharacterAPI
        # self.PBotUtils = PBotUtils(self.gw.jvm.haven.purus.pbot.PBotUtils)
        # self._PBotWindowAPI = self.session.PBotWindowAPI
        # self.player = self.PBotUtils.player()

        self.area1 = self.PBotUtils.select_area()
        self.PBotUtils.sys_msg("Укажи ОТКУДА мне брать ЛКМ выделяя зону")
        self.PBotUtils.sys_msg("Закончил {}".format(self.area1))

        self.area2 = self.PBotUtils.select_area()
        self.PBotUtils.sys_msg("Укажи КУДА складывать ЛКМ выделяя зону")
        self.PBotUtils.sys_msg("Закончил {}".format(self.area2))

        #gobs otkuda
        for gob in self.PBotUtils.gobs_in_area(self.area1[0], self.area1[1]):
            self.gobs_otkuda.append(gob)

        #gobs kuda
        gobs = self.PBotUtils.gobs_in_area(self.area2[0], self.area2[1])
        if gobs:
            for gob in self.PBotUtils.gobs_in_area(self.area2[0], self.area2[1]):
                if not gob.stockpile_is_full():
                    self.gobs_kuda.append(gob)

        while self.gobs_otkuda:
            self.take_from()
            self.place_to()

        # gobs = self.PBotGobAPI.gobs_in_area(*self.area2[0], *self.area2[1])
        # if gobs:
        #     self.cb()
        # else:
        #     self.check_inventar()
        #     self.make_stockpiles()
        #     self.cb()

    def take_from(self):
        free = self.PBotUtils.player_inventory().free_slots()
        items = len(self.PBotUtils.player_inventory().get_inventory_items())
        self.PBotUtils.sys_msg("Свободно в инвентаре {} предметов {}".format(free, items))
        if items < 2:
            TheEnd = True
            for gob in self.gobs_otkuda:
                if self.PBotUtils.player_inventory().free_slots() < 2:
                    return
                elif not gob.get_id():
                    TheEnd = True
                    continue
                else:
                    TheEnd = False
                    gob.pf_click(3, 1)
                    # self.PBotUtils.pf_wait()
                    time.sleep(0.9)
                    self.PBotUtils.pf_wait()
                    while self.player.is_moving():
                        time.sleep(0.1)
                    gob.pf_click(3, 0)
                    wnd_name = gob.window_name_for_gob()
                    if wnd_name:
                        wnd = self.PBotWindowAPI.get_window(wnd_name, 1000*5)
                        invs = wnd.get_inventories()
                        have_item = len(invs[0].get_inventory_items())
                        # self.PBotUtils.sys_msg("Предметов В {}".format(have_item))
                        if have_item < 1:
                            # gob.set_marked(0, 250, 0)
                            self.gobs_otkuda.remove(gob)
                            self.ignore.append(gob.get_id())

        else:
            TheEnd = False
        return TheEnd

    def place_to(self):
        if not self.gobs_kuda:
            self.logic_stockpiles()
            time.sleep(1.025)
            for gob in self.PBotUtils.gobs_in_area(self.area2[0], self.area2[1]):
                if not gob.stockpile_is_full():
                    self.gobs_kuda.append(gob)
        for gob in self.gobs_kuda:
            self.PBotUtils.sys_msg("Я тут")
            notFull = True
            while notFull:
                ee = self.take_from()
                if ee:
                    self.PBotUtils.sys_msg("Закончил 2")
                    break
                wnd_name = gob.window_name_for_gob()
                self.PBotUtils.sys_msg("Уже тут {}".format(wnd_name))
                if wnd_name is None:
                    self.give_to_pile(gob)
                else:
                    self.give_to_window(gob, wnd_name)
                items = len(self.PBotUtils.player_inventory().get_inventory_items())
                if items > 0:
                    notFull = False
        self.PBotUtils.sys_msg("Закончил 3")



    def check_inventar(self):
        free = self.PBotUtils.player_inventory().free_slots()
        items = len(self.PBotUtils.player_inventory().get_inventory_items())
        self.PBotUtils.sys_msg("Свободно в инвентаре {} предметов {}".format(free, items))
        if items < 2:
            TheEnd = True
            for gob in self.PBotUtils.gobs_in_area(self.area1[0], self.area1[1]):
                if self.PBotUtils.player_inventory().free_slots() < 2:
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
                    self.PBotUtils.pf_wait()
                    while self.player.is_moving():
                        time.sleep(0.5)
                    gob.pf_click(3, 0)
                    wnd_name = gob.window_name_for_gob()
                    if wnd_name:
                        wnd = self.PBotWindowAPI.get_window(wnd_name, 1000*5)
                        invs = wnd.get_inventories()
                        have_item = len(invs[0].get_inventory_items())
                        self.PBotUtils.sys_msg("Предметов В {}".format(have_item))
                        if have_item < 1:
                            self.ignore.append(gob.get_id())

        else:
            TheEnd = False
        return TheEnd

    def make_stockpiles(self):
        itms = self.PBotUtils.player_inventory().get_inventory_items()
        itm = itms.pop()
        itm.take_item(True)
        self.PBotUtils.make_pile()
        x = min(self.area2[0][0], self.area2[1][0]) + 5.5
        y = min(self.area2[0][1], self.area2[1][1]) + 5.5
        x_lim = max(self.area2[0][0], self.area2[1][0])
        y_lim = max(self.area2[0][1], self.area2[1][1])
        self.PBotUtils.placeThing(x, y)
        while self.PBotGobAPI.get_gob_by_coords(x, y) is None:
            time.sleep(0.025)
        while self.PBotGobAPI.get_gob_by_coords(x, y).get_resname() is None:
            time.sleep(0.025)
        bb = self.PBotGobAPI.get_gob_by_coords(x, y).get_boundingbox_rect()
        for itm in itms:
            x += abs(bb[0][0]) + abs(bb[1][0])
            if x >= x_lim:
                y += abs(bb[0][1]) + abs(bb[1][1])
                x = min(self.area2[0][0], self.area2[1][0]) + 5.5
            if y >= y_lim:
                break
            loc_found = False
            for loc in [[bb[0][0] + 5.5, 0], [bb[1][0] - 5.5, 0], [0, bb[0][1] + 5.5], [0, bb[1][1] - 5.5]]:
                self.PBotUtils.pf_left_click(x + loc[0], y + loc[1])
                if self.PBotUtils.pf_wait():
                    loc_found = True
                    break
            if not loc_found:
                return
            itm.take_item(True)
            self.PBotUtils.make_pile()
            self.PBotUtils.placeThing(x, y)
            while self.PBotGobAPI.get_gob_by_coords(x, y) is None:
                time.sleep(0.025)

    def logic_stockpiles(self):
        itms = self.PBotUtils.player_inventory().get_inventory_items()
        itm = itms.pop()
        itm.take_item(True)
        self.PBotUtils.make_pile()
        if not self.x:
            self.x = min(self.area2[0][0], self.area2[1][0]) + 5.5
            self.y = min(self.area2[0][1], self.area2[1][1]) + 5.5
            self.x_lim = max(self.area2[0][0], self.area2[1][0])
            self.y_lim = max(self.area2[0][1], self.area2[1][1])
            self.PBotUtils.placeThing(self.x, self.y)
            while self.PBotGobAPI.get_gob_by_coords(self.x, self.y) is None:
                time.sleep(0.025)
            while self.PBotGobAPI.get_gob_by_coords(self.x, self.y).get_resname() is None:
                time.sleep(0.025)
            gob = self.PBotGobAPI.get_gob_by_coords(self.x, self.y)
            self.bb = gob.get_boundingbox_rect()
            gob.pf_click(1, 0)
            time.sleep(0.2)
        else:
            self.x += abs(self.bb[0][0]) + abs(self.bb[1][0])
            if self.x >= self.x_lim:
                self.y += abs(self.bb[0][1]) + abs(self.bb[1][1])
                self.x = min(self.area2[0][0], self.area2[1][0]) + 5.5
            # if self.y >= self.y_lim:
            #     break
            loc_found = False
            for loc in [[self.bb[0][0] + 5.5, 0], [self.bb[1][0] - 5.5, 0], [0, self.bb[0][1] + 5.5], [0, self.bb[1][1] - 5.5]]:
                self.PBotUtils.pf_left_click(self.x + loc[0], self.y + loc[1])
                if self.PBotUtils.pf_wait():
                    loc_found = True
                    break
            if not loc_found:
                return
            gob = self.PBotGobAPI.get_gob_by_coords(self.x, self.y)
            self.PBotUtils.placeThing(self.x, self.y)
            gob.pf_click(1, 0)
            time.sleep(0.2)

    def cb(self):
        self.PBotUtils.sys_msg("start {} {}".format(self.area1, self.area2))
        gobs = self.PBotUtils.gobs_in_area(self.area2[0], self.area2[1])
        works = []
        if gobs:
            for gob in self.PBotUtils.gobs_in_area(self.area2[0], self.area2[1]):
                if gob.stockpile_is_full():
                    gob.set_marked(0,255,0)
                    continue
                else:
                    works.append(gob)

            for gob in works:
                notFull = True
                while notFull:
                    TheEnd = self.check_inventar()
                    if TheEnd:
                        self.PBotUtils.sys_msg("Закончил")
                        break
                    wnd_name = gob.window_name_for_gob()
                    if wnd_name is None:
                        self.give_to_pile(gob)
                    else:
                        self.give_to_window(gob, wnd_name)
                    items = len(self.PBotUtils.player_inventory().get_inventory_items())
                    if items > 0:
                        notFull = False
        else:
            self.check_inventar()
            self.logic_stockpiles()
            self.cb()

        self.PBotUtils.sys_msg("Закончил")

    def give_to_pile(self, gob):
        gob.pf_click(3, 0)
        self.PBotUtils.pf_wait()
        wnd = self.PBotWindowAPI.get_window("Stockpile", 1000*3600)
        rem = self.PBotWindowAPI.get_stockpile_total_capacity(self.ui)-wnd.get_stockpile_used_capacity()
        wnd.put_item_from_inventory_to_stockpile(rem)
        wnd.close()
        time.sleep(0.3)
        if gob.stockpile_is_full():
            self.gobs_kuda.remove(gob)


    def give_to_window(self, gob, wnd_name):
        gob.pf_click(3, 0)
        self.PBotUtils.pf_wait()
        time.sleep(0.3)
        wnd = self.PBotWindowAPI.get_window(wnd_name, 1000*5)
        invs = wnd.get_inventories()
        if len(invs) < 1:
            return
        for x in range(invs[0].free_slots()):
            invs[0].xfer_to()
        self.PBotUtils.sys_msg("Предметов В {}".format(len(invs[0].get_inventory_items())))
        time.sleep(0.3)
