from __pbot.PBotSession import PBotSession
import math, time, random, datetime

#Forage script v1.1 by Frostz

#Randomly walks around, searches and picks up forageables avoiding aggressive mobs
#Change to crawl speed to stop the script

#add here herbs you want to ignore
blacklisted_herbs = '|'.join([
    #'blueberry',
    #'bloodstern',
    #'candleberry',
    'cattail',
    #'oystermushroom',
    'perfect',
    'clover',
    #'chantrelle',
    #'chives',
    'dandelion',
    #'lingon',
    #'ladysmantle',
    'mistletoe',
    'greenkelp',
    'frogspawn',
    #'royaltoadstool',
    #'rustroot',
    'spindlytaproot',
    'stingingnettle',
    'waybroad',
    'windweed',
    'yarrow',
    #'lakesnail',
    'clay-gray',
    'fairyshroomp',
])

#add here kritters you want to ignore
blacklisted_kritters = '|'.join([
    'ants',
    'anthill',
    #'dragonfly',
    #'firefly',
    'forestlizard',
    'forestsnail',
    'frog',
    'hen',
    'rat',
    'crab',
    'stoat',
    'chicken',
    'stagbeetle',
    'grasshopper',
    #'ladybug',
    'magpie',
    'midgeswarm',
    'moonmoth',
    'monarchbutterfly',
    'rabbit',
    'sandflea',
    'silkmoth',
    'squirrel',
    'firefly',
    'toad',
    'hedgehog',
    'waterstrider',
    'wildbees',
])

mob_scan_radius = 350
forage_scan_radius = 500
use_pathfinding = False

class Script:
    def run(self, sess: PBotSession):
        self._PBotGobAPI = sess.PBotGobAPI
        self._PBotCharacterAPI = sess.PBotCharacterAPI
        self._PBotUtils = sess.PBotUtils

        self._PBotUtils.sys_msg('Forage started')
        player = self._PBotGobAPI.get_player()

        while(player):
            if self._PBotCharacterAPI.get_speed() == 0:
                self._PBotUtils.sys_msg('Forage stopped')
                break

            # if player.is_moving() or self._PBotUtils.pf_wait():
            if player.is_moving():
                forage_list = self.search_forageables(forage_scan_radius)
                aggressive_mobs = self.scan_aggressive_mobs(mob_scan_radius)
                if self.is_player_safe(player, aggressive_mobs, mob_scan_radius):
                    if len(forage_list) > 0:
                        self.seek_forageable(self.get_closest_safe_forageable(forage_list, aggressive_mobs, mob_scan_radius))
                
                self.sleep()
            else:
                self.move_random(player)
                # self.move_points(player, point)
                self.sleep()

    def sleep(self):
        time.sleep(0.5)

    def is_player_safe(self, player, aggressive_mobs, mob_scan_radius):
        for aggressive_mob in aggressive_mobs:
            if aggressive_mob.dist(player) < mob_scan_radius and not aggressive_mob.is_knocked():
                self.avoid_mob(player, aggressive_mob, mob_scan_radius)
                return False

        return True

    def get_closest_safe_forageable(self, forage_list, aggressive_mobs, mob_scan_radius):
        sorted_forage = sorted(
            forage_list, 
            key=lambda elem: self.distance_to_player(elem),
        )

        for item in sorted_forage:
            is_safu = True

            for mob in aggressive_mobs:
                if item.dist(mob) < mob_scan_radius:
                    is_safu = False
            
            if is_safu:
                return item

    def move_random(self, player):
        x = player.get_coords()[0]
        y = player.get_coords()[1]

        u = random.uniform(-1,1)
        rx = random.random() * u
        ry = random.random() * u

        nx=x+((x/10)*ry)
        ny=y+((y/10)*rx)

        self._PBotUtils.map_click(nx, ny)

    def move_points(self, player):
        x = player.get_coords()[0]
        y = player.get_coords()[1]

        u = random.uniform(-1,1)
        rx = random.random() * u
        ry = random.random() * u

        nx=x+((x/10)*ry)
        ny=y+((y/10)*rx)

        self._PBotUtils.map_click(nx, ny)

    def search_forageables(self, forage_scan_radius):
        herbs = self._PBotGobAPI.get_gobs_by_resname('gfx/terobjs/herbs/(?!('+blacklisted_herbs+')).*')
        items = self._PBotGobAPI.get_gobs_by_resname('gfx/terobjs/items/grub.*')
        kritters = self._PBotGobAPI.get_gobs_by_resname(
            'gfx/kritter/(?!('
            +blacklisted_kritters+'|'
            +self.aggressive_mobs_string
            +self.passive_mobs_string
            +')).*'
        )

        forageables = herbs + kritters + items

        return forageables

    def seek_forageable(self, herb):
        id = herb.add_gob_text('Цель')

        self._PBotUtils.sys_msg("Иду поднимать {}".format(herb.get_resname().split("/")[-1]))

        if herb.get_resname().split("/")[-1] == 'oystermushroom':
            herb.do_click(3, 0)
        else:
            herb.pf_click(3, 0) if use_pathfinding else herb.do_click(3, 0)

        menu = self._PBotUtils.get_flowermenu(1000)
        if menu:
            menu.choose_petal('Pick')
        else: #walkover stuff like leafpile, dustpile, etc
            herb.pf_click(1, 0) if use_pathfinding else herb.do_click(1, 0)

    def distance_to_player(self, target):
        return target.dist(self._PBotGobAPI.get_player())

    def scan_aggressive_mobs(self, scan_radius):
        return self._PBotGobAPI.get_gobs_by_resname('gfx/kritter/'+self.aggressive_mobs_complete)

    def avoid_mob(self, player, mob, radius):
        px = player.get_coords()[0]
        py = player.get_coords()[1]

        mx = mob.get_coords()[0]
        my = mob.get_coords()[1]

        dist = mob.dist(player)

        nx=self.move_away(px, mx, dist, radius)
        ny=self.move_away(py, my, dist, radius)

        self._PBotUtils.pf_left_click(nx, ny) if use_pathfinding else self._PBotUtils.map_click(nx, ny)

    def move_away(self, current, target, dist, radius):
        factor = radius / dist
        return target + (current - target) * factor


    aggressive_mobs_list = [
        'adder',
        'badger',
        'bat',
        'bear',
        'boreworm',
        'boar',
        'caveangler',
        'caverat',
        'lynx',
        'midgeswarm',
        'moose',
        'orca',
        #'sandflea',
        'troll',
        'walrus',
        'wildgoat',
        'wolf',
        'wolverine',
    ]
    aggressive_mobs_string = '|'.join(aggressive_mobs_list)
    aggressive_mobs_complete = '|.*'.join(aggressive_mobs_list)


    passive_mobs_list = [
        'beaver',
        'cattle',
        'dryad',
        'fox',
        'goldeneagle',
        'greyseal',
        'horse',
        'mammoth',
        'pelican',
        'reddeer',
        'sheep',
        'swan'
    ]
    passive_mobs_string = '|'.join(passive_mobs_list)