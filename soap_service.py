from spyne import Application, rpc, ServiceBase, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from flask import Flask, request, Response

class HelloService(ServiceBase):
    @rpc(Unicode, _returns=Unicode)
    def say_hello(ctx, name):
        return f"Hello, {name}!"

# Spyne Application
application = Application(
    [HelloService],
    tns='spyne.examples.hello',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

# WSGI Application
wsgi_app = WsgiApplication(application)

# Flask app
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def soap_service():
    # Define start_response collector
    response_data = {}

    def start_response(status, response_headers, exc_info=None):
        response_data['status'] = status
        response_data['headers'] = response_headers
        return response_data.setdefault('body', []).append

    # Call the WSGI app
    result = wsgi_app(request.environ, start_response)
    response_body = b"".join(result)

    # Return a proper Flask response
    status_code = int(response_data['status'].split()[0])
    headers = dict(response_data['headers'])

    return Response(response=response_body, status=status_code, headers=headers)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
