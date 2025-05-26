from spyne import Application, rpc, ServiceBase, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from flask import Flask, request, Response
import os

# Define the SOAP service
class HelloService(ServiceBase):
    @rpc(Unicode, _returns=Unicode)
    def say_hello(ctx, name):
        return f"Hello, {name}!"

# Flask app
app = Flask(__name__)

# Create the Spyne application
soap_app = Application(
    [HelloService],
    tns='spyne.examples.hello',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

# Wrap with WSGI application
wsgi_app = WsgiApplication(soap_app)
@app.route("/hello")
def index():
    return "SOAP Service is running. Use a SOAP client to POST to /"

# Flask route to handle SOAP requests
@app.route("/", methods=["GET", "POST"])
def soap_service():
    response = []

    def start_response(status, headers):
        nonlocal response
        response.append(("status", status))
        response.append(("headers", headers))

    result = wsgi_app(request.environ, start_response)
    status = dict(response).get("status", "500 INTERNAL SERVER ERROR")
    headers = dict(response).get("headers", [])

    return Response(result, status=status, headers=dict(headers))


# Entry point
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
