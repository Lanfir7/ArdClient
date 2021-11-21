from typing import Optional, List

from __py_api.PBotItem import PBotItem


class PBotCharacterAPI(object):
    def __init__(self, gw, ui):
        self._CharacterAPI = gw.jvm.haven.purus.pbot.PBotCharacterAPI
        self._ui = ui

    ## Returns the player stamina
    # @return Player stamina between 0-100
    def get_stamina(self) -> float:
        return float(self._CharacterAPI.getStamina(self._ui))

    ## Returns the player energy
    # @return Player energy between 0-100
    def get_energy(self) -> float:
        return float(self._CharacterAPI.getEnergy(self._ui))

    ## Returns the player hp
    # @return Player hp between 0-100
    def get_hp(self) -> float:
        return float(self._CharacterAPI.getHp(self._ui))

    ## Send act message to server
    # Act can be used for example to choose a cursor
    # Some acts:
    # dig, mine, carry, destroy, fish, inspect, repair, crime, swim, tracking, aggro, shoot
    # @param act list of acts
    def do_act(self, act: List[str]):
        self._CharacterAPI.doAct(self._ui, act)

    # ## Resname of the cursor currently selected
    # # May be none if cursor couldn't be found
    # # @return resname of the cursor
    # def get_curs_name(self) -> Optional[str]:
    #     return self._CharacterAPI.PBotCharacterAPI().getCursName()

    ## Cancels the current act by right clicking
    def cancel_act(self):
        self._CharacterAPI.cancelAct(self._ui)

    ## Set player speed setting
    # @param speed 1 = crawl, 2 = walk, 3 = run, 4 = sprint
    def set_speed(self, speed: int):
        self._CharacterAPI.setSpeed(self._ui, speed)

    ## Get current speed setting of player
    # @return 1 = crawl, 2 = walk, 3 = run, 4 = sprint
    def get_speed(self) -> int:
        return self._CharacterAPI.getSpeed(self._ui)

    ## Get maximum speed setting that the player can be set to
    # @return 1 = crawl, 2 = walk, 3 = run, 4 = sprint
    def get_max_speed(self) -> int:
        return self._CharacterAPI.getMaxSpeed(self._ui)

    ## Send message to the given chat
    # @param chat_name name of the chat, for example "Area Chat"
    # @param msg Message to send into the chat
    def msg_to_chat(self, chat_name: str, msg: str):
        self._CharacterAPI.msgToChat(self._ui, chat_name, msg)

    ## Returns content of each slot in players equipment menu
    # @return list with each slot containing None or PBotItem
    def get_equipment(self) -> List[Optional[PBotItem]]:
        return [PBotItem(x) if x is not None else None for x in self._CharacterAPI.getEquipment()]
    #
    # ## Equip item from hand to the given slot
    # # @param slot equipment slot to equip item to
    # def equipEquipment(self, slot: int):
    #     self._CharacterAPI.PBotCharacterAPI().equipEquipment(slot)
