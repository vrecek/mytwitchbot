from App import BotApp
from threading import Timer


def MiscProcess(APP: BotApp, dictProxy: dict) -> None:
    # Count the seconds since the program has started
    def uptimeInterval() -> None:
        Timer(1.0, uptimeInterval).start()

        dictProxy["uptime"] += 1


    uptimeInterval()
