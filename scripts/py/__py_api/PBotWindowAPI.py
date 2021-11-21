from typing import Optional, List
from __py_api.PBotWindow import PBotWindow


class PBotWindowAPI(object):
    def __init__(self, gw, ui):
        self._PBotWindowAPI = gw.jvm.haven.purus.pbot.PBotWindowAPI
        self._ui = ui


    ## Get a window with a specific name
    # @param name Name of the window
    # @param timeout Timeout in milliseconds to wait for the window to appear
    # @return Returns the window or None if not found before timeout expires
    def get_window(self, name: str, timeout: int = 0) -> Optional[PBotWindow]:
        wnd = self._PBotWindowAPI.waitForWindow(self._ui, name, timeout)
        return PBotWindow(wnd) if wnd is not None else None

    ## Wait for a window with a specific name to disappear
    # @param name of the window
    # @param timeout in milliseconds
    def wait_for_window_close(self, name: str, timeout: int = 3600000):
        self._PBotWindowAPI.waitForWindowClose(self._ui, name, timeout)

    ## Get windows that match the given regex pattern
    # @param name Pattern to match window titles to
    # @return list of windows matching
    def get_windows(self, name: str) -> List[PBotWindow]:
        return [PBotWindow(x) for x in self._PBotWindowAPI.getWindows(self._ui, name)]

    ## Total capacity of the stockpile, if the window is stockpile
    # @return total capacity or -1 if stockpile couldn't be found
    def get_stockpile_total_capacity(self, ui) -> int:
        return self._PBotWindowAPI.getStockpileTotalCapacity(ui)
