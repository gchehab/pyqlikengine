from websocket import create_connection
import jwt
import ssl


class EngineCommunicator:

    def __init__(self, url):
        self.url = url
        self.ws = create_connection(self.url)
        self.session = self.ws.recv()  # Holds session object. Required for Qlik Sense Sept. 2017 and later
       
    @staticmethod
    def send_call(self, call_msg):
        self.ws.send(call_msg)

        # Qlik sometimes returns more than one json response for a sinclu request -- perhaps should use an async socker?
        while True:
            data = self.ws.recv()
            if ('result' in data or 'error' in data):
                break
        return data

    @staticmethod
    def close_qvengine_connection(self):
        self.ws.close()

class SecureEngineCommunicator(EngineCommunicator):

    def __init__(self, senseHost, proxyPrefix, userDirectory, userId, privateKeyPath, ignoreCertErrors=False):
        self.url = "wss://" + senseHost + "/" + proxyPrefix + "/app/engineData"
        sslOpts = {}
        if ignoreCertErrors:
            sslOpts = {"cert_reqs": ssl.CERT_NONE}
        
        privateKey = open(privateKeyPath).read()
        token = jwt.encode({'user': userId, 'directory': userDirectory}, privateKey, algorithm='RS256')

        self.ws = create_connection(self.url, sslopt=sslOpts, header=['Authorization: BEARER ' + str(token)])
        self.session = self.ws.recv()