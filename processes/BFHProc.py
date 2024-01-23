from App import BotApp
from time import sleep
from datetime import datetime


def BFHProcess(APP: BotApp, dictProxy) -> None:
    RECEIVE_FROM = 'demonzzbot'
    buff = ['', '']

    def checkResponse(string: str):
        for x in ['boss', 'ffa', 'heist']:
            exc = f'!{x}'

            if exc in string and dictProxy[x]:
                command = exc

                if x == 'heist':
                    command = f'{exc} {dictProxy["heist"]}'

                return [x, command]
            
        return [None, None]


    def bfhChannel():
        nonlocal buff

        fromWho, userMsg = APP.getDictProxyValues(dictProxy)

        # Compare the values
        if not APP.canContinueLoop([fromWho, userMsg], buff):
            return
        buff = [fromWho, userMsg]

        # Check if the boss/ffa has appeared
        if fromWho == RECEIVE_FROM:
            type, command = checkResponse(userMsg)

            if type:
                print(f'[{type.upper()}] {datetime.now().strftime("[%H:%M:%S]")} {command}')

                APP.send(command)
                sleep(2)


    while True:
        bfhChannel()