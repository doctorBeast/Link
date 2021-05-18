from Link import app, socketIO

socketIO.run(app=app, host="0.0.0.0", debug=True)
