import json
import os
import signal
from operator import itemgetter
from irc import twitch_irc
from multiprocessing import Process
from typing import Callable


class BotApp:
    def __init__(self, config_file: str) -> None:
        """Required config fields: `channel, user.oauth, user.name"""

        if not os.path.isfile(config_file):
            raise Exception("Config file does not exist")


        with open(config_file, 'r') as file:
            deserialized = json.load(file)

            try:
                itemgetter('channel')(deserialized)
                itemgetter('name', 'oauth')(deserialized["user"])
                
            except:
                raise Exception("Some fields are missing")
                
            self.__config = deserialized
            self.__processes = []



    def connect(self) -> None:
        self.__conn = twitch_irc.TwitchIRC(
            self.getConfigInfo('user_name'),
            self.getConfigInfo('user_oauth'),
        )


    def newProcess(self, fn: Callable, name: str, *args) -> Process:
        def processHandler(proc_args):
            signal.signal(signal.SIGINT, lambda sig,frame: exit(0))
            fn(*proc_args)


        proc = Process(target=processHandler, args=(args,))

        self.__processes.append({
            "name": name,
            "proc": proc
        })

        return proc


    def launchProcesses(self) -> None:
        for p in self.__processes:
            print(f'[INFO] Process -{p["name"]}- has started')

            p["proc"].daemon = True
            p["proc"].start()

        for p in self.__processes:
            p["proc"].join()


    def send(self, msg: str) -> None:
        self.__conn.send(self.__config["channel"], msg)

    
    def listen(self, listenFn: Callable) -> None:
        self.__conn.listen(self.__config["channel"], on_message=listenFn)


    def getDictProxyValues(self, proxy, additionalValues: list = None) -> list:
        proxyValues = list(proxy.values())[0:2]

        if additionalValues:
            proxyValues.append([proxy[x] if x in proxy else None for x in additionalValues])

        return proxyValues
    

    def canContinueLoop(self, original: list, buff: list) -> bool:
        """First array element should be `fromWho` and second should be `userMsg`"""
        if (original[0] == buff[0]) and (original[1] == buff[1]):
            return False

        return True


    def getConfigInfo(self, key: str) -> str:
        """Possible keys: `user_name, user_oauth, channel`"""
    
        c = self.__config

        match key:
            case 'channel':
                return c["channel"]
            
            case "user_name": 
                return c["user"]["name"]
            
            case "user_oauth": 
                return c["user"]["oauth"]
            
            case _: 
                if not key in c:
                    raise Exception(f"Field `{key}` not found")

                return c[key]
                           

    def closeConnection(self) -> None:
        self.__conn.close_connection()