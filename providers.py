import json
import os
from flask import Response
import requests
from rootClient import RootClient


class Providers:

    def __init__(self):
        self.host = "https://algocerca.cl/"
        self.root = RootClient()
        self.endpoint_id = "wp-json/wp/v2/users/me?_wpnonce=9467a0bf9c"
        #Para windows debieras setear el directorio de las imagenes
        self.img_folder = "/home/liviano/"#REMPLAZAR! Segun SO y USER

    def getter(self, endpoint, filter=""):
        token = self.root
        token = token.get_valid_token()
        url = self.host + endpoint
        get_request = requests.get(url, headers=token)
        print("URL: " + url)
        print("TOKEN: " + str(token))
        jsonResponse = Response(json.dumps(get_request.json()), mimetype='application/json')
        return jsonResponse

    # Metodo para realizar puts a la api
    def putter(self, user_token, endpoint, data):
        # token es el root_token (ojo)
        token = self.root
        token = token.get_valid_token()
        ide = str(self.myid(user_token))
        # el endpoint debiera abrir el espacio para recibir la id de usuario propietario del dato que se quiere actualizar
        url = self.host + endpoint + ide
        print(ide)
        response = requests.put(url, params=data, headers=token)
        jsonResponse = Response(json.dumps(response.json()), mimetype='application/json')
        return jsonResponse

    def poster(self, data, endpoint):
        token = self.root
        token = token.get_valid_token()
        host = self.host
        host = "https://algocerca.cl/"
        resPost = requests.post(url=host + endpoint, data=data, headers=token)
        jsonResponse = Response(json.dumps(resPost.json()), mimetype='application/json')
        # devuelve el json-callback del post
        return jsonResponse

    # Devuelve la id del arg token_user
    def myid(self, token_user):
        token = self.root
        token = token.get_valid_token()
        url = self.host + self.endpoint_id
        # el argumento token pasa como identifiacion/authorizacion
        bearer = {"Authorization": token_user}
        youAre = requests.get(url, headers=bearer)
        youAreJson = youAre.json()
        ide = youAreJson["id"]
        return ide

    def imgUL(self, filename):
        token = self.root
        token = token.get_valid_token()
        token = token["Authorization"]
        # posiblemente es necesario randomizar el nombre por posibles coliciones
        imgPath = self.img_folder+ filename
        data = open(imgPath, 'rb').read()
        fileName = os.path.basename(imgPath)
        print("ESTO ES EL TOKEN: " + str(token))
        print("ESTO ES EL FILENAME: " + str(fileName))
        res = requests.post(url='https://algocerca.cl/wp-json/wp/v2/media',
                            data=data,
                            headers={'Authorization': token, \
                                     'Content-Type': 'image/jpg', \
                                     'Content-Disposition': 'attachment; filename=%s' % fileName}, )
        # pp = pprint.PrettyPrinter(indent=4) ## print it pretty.
        # pp.pprint(res.json()) #this is nice when you need it
        jsonResponse = Response(json.dumps(res.json()), mimetype='application/json')
        return jsonResponse

    def putter_image(self, user_token, endpoint, data):
        token = self.root
        token = token.get_valid_token()
        ide = str(self.myid(user_token))
        url = self.host + endpoint
        response = requests.put(url, data=data, headers=token)
        jsonResponse = Response(json.dumps(response.json()), mimetype='application/json')
        print(response.text)
        return jsonResponse