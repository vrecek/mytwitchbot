from App import BotApp
from time import sleep
from datetime import datetime


def BossProcess(APP: BotApp, dictProxy) -> None:
    RECEIVE_FROM = 'demonzzbot'
    COMMAND = "!boss"
    buff = ['', '']


    def bossChannel():
        nonlocal buff

        # `boss` is required to be True
        if not dictProxy["boss"]: return
        
        fromWho, userMsg = APP.getDictProxyValues(dictProxy)

        # Compare the values
        if not APP.canContinueLoop([fromWho, userMsg], buff):
            return
        buff = [fromWho, userMsg]

        # Check if the boss has appeared
        if fromWho == RECEIVE_FROM and '!boss' in userMsg:
            print(f'[BOSS] {datetime.now().strftime("[%H:%M:%S]")} {COMMAND}')
            
            APP.send(COMMAND)
            sleep(5)


    while True:
        bossChannel()