from App import BotApp
from time import sleep
from math import floor
from App import BotApp
from typing import Optional
import threading
import re


def FishProcess(APP: BotApp, dictProxy: dict) -> None:
    USERNAME:      str = APP.getConfigInfo('user_name')
    RECEIVE_FROM:  str = APP.getConfigInfo('receivers')["fish"]
    COMMAND:       str = '$fish'
    TIMER_TIMEOUT: float = 120.0
    fishToggle:    bool = True
    buff:          list = ['', '']
    activeTimer:   Optional[threading.Timer] = None


    def timeoutFn() -> None:
        nonlocal activeTimer

        activeTimer = None

        print('[FISH WARN] Timeout...')
        typeCommand()

    def typeCommand() -> None:
        nonlocal activeTimer

        if not dictProxy["fish"]:
            return

        # Send the message and print a timestamp
        APP.send(COMMAND)
        print(f"[FISH] {APP.getFormattedTime()} {COMMAND}")

        # Timeout if the script did not receive a valid answer
        activeTimer = threading.Timer(TIMER_TIMEOUT, timeoutFn)
        activeTimer.start()

    def fishChannel() -> None:
        nonlocal activeTimer
        nonlocal buff
        nonlocal fishToggle

        # Handle the fish toggling
        # # # # # # # # # # # # # # 
        # If toggled off
        if not dictProxy["fish"]: 
            fishToggle = False
            if activeTimer:
                activeTimer.cancel()
                activeTimer = None

            return
        
        # If toggled on
        if not fishToggle:
            fishToggle = True

            sleep(1)
            typeCommand()
        # # # # # # # # # # # # # # 
        
        # Get sender username and his message
        fromWho, userMsg = APP.getDictProxyValues(dictProxy)

        # Compare the values
        if not APP.canContinueLoop([fromWho, userMsg], buff):
            return
        buff = [fromWho, userMsg]

        # Self explanatory
        cooldownBrackets = re.search(r'\((.+)\)', userMsg)
        if (
            (USERNAME not in userMsg) or 
            (RECEIVE_FROM != fromWho) or 
            (not cooldownBrackets)
        ): 
            return

        # If a fish has been caught
        fish: Optional[Match[AnyStr]] = re.search(r'✨([^✨]+)✨', userMsg)
        if fish:
            print('[FISH FINISH] Fish has been caught!')

            sleep(.5)
            APP.send(f'Ryba {fish.group(1)} złapana B)')

            # Clear the timer
            activeTimer.cancel()
            activeTimer = None

            # Wait 30 minutes and re-type
            sleep(1802)
            typeCommand()

            return


        # Filter only numbers
        nums: list = re.sub(
            r'[^0-9 ]',
            '',
            cooldownBrackets.group(1) 
        ).rstrip().split(' ')


        # Extract the time in seconds
        m, s = [ int(x) for x in (nums if len(nums) == 2 else [0, nums[0]]) ]

        seconds: int = m * 60 + s + 2
        s = seconds % 60
        m = seconds // 60

        # Clear the timer
        activeTimer.cancel()
        activeTimer = None

        # Type the next message if the time pass
        print(f'[FISH INFO] Next message in {m}m {s}s')

        sleep(seconds)
        typeCommand()


    # Type the first message, and start listening
    threading.Timer(1, typeCommand).start()
    while True:
        fishChannel()