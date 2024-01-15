import json
import os
from operator import itemgetter
from irc import twitch_irc


class BotApp:
    def __init__(self, config_file: str) -> None:
        """Required config fields: `channel, user_sender.oauth, user_sender.name, bot_sender.oauth, bot_sender.name`"""

        if not os.path.isfile(config_file):
            raise Exception("Config file does not exist")


        with open(config_file, 'r') as file:
            deserialized = json.load(file)

            try:
                itemgetter('channel')(deserialized)
                itemgetter('name', 'oauth')(deserialized["user_sender"])
                itemgetter('name', 'oauth')(deserialized["bot_sender"])
                
            except:
                raise Exception("Some fields are missing")
                
            self.__config = deserialized
            self.vars = {}

    def __send_listen_help(self, user: str, type: str, val):
        ch = self.getConfigInfo('channel')

        if user == 'bot':
            conn = self.__connBot
        elif user == 'user':
            conn = self.__connUser

        if type == 'send':
            conn.send(ch, val)
        elif type == 'listen':
            conn.listen(ch, on_message=val)



    def connect(self):
        self.__connUser = twitch_irc.TwitchIRC(
            self.getConfigInfo('user_name'),
            self.getConfigInfo('user_oauth'),
        )

        self.__connBot = twitch_irc.TwitchIRC(
            self.getConfigInfo('bot_name'),
            self.getConfigInfo('bot_oauth'),
        )
    

    def send(self, user: str, msg: str) -> None:
        """`user` field must be either 'bot' or 'user'"""

        self.__send_listen_help(user, 'send', msg)

    
    def listen(self, user, listenFn) -> None:
        """`user` field must be either 'bot' or 'user'"""

        self.__send_listen_help(user, 'listen', listenFn)


    def setVar(self, key: str, val: str) -> None:
        self.vars[key] = val


    def getVar(self, key: str):
        return self.vars[key] if key in self.vars else None


    def getConfigInfo(self, key: str):
        """Possible keys: `user_name, user_oauth, bot_name, bot_oauth, channel`"""
    
        c = self.__config

        match key:
            case 'channel':
                return c["channel"]
            
            case "user_name": 
                return c["user_sender"]["name"]
            
            case "user_oauth": 
                return c["user_sender"]["oauth"]
            
            case "bot_name": 
                return c["bot_sender"]["name"]
            
            case "bot_oauth": 
                return c["bot_sender"]["oauth"]
            
            case _: 
                raise Exception(f"Field `{key}` not found")
            

    def closeConnection(self) -> None:
        """Closes both connections"""

        self.__connUser.close_connection()
        self.__connBot.close_connection()