import json
import os
from flask import Flask, request
from providers import Providers
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Esto está online'


@app.route('/myproducts/', methods=["GET"])
def myproducts():
    provs = Providers()
    token = request.headers["Authorization"]
    my_id = provs.myid(token)
    get_my_products = provs.getter("wp-json/wc/v2/products/?vendor=" + str(my_id))
    return get_my_products


# recibe la ide del vendedor, devuelve sus productos
# D.T. = validador de token
@app.route('/getproducts/<ide>', methods=["GET"])
def getProducts(ide):
    provs = Providers()
    product = provs.getter("wp-json/wc/v2/products?vendor=" + str(ide))
    return product


# lista todos los vendedores
@app.route('/getvendors/', methods=["GET"])
def getVendors():
    provs = Providers()
    vendors = provs.getter("wp-json/wcmp/v1/vendors")
    return vendors


# Wordpress es medio tontito para subir productos con imagenes,
# primero se sube la imagen (POST), luego el producto (POST)
# y recien ahí se unnen a través de un put al producto (PUT)

@app.route("/upload-product", methods=["POST"])
def upload_product():
    provs = Providers()
    token = {"Authorization": request.headers["Authorization"]}
    if request.method == "POST":
        endpoint = "wp-json/wc/v2/products/"
        token = request.headers["Authorization"]
        data = request.get_json()
        imageId = data["image_id"]
        del data["image_id"]
        # Asignamos la id del vendedor a la data, segun asociacion token<->id
        ide = provs.myid(token)
        data["vendor"] = ide
        # En algun momento tendremos que manipular los errores ^.^
        putImage = {"images": [{"id": imageId, "position": 1}]}
        # [Tallarin], lee la respuesta del post que envio para subir el producto
        response_post_product = provs.poster(data, endpoint)
        respuesta = json.loads(response_post_product.get_data().decode("utf-8"))
        print("Image id = " + str(putImage))
        print("Product id = " + str(respuesta["id"]))
        endpoint_with_id_product = "wp-json/wc/v2/products/" + str(respuesta["id"])
        finalPut = provs.putter_image(token, endpoint_with_id_product, data=json.dumps(putImage))
        return finalPut
    # Debiera ya estar pensando en una class validadores O.o
    else:
        if (request.method != "POST"):
            print("SOLO METODOS POST, PLIZ")
        else:
            print("Problemas con el token")


# FALTA PEDIR TOKEN PARA ESTE ENDPOINT o que sea un metodo en providers
@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():
    provs = Providers()
    token = {"Authorization": request.headers["Authorization"]}
    # Si el metodo es de tipo post y el token es valido-->
    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            # Guarda temporalmente la imagen recibida en el subdirectorio uploads
            image.save(os.path.join(provs.img_folder, image.filename))
            imgUpload = provs.imgUL(image.filename)
            # Borramos la imagen (era solo de pasada)
            if os.path.exists(provs.img_folder + image.filename):
                os.remove(provs.img_folder + image.filename)
            return imgUpload


if __name__ == '__main__':
    app.run()
