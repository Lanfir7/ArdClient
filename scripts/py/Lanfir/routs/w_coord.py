from __pbot.PBotSession import PBotSession

class Script:
    def run(self, sess: PBotSession):
        self._PBotUtils = sess.PBotUtils
        file = open("coords.txt", "r")
        filer = file.read()
        file.close()
        filew = open("coords.txt", "w")
        coords = sess.PBotGobAPI.get_player().get_coords()
        new_file = "{}{},{}\n".format(filer, coords[0], coords[1])
        filew.write(new_file)
        filew.close()
        self._PBotUtils.sys_msg('Координаты сохранены')