import os
import sys
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
import importlib
from threading import Thread
from py4j.java_gateway import JavaGateway, CallbackServerParameters, GatewayParameters


class Variables:
    def __init__(self, value):
        self.version = value


class PBotRunner(object):

    def start(scriptname, methodname, scriptid):
        importlib.invalidate_caches()
        script = importlib.import_module(scriptname)
        importlib.reload(script)
        Thread(target=getattr(script.Script(), methodname), args=[gateway, scriptid, gvar]).start()

    class Java:
        implements = ["haven.purus.pbot.Py4j.PBotScriptLoader"]


gvar = Variables("0.1")
gateway = JavaGateway(callback_server_parameters=CallbackServerParameters(),
                      python_server_entry_point=PBotRunner,
                      gateway_parameters=GatewayParameters(auto_field=True, auto_convert=True))