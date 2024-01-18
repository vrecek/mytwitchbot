from App import BotApp
from time import sleep


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
            split = userMsg[2:].split(' ')
            command, *args = split

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
                    string, num = args

                    if not num.isnumeric():
                        APP.send("[❌] Incorrect `say` number argument")
                        return

                    s = ""
                    for x in range(abs(int(num))):
                        s += f"{string} "

                    APP.send(s)


                # `settings` command
                case "settings":
                    # Display SET_ACTION settings
                    # SET_ACTION keys must be in a dictProxy
                    string = ''
                    for x in SET_ACTION:
                        string += f'{x}: {dictProxy[x]} | '

                    string = string[:-2]

                    APP.send(f'[ℹ️] {string}')


                case _:
                    APP.send("[❌] Incorrect command")
                    return


    while True:
        optionsChannel()