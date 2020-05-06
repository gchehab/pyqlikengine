from websocket import create_connection
from jwt import JWT, jwk_from_pem
import ssl
import os
from datetime import datetime, timedelta

class EngineCommunicator:

    def __init__(self, url, debug=False):
        self.url = url
        self.ws = create_connection(self.url)
        self.session = self.ws.recv()  # Holds session object. Required for Qlik Sense Sept. 2017 and later
        if debug:
            print ("> " + self.session)
       
    @staticmethod
    def send_call(self, call_msg):
        if debug:
            print ("> " + call_msg)
        self.ws.send(call_msg)

        # Qlik sometimes returns more than one json response for a single request -- perhaps should use an async socket.
        # Might be needed to append all responses to returned data in a future review
        while True:
            data = self.ws.recv()
            if debug:
                print("< " + data)
            if ('result' in data or 'error' in data):
                break
        return data

    @staticmethod
    def close_qvengine_connection(self):
        self.ws.close()

class SecureEngineCommunicator(EngineCommunicator):

    def __init__(self, senseHost, proxyPrefix, userDirectory, userId, privateKeyPath, userGroup=None, ignoreCertErrors=False, rootCA=None, ):
        self.url = "wss://" + senseHost + "/" + proxyPrefix + "/app/engineData"
        sslOpts = {}
        if ignoreCertErrors:
            sslOpts = {"cert_reqs": ssl.CERT_NONE}
        else:
            if rootCA is not None:
                sslOpts = {'ca_certs': rootCA}
            else:
                sslOpts = None
        
        payload = {'user': userId, 'directory': userDirectory}
        if userGroup is not None:
            payload['group'] = userGroup

        privateKey = jwk_from_pem(open(privateKeyPath,"rb").read())
        token=JWT().encode(key=privateKey, alg='RS256',
                           payload=payload,
                           optional_headers={'exp': (datetime.utcnow() + timedelta(minutes=10)).isoformat()} )
               
        self.ws = create_connection(self.url, sslopt=sslOpts, header=['authorization: bearer ' + str(token)])
        self.session = self.ws.recv()
