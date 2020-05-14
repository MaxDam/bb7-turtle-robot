from flask import Flask, request
from waitress import serve
import os

#inizializza l'interfaccia rest
app = Flask(__name__)

#ping
@app.route('/ping', methods=['GET'])
def ping():
    return "it works!", 200, {'ContentType':'text/html'} 

#command to bby
@app.route('/cmd/<cmd>', methods=['GET'])
def executeCommand(cmd):
    os.system("python bb7.py " + cmd)
    return "", 200, {'ContentType':'text/html'} 

#main
if __name__ == '__main__':
    #avvia il server waitress in ascolto
    serve(app, host="0.0.0.0", port=8090)