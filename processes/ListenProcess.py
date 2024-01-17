from App import BotApp
from operator import itemgetter


def ListenProcess(APP: BotApp, dictProxy):
    def listenChannel(msg) -> None:
        fromWho, userMsg = itemgetter('display-name', 'message')(msg)

        # Do not update if the response is the same
        if fromWho == dictProxy["fromWho"] and userMsg == dictProxy["userMsg"]:
            return

        # Set the correct values
        dictProxy.update({
            "fromWho": fromWho, 
            "userMsg": userMsg
        })

    APP.listen(listenChannel)