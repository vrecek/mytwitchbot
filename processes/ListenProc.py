from App import BotApp
from operator import itemgetter


def ListenProcess(APP: BotApp, dictProxy):
    def listenChannel(msg) -> None:
        fromWho, userMsg = itemgetter('display-name', 'message')(msg)
            
        # Set the correct values
        dictProxy.update({
            "fromWho": fromWho, 
            "userMsg": userMsg
        })

    APP.listen(listenChannel)