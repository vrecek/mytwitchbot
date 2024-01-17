from App import BotApp
from time import sleep
from datetime import datetime


def BossProcess(APP: BotApp, dictProxy) -> None:
    RECEIVE_FROM = 'demonzzbot'
    COMMAND = "!boss"
    buff = ['', '']


    def bossChannel():
        nonlocal buff

        fromWho, userMsg = APP.getDictProxyResponse(dictProxy)

        # Compare the values
        if not APP.canContinueLoop([fromWho, userMsg], buff):
            return
        buff = [fromWho, userMsg]

        # Check if the boss has appeared
        if fromWho == RECEIVE_FROM and '!boss' in userMsg:
            print(f'[BOSS] {datetime.now().strftime("[%H:%M:%S]")} {COMMAND}')
            
            APP.send('user', COMMAND)
            sleep(5)


    while True:
        bossChannel()