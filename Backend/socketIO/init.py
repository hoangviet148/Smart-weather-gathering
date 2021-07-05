from flask_socketio import SocketIO
import eventlet

socketio = SocketIO()

def createSocket(app):
    asyncMode = 'eventlet'
    socketio.init_app(app, asyncMode=asyncMode, cors_allowed_origins="*")

    return app