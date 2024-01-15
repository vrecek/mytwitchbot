from App import BotApp
from operator import itemgetter
from time import sleep
from math import floor
from datetime import datetime
import threading
import re


def FishProcess(APP: BotApp):
    USERNAME = APP.getConfigInfo('user_name')
    RECEIVE_FROM = 'Supibot'
    COMMAND = '$fish'
    TIMER_TIMEOUT = 120.0
    activeTimer = None


    def timeoutFn() -> None:
        nonlocal activeTimer

        activeTimer = None

        print('[WARN] Timeout...')
        typeCommand()

    def typeCommand() -> None:
        nonlocal activeTimer

        APP.send('user', COMMAND)
        print(f"{datetime.today().strftime('[%H:%M:%S]')} {COMMAND}")

        activeTimer = threading.Timer(TIMER_TIMEOUT, timeoutFn)
        activeTimer.start()

    def listenChannel(msg) -> None:
        nonlocal activeTimer
        
        fromWho, userMsg = itemgetter('display-name', 'message')(msg)
        
        # Self explanatory
        cooldownBrackets = re.search(r'\((.+)\)', userMsg)
        if (
            (USERNAME not in userMsg) or 
            (RECEIVE_FROM != fromWho) or 
            (not cooldownBrackets)
        ): 
            return
        

        # If a fish has been caught
        fish = re.search(r'✨(.+)✨', userMsg)
        if fish:
            print('[FINISH] Fish has been caught!')

            APP.send('user', f'Ryba {fish.group(1)} złapana B)')

            # Clear the timer
            activeTimer.cancel()
            activeTimer = None

            sleep(1801)
            return


        # Filter only numbers
        nums = re.sub(
            r'[^0-9 ]',
            '',
            cooldownBrackets.group(1) 
        ).rstrip().split(' ')


        # Extract the time in seconds
        m, s = [ int(x) for x in (nums if len(nums) == 2 else [0, nums[0]]) ]

        seconds = m * 60 + s + 2
        s = seconds % 60
        m = floor(seconds / 60)

        # Clear the timer
        activeTimer.cancel()
        activeTimer = None

        print(f'[INFO] Next message in {m}m {s}s')
        threading.Timer(seconds, typeCommand).start()

    
    threading.Timer(2, typeCommand).start()

    print(f'[START] Started listening on channel {APP.getConfigInfo("channel")}')
    APP.listen('user', listenChannel)