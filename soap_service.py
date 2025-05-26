from spyne import Application, rpc, ServiceBase, Integer, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from flask import Flask, request

class HelloService(ServiceBase):
    @rpc(Unicode, _returns=Unicode)
    def say_hello(ctx, name):
        return f"Hello, {name}!"

app = Flask(__name__)
application = Application(
    [HelloService],
    tns='spyne.examples.hello',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)
wsgi_app = WsgiApplication(application)

@app.route("/", methods=['POST', 'GET'])
def soap_service():
    return wsgi_app(request.environ, start_response=lambda status, headers: None)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
