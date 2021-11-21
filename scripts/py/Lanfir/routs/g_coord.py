import itertools
from typing import Optional
from PBotWindowAPI import PBotWindowAPI
from PBotCharacterAPI import PBotCharacterAPI
from PBotUtils import PBotUtils
from PBotGobAPI import PBotGobAPI
from __pbot.variables import Vars
from PBotWindow import PBotWindow
from PBotInventory import PBotInventory
import sys, os, threading, time
import math, time, random, datetime

class Script(Vars):
    # def getWInv(self, wnd: PBotWindow) -> Optional[PBotInventory]:
    #     if wnd != None:
    #         inv = wnd.get_inventories()
    #         if len(inv) > 0:
    #             return inv[0]
    #     return None

    def run(self):
        self.PBotUtils = PBotUtils(self.gw, self.ui)
        self.PBotGobAPI = PBotGobAPI(self.gw, self.ui)
        self.PBotWindowAPI = PBotWindowAPI(self.gw, self.ui)
        self.PBotCharacterAPI = PBotCharacterAPI(self.gw, self.ui)
        self.player = self.PBotGobAPI.get_player()
        points = self.read_txt("coords")
        start = self.read_txt("current_route")
        # login = self.read_txt("login_settings").split(",")
        if self.PBotCharacterAPI.get_speed() == 0:
            start = ""
            self.PBotCharacterAPI.set_speed(2)
            time.sleep(0.5)
        # if not start:
        #     sess.close_session()
        #     sess = sess.new_session(login[0], login[1], login[2])
        #     time.sleep(1.5)
        # self.session = sess
        # self._PBotGobAPI = sess.PBotGobAPI
        # self._PBotCharacterAPI = sess.PBotCharacterAPI
        # self._PBotUtils = sess.PBotUtils
        # self._PBotWindowAPI = sess.PBotWindowAPI
        # self.player = sess.PBotGobAPI.get_player()
        self.PBotUtils.sys_msg('Старт')


        for step in points.split("\n"):
            if step:
                if self.PBotCharacterAPI.get_speed() == 0:
                    self.PBotUtils.sys_msg('Стоп')
                    break
                if start:
                    if step == start:
                        start = ""
                        self.PBotUtils.sys_msg('Продолжаю путь, сэр!')
                        self.walk(step)
                else:
                    self.walk(step)

        self.PBotUtils.sys_msg('Конец')

    def walk(self, step):
        st = step.split(",")
        self.PBotUtils.sys_msg('Иду {}, {}'.format(float(st[0]), float(st[1])))
        walking = True
        while walking:
            if self.PBotCharacterAPI.get_speed() == 0:
                self.PBotUtils.sys_msg('Стоп')
                break
            # self.check_stamina()
            self.PBotUtils.map_click(float(st[0]), float(st[1]))
            # self.PBotUtils.pf_left_click(float(st[0]), float(st[1]))
            # self.PBotUtils.pf_move(float(st[0]), float(st[1]))
            time.sleep(0.5)
            if self.player.is_moving():
                time.sleep(0.5)
            coords = self.PBotGobAPI.get_player().get_coords()
            if (int(coords[0])+1 == int(float(st[0])) and int(coords[1])+1 == int(float(st[1]))) or (int(coords[0]) == int(float(st[0])) and int(coords[1]) == int(float(st[1]))):
                filew = open("current_route.txt", "w")
                new_file = "{},{}".format(float(st[0]), float(st[1]))
                filew.write(new_file)
                filew.close()
                walking = False

    # def check_stamina(self):
    #     if self._PBotCharacterAPI.get_stamina() < 50:
    #         invs = [self.PBotUtils.player_inventory(), self.getWInv(self._PBotWindowAPI.get_window("Belt"))]
    #         for inv in filter(None, invs):
    #             for itm in filter(lambda x: x != None and str(x.get_contents_name()).endswith("of Water"), itertools.chain(inv.get_inventory_items_by_resnames(".*"), self._PBotCharacterAPI.get_equipment())):
    #                 itm.activate_item()
    #                 menu = self.PBotUtils.get_flowermenu(5000)
    #                 if menu != None:
    #                     menu.choose_petal("Drink")
    #                     time.sleep(0.2)
    #                     self.PBotUtils.wait_for_hourglass(3*1000)
    #                     return

    def read_txt(self, name):
        file = open("{}.txt".format(name), "r")
        filer = file.read()
        file.close()
        return filer

