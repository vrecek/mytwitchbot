from App import BotApp
from time import sleep
import json


def OptionsProcess(APP: BotApp, dictProxy) -> None:
    SET_ACTION = ['fish', 'boss']
    buff = ["", ""]


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

            sleep(.75)

            match(command):
                # `set` command
                case "set":
                    # Return if the length is different than 2, or action/switch is incorrect
                    if len(args) != 2 or args[0] not in SET_ACTION or args[1] not in ['on', 'off']:
                        APP.send("[❌] Incorrect `set` arguments")
                        return 

                    # Change switch on/off to True/False
                    action, switch = args
                    switch = True if switch == 'on' else False

                    # Update the proxy with a new value
                    dictProxy.update({
                        action: switch
                    })

                    print(f'[OPTIONS] Changed `{action}` to `{switch}')
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
                                    asciis = json.load(file)
                                    art_type = rest[0]

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
                            string = ' '.join(rest)

                            s = ' '.join([string for _ in range(int(first))])

                            APP.send(s)


                # `settings` command
                case "settings":
                    # Display SET_ACTION settings
                    # SET_ACTION keys must be in a dictProxy
                    s = ' '.join([f'{x}: {dictProxy[x]} | ' for x in SET_ACTION])[:-2]

                    APP.send(f'[ℹ️] {s}')


                case _:
                    APP.send("[❌] Incorrect command")
                    return


    while True:
        optionsChannel()