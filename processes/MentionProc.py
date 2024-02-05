from App import BotApp
from threading import Timer


def MentionProcess(APP: BotApp, dictProxy: dict) -> None:
    buff: list = ['', '']
    NAME: str = 'vrecek'
    EXCLUDED: list = ['Supibot', 'demonzzbot']


    def mentionChannel() -> None:
        nonlocal buff

        fromWho, userMsg = APP.getDictProxyValues(dictProxy)

        # Compare the values
        if not APP.canContinueLoop([fromWho, userMsg], buff):
            return
        buff = [fromWho, userMsg]

        
        # Check if someone has mentioned the specified username
        if ( (fromWho in EXCLUDED) or (NAME not in userMsg) ):
            return


        print(f'[MENTION] {APP.getFormattedTime()} @{fromWho}: {userMsg}')


    while True:
        mentionChannel()
