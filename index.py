from App import BotApp
from multiprocessing import Manager
from processes.FishProc import FishProcess
from processes.BossProc import BossProcess
from processes.ListenProcess import ListenProcess


if __name__ == '__main__':
    try:
        APP = BotApp('config.json') 

        APP.connect()
        print(f'[INFO] Established connection to the IRC')

        with Manager() as manager:
            responseDict = manager.dict(APP.getDictProxyResponse({}, True))
            processes = [
                APP.newProcess(ListenProcess, "Listen", APP, responseDict),
                APP.newProcess(FishProcess, "Fish", APP, responseDict),
                APP.newProcess(BossProcess, "Boss", APP, responseDict)
            ]

            APP.launchProcesses()
        
    except KeyboardInterrupt:
        APP.closeConnection()
        print('[EXIT] Exit requested')

    except Exception as e:
        APP.closeConnection()
        print(f'[ERROR] {str(e)}')