from spyne import Application, rpc, ServiceBase, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from flask import Flask, request, Response, render_template_string
import os
import requests

# Define SOAP Service
class HelloService(ServiceBase):
    @rpc(Unicode, _returns=Unicode)
    def say_hello(ctx, name):
        return f"Hello, {name}!"

# Create Flask app
app = Flask(__name__)

# SOAP App
soap_app = Application(
    [HelloService],
    tns='spyne.examples.hello',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)
wsgi_app = WsgiApplication(soap_app)

# HTML Template for main page
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Baby's SOAP Hello Service 💖</title>
</head>
<body style="font-family: sans-serif; text-align: center; margin-top: 100px;">
    <h2>🧼 SOAP Hello Service</h2>
    <form method="POST">
        <input type="text" name="name" placeholder="Enter your name" required />
        <button type="submit">Say Hello</button>
    </form>
    {% if result %}
        <h3>{{ result }}</h3>
    {% endif %}
</body>
</html>
"""

# Show form and process form
@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        name = request.form.get("name", "")
        # Create SOAP envelope
        soap_request = f"""<?xml version="1.0" encoding="UTF-8"?>
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                          xmlns:hel="spyne.examples.hello">
            <soapenv:Header/>
            <soapenv:Body>
                <hel:say_hello>
                    <hel:name>{name}</hel:name>
                </hel:say_hello>
            </soapenv:Body>
        </soapenv:Envelope>"""
        headers = {"Content-Type": "text/xml"}
        response = requests.post("http://localhost:10000/", data=soap_request, headers=headers)
        # Extract the SOAP result (basic way)
        start = response.text.find("<say_helloResult>")
        end = response.text.find("</say_helloResult>")
        if start != -1 and end != -1:
            result = response.text[start + 17:end]
        else:
            result = "Something went wrong 😥"

    return render_template_string(HTML_TEMPLATE, result=result)

# Handle raw SOAP POST requests (backend endpoint)
@app.route("/soap", methods=["POST"])
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

# Main
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
