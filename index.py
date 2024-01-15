from App import BotApp
from multiprocessing import Process
from processes.FishProc import FishProcess


if __name__ == '__main__':
    try:
        APP = BotApp('config.json') 

        APP.connect()
        print(f'[INFO] Established connection to the IRC')


        processes = [
            Process(target=FishProcess, args=(APP,))
        ]


        for proc in processes:
            proc.daemon = True
            proc.start()

        for proc in processes:
            proc.join()


    except KeyboardInterrupt:
        APP.closeConnection()
        print('[EXIT] Exit requested')

    except Exception as e:
        APP.closeConnection()
        print(f'[ERROR] {str(e)}')