from App import BotApp
from operator import itemgetter
from time import sleep
from datetime import datetime
from threading import Timer


def BFHProcess(APP: BotApp, dictProxy: dict) -> None:
    RECEIVE_FROM = 'demonzzbot'
    buff = ['', '']
    res = {
        "boss": {
            "c": "!boss",
            "t": .5,
            "b": True
        },
        "ffa": {
            "c": "!ffa",
            "t": .5,
            "b": True
        },
        "heist": {
            "c": f"!heist {dictProxy['heist']}",
            "t": 6.0,
            "b": True
        }
    }


    def checkResponse(string: str) -> list:
        # Extract the command, time to exe, bool
        for x in res:
            command, time, canNext = itemgetter('c', 't', 'b')(res[x])

            # Return values above if the response is correct
            if canNext and (f"!{x}" in string) and dictProxy[x]:
                return [x, command, float(time)]

        return [None, None, None]

    def allowNext(type: str) -> None:
        res[type]["b"] = True

    def exeTimer(type: str, command: str) -> None:
        print(f'[{type.upper()}] {datetime.now().strftime("[%H:%M:%S]")} {command}')
        APP.send(command)

        # "Unlock" the command in 10 seconds
        Timer(10, lambda: allowNext(type)).start()


    # Main channel
    def bfhChannel():
        nonlocal buff

        fromWho, userMsg = APP.getDictProxyValues(dictProxy)

        # Compare the values
        if not APP.canContinueLoop([fromWho, userMsg], buff):
            return
        buff = [fromWho, userMsg]

        # Check if the boss/ffa/heist has appeared
        if fromWho == RECEIVE_FROM:
            type, command, time = checkResponse(userMsg)

            if not type:
                return

            # "Lock" the command, just to prevent sending the same message
            res[type]["b"] = False

            # Send the message after `time` seconds
            Timer(time, lambda: exeTimer(type, command)).start()


    while True:
        bfhChannel()