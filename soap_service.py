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

# Flask route to handle SOAP requests
@app.route("/", methods=['POST', 'GET'])
def soap_service():
    def start_response(status, headers):
        response.status = status
        for header in headers:
            response.headers[header[0]] = header[1]

    response = Response()
    response.data = wsgi_app(request.environ, start_response)
    return response

# Entry point
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
