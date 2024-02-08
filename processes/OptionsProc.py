from App import BotApp
from math import floor
from time import sleep
from subprocess import run
from signal import SIGKILL
from time import time
import json
import os 


def OptionsProcess(APP: BotApp, dictProxy: dict) -> None:
    SET_ACTION: list = ['fish', 'boss', 'ffa', 'heist']
    buff:       list = ["", ""]


    def optionsChannel():
        nonlocal buff    

        fromWho, userMsg = APP.getDictProxyValues(dictProxy)

        # Compare the values
        if not APP.canContinueLoop([fromWho, userMsg], buff):
            return
        buff = [fromWho, userMsg]


        # Change the app options through a chat
        # Check if the user was the sender, and if he typed a command prefix
        if fromWho == APP.getConfigInfo("user_name") and userMsg[0:2] == '>>':
            command, *args = userMsg[2:].split(' ')

            sleep(1)

            match (command):
                # `set` command
                case "set":
                    # Return if the length is different than 2, or action/switch is incorrect
                    if len(args) != 2 or args[0] not in SET_ACTION:
                        APP.send("[❌] Incorrect `set` arguments")
                        return 

                    # Change switch on/off to True/False
                    action, switch = args

                    # Heist
                    if action == 'heist':
                        if switch.isnumeric():
                            switch = int(switch)
                        elif switch == 'off':
                            switch = False
                        else:
                            APP.send("[❌] Incorrect `set heist` arguments")
                            return 
                        
                    # Other option
                    else:
                        if switch not in ['on', 'off']:
                            APP.send("[❌] Incorrect `set` arguments")
                            return 

                        switch = True if switch == 'on' else False


                    # Update the proxy with a new value
                    dictProxy.update({
                        action: switch
                    })

                    print(f'[OPTIONS] Changed `{action}` to `{switch}`')
                    APP.send(f"[✅] Changed `{action}` to `{switch}`")


                # `say` command
                case "say":
                    if len(args) < 2:
                        APP.send("[❌] Incorrect `say` arguments")
                        return

                    first, *rest = args

                    match (first):
                        # Print an ASCII art
                        case 'art':
                            try:
                                with open('data/ascii.json') as file:
                                    # Open the JSON art file and search for an art
                                    asciis:   dict = json.load(file)
                                    art_type: str = rest[0]

                                    if art_type not in asciis:
                                        APP.send("[❌] Art not found")
                                    else:
                                        APP.send(asciis[art_type])

                            except:
                                APP.send("[❌] Error loading JSON")


                        # Say a sentence
                        case _:
                            # `first` must be a positive number
                            if not first.isnumeric():
                                APP.send("[❌] Incorrect `say` arguments")
                                return
                            
                            # Combine the `string` array into a one string
                            string:  str = ' '.join(rest)
                            fullStr: str = (f'{string} ' * int(first)).rstrip()

                            APP.send(fullStr)


                # `uptime` command
                case "uptime":
                    # Calculate how much time has passed since the beginning
                    startingTime: int = dictProxy["startingTime"]
                    currentTime:  int = int( time() * 1000 )

                    totalSeconds: int = (currentTime - startingTime) // 1000

                    # Calculate total hours, minutes and seconds
                    h: int = totalSeconds // 3600
                    m: int = totalSeconds // 60 % 60
                    s: int = totalSeconds % 60

                    time_str: str = ''

                    # Reduce redundant code
                    # Determine whether any hours, minutes, seconds have passed, if yes, append them to the string
                    def join_time(val: int, letter: str) -> None:
                        nonlocal time_str
                        if val:
                            time_str += f'{val}{letter} '

                    join_time(h, 'h')
                    join_time(m, 'm')
                    join_time(s, 's')

                    APP.send(f'[ℹ️] Uptime: {time_str}')


                # `settings` command
                case "settings":
                    # Display SET_ACTION settings
                    # SET_ACTION keys must be in a dictProxy
                    s: str = ' '.join([f'{x}: {dictProxy[x]} | ' for x in SET_ACTION])[:-2]

                    APP.send(f'[ℹ️] {s}')


                # `exit` command
                case "exit":
                    # Run the command to get the current processes
                    shstr: str = "ps -u | grep 'python3 index.py' | awk '{print $2}'"
                    sh:    str = run(shstr, capture_output=True, shell=True).stdout.decode()

                    # Split the PIDs to the array, and remove the main PID
                    arr: list = sh.rstrip().split('\n')
                    arr.remove(str( os.getppid() ))

                    for pid in arr:
                        pid: int = int(pid)

                        # Kill every process
                        try:
                            if pid == os.getpid():
                                print('[EXIT] Exit input')

                            os.kill(pid, SIGKILL)

                        except Exception:
                            continue


                case _:
                    APP.send("[❌] Incorrect command")
                    return
                    
            sleep(1)


    while True:
        optionsChannel()