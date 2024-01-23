from App import BotApp
from multiprocessing import Manager
from processes.FishProc import FishProcess
from processes.BFHProc import BFHProcess
from processes.ListenProc import ListenProcess
from processes.OptionsProc import OptionsProcess

## config.json ##
# channel: str
# user: { name: str, oauth: str }
##             ##

# Leave as it is, eventually add a new entries
def getInitialProxy() -> dict:
    return {
        "fromWho": "", 
        "userMsg": "",
        "fish": True,
        "ffa": True,
        "boss": True,
        "heist": 1000
    }


if __name__ == '__main__':
    try:
        APP = BotApp('config.json') 

        APP.connect()
        print(f'[INFO] Established connection to the IRC')

        with Manager() as manager:
            responseDict = manager.dict(getInitialProxy())
            
            processes = [
                APP.newProcess(ListenProcess, "Listen", APP, responseDict),
                APP.newProcess(FishProcess, "Fish", APP, responseDict),
                APP.newProcess(BFHProcess, "Boss/FFA/Heist", APP, responseDict),
                APP.newProcess(OptionsProcess, "Options", APP, responseDict),
            ]

            APP.launchProcesses()


    except KeyboardInterrupt:
        APP.closeConnection()
        print('[EXIT] Exit requested')

    except Exception as e:
        APP.closeConnection()
        print(f'[ERROR] {str(e)}')