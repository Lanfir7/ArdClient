from typing import Optional, Callable, List

from __py_api.PBotGob import PBotGob


class PBotGobAPI(object):
    def __init__(self, gw, ui):
        self._PBotGobAPI = gw.jvm.haven.purus.pbot.PBotGobAPI
        self._ui = ui

    # ## Get gobs matching the specific regex pattern
    # # @param resname regex pattern
    # # @return List of PBotGobs with resname matching the given regex pattern
    # def get_gobs_by_resname(self, resname: str) -> List[PBotGob]:
    #     return [PBotGob(x) for x in self._PBotGobAPI.findGobByNames(resname)]

    ## Get the player gob if it exists
    # @return player gob ot None if not found
    def get_player(self) -> PBotGob:
        gob = self._PBotGobAPI.player(self._ui)
        return PBotGob(gob) if gob is not None else None


    ## Get closest gob matching the specific regex pattern
    # @param resname regex pattern
    # @return closest PBotGob
    def get_closest_gob_by_resname(self, resname: str) -> Optional[PBotGob]:
        gob = self._PBotGobAPI.findGobByNames(self._ui, 5, resname)
        return PBotGob(gob) if gob is not None else None

    ## Returns gob with exactly the given coords or None if not found
    # @param x x-coordinate of the gob
    # @param y y-coordinate of the gob
    # @return gob with coordinates given or null
    def get_gob_by_coords(self, x: float, y: float) -> Optional[PBotGob]:
        gob = self._PBotGobAPI.getGobWithCoords(self._ui, (x, y))
        return PBotGob(gob) if gob is not None else None

    ## Find object by id
    # @param id id of the object to look for
    # @return object with id or None if not found
    def find_gob_by_id(self, id: int) -> Optional[PBotGob]:
        gob = self._PBotGobAPI.findGobById(self._ui, id)
        return PBotGob(gob) if gob is not None else None

    ## Used to register gob callbacks
    # @param cb callback called with the gob
    def select_gob(self):
        gob = self._PBotGobAPI.selectGob(self._ui)
        return PBotGob(gob)

#
# class _SelectGobCb(object):
#     def __init__(self, cb: Callable[[PBotGob], any]):
#         self.cb = cb
#
#     def callback(self, gob):
#         self.cb(PBotGob(gob))
#
#     class Java:
#         implements = ["haven.purus.pbot.api.Callback"]