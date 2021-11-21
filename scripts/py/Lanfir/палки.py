## Transfer items from inventory to closest gob, like drying frame oven etc.
import sys, os
sys.path.insert(0, os.path.abspath('..'))

from __pbot.PBotSession import PBotSession


class Script:
    def run(self, sess: PBotSession):
        self._PBotCharacterAPI = sess.PBotCharacterAPI
        self._PBotUtils = sess.PBotUtils
        # self.send_telegram("hello world!")
        gg = sess.PBotUtils.get_item_at_hand()
        sess.PBotUtils.sys_msg("start {}".format(gg.get_name ()))
        invs = [sess.PBotUtils.player_inventory()]
        for inv in filter(None, invs):
            for itm in filter(lambda x: x != None and str(x.get_contents_name()).endswith("Tea"), itertools.chain(inv.get_inventory_items_by_resnames(".*"), sess.PBotCharacterAPI.get_equipment())):
                # itm.activate_item()
                # itm.take_item()
                itm.take_item()
                locat = itm.get_inv_loc()
                sess.PBotUtils.sys_msg("Взял {}".format(locat))
                # itm.itemact()
                time.sleep(0.2)
                barrel.item_click(0)
                # sess.PBotUtils.sys_msg("Слил")
                time.sleep(0.2)

                if locat[0] > 9:
                    locat_x = locat[0]-2
                elif locat[0] > 4:
                    locat_x = locat[0]-1
                else:
                    locat_x = locat[0]
                sess.PBotUtils.sys_msg("Взял {}".format(locat_x))

                if locat[1] > 9:
                    locat_y = locat[1]-5
                elif locat[1] > 4:
                    locat_y = locat[1]-1
                else:
                    locat_y = locat[1]
                inv.drop_item_to_inventory(locat_x, locat_y)
                # sess.PBotUtils.sys_msg("Положил")
                time.sleep(0.2)

    def send_telegram(self, text: str):
        token = "2088869176:AAGkyUmaRGKEzzqR3ccgfBJ_dxYmKkF-NYI"
        url = "https://api.telegram.org/bot"
        channel_id = "20871713"
        url += token
        method = url + "/sendMessage"

        r = requests.post(method, data={
            "chat_id": channel_id,
            "text": text
        })

        if r.status_code != 200:
            raise Exception("post_text error")


