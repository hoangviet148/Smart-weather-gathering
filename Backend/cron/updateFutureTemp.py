from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import time

from socketIO.init import socketio
from controllers.SensorController import predictFutureTemp1, predictFutureTemp4

def updateFutureTempPrediction():
    print(socketio)
    socketio.emit("UpdateFutureTempPrediction", "1")
    print("updateFutureTempPrediction")
    # temp1 = predictFutureTemp1()
    # temp4 = predictFutureTemp4()
    # futureTemp = {
    #     "temp1": temp1,
    #     "temp4": temp4
    # }
    # socketio.emit("UpdateFutureTempPrediction", futureTemp)

    
def registerCron():
    print("register cron")
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(func=updateFutureTempPrediction, trigger="interval", seconds=30)
    scheduler.start()

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())

def registerCron1():
    print("register cron1")
    while(True):
        socketio.emit("UpdateFutureTempPrediction", "1")
        time.sleep(30000)
