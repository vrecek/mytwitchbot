import json
import os
import signal
from operator import itemgetter
from irc import twitch_irc
from multiprocessing import Process
from typing import Callable
from datetime import datetime


class BotApp():
    def __init__(self, config_file: str) -> None:
        """Required config fields: `channel, user.oauth, user.name"""

        if not os.path.isfile(config_file):
            raise Exception("Config file does not exist")


        # Open the config file and the required fields
        with open(config_file, 'r') as file:
            deserialized = json.load(file)

            try:
                itemgetter('channel')(deserialized)
                itemgetter('name', 'oauth')(deserialized["user"])
                
            except:
                raise Exception("Some fields are missing")

            self.__config = deserialized
            self.__processes = []



    # Connect to the IRC
    def connect(self) -> None:
        self.__conn = twitch_irc.TwitchIRC(
            self.getConfigInfo('user_name'),
            self.getConfigInfo('user_oauth'),
        )


    # Create a new process
    def newProcess(self, fn: Callable, name: str, *args) -> Process:
        def processHandler(proc_args):
            # Set a SIGINT signal in case of KeyboardInterrupt
            # And execute the callable argument
            signal.signal(signal.SIGINT, lambda sig,frame: exit(0))
            fn(*proc_args)

        # Create an actual process
        proc = Process(target=processHandler, args=(args,))

        # Append to the class' process array
        self.__processes.append({
            "name": name,
            "proc": proc
        })

        return proc


    # Start the processes
    def launchProcesses(self) -> None:
        for p in self.__processes:
            p["proc"].daemon = True
            p["proc"].start()

            # Print the started process and its PID
            print(f'[INFO] Process -{p["name"]}- has started [{p["proc"].pid}]')

        for p in self.__processes:
            p["proc"].join()


    # Sends the message to the IRC
    def send(self, msg: str) -> None:
        self.__conn.send(self.__config["channel"], msg)

    
    # Listen to the incoming messages
    def listen(self, listenFn: Callable) -> None:
        self.__conn.listen(self.__config["channel"], on_message=listenFn)


    # Get the proxy fields
    def getDictProxyValues(self, proxy, additionalValues: list = None) -> list:
        # By default returns the first two fields, which should be fromWho and userMsg
        proxyValues = list(proxy.values())[0:2]

        # If additionalValues are specified, checks their existence and appends them to the final array
        if additionalValues:
            proxyValues.append([proxy[x] if x in proxy else None for x in additionalValues])

        return proxyValues
    

    # Checks if the while:True loop can continue
    def canContinueLoop(self, original: list, buff: list) -> bool:
        """First array element should be `fromWho` and second should be `userMsg`"""

        # Compare two messages (current and previous)
        # If the messages are identical, return False
        if (original[0] == buff[0]) and (original[1] == buff[1]):
            return False

        return True


    # Get the config dict fields
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
         

    #
    def getFormattedTime(self) -> str:
        return datetime.now().strftime("[%H:%M:%S]")


    def closeConnection(self) -> None:
        self.__conn.close_connection()