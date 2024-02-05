from App import BotApp
from multiprocessing import Manager
from processes.FishProc import FishProcess
from processes.BFHProc import BFHProcess
from processes.ListenProc import ListenProcess
from processes.OptionsProc import OptionsProcess
from processes.MentionProc import MentionProcess
from time import time


## config.json ##
# channel: str
# user: { name: str, oauth: str }
##             ##

# Leave it as it is, eventually add a new entries
def getInitialProxy() -> dict:
    return {
        "fromWho": "", 
        "userMsg": "",

        "fish": True,
        "ffa": True,
        "boss": True,
        "heist": 1000,

        "startingTime": int( time() * 1000 )
    }


if __name__ == '__main__':
    try:
        APP: BotApp = BotApp('config.json') 

        APP.connect()
        print(f'[INFO] Established connection to the IRC')

        # Create the IPC proxy
        with Manager() as manager:
            responseDict: dict = manager.dict(getInitialProxy())
            
            # Create your processes
            APP.newProcess(ListenProcess, "Listen", APP, responseDict)
            APP.newProcess(FishProcess, "Fish", APP, responseDict)
            APP.newProcess(BFHProcess, "Boss/FFA/Heist", APP, responseDict)
            APP.newProcess(OptionsProcess, "Options", APP, responseDict)
            APP.newProcess(MentionProcess, "Mention", APP, responseDict)

            # Launch processes that you created
            APP.launchProcesses()


    # Ctrl + C
    except KeyboardInterrupt:
        APP.closeConnection()
        print('[EXIT] Exit requested')

    except Exception as e:
        APP.closeConnection()
        print(f'[ERROR] {str(e)}')