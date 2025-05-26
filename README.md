
# 🧼 Hello SOAP Service

This is a simple SOAP-based web service built using Python, Flask, and Spyne, deployed on Render.com.

## 🚀 Features

* Accepts a name via SOAP or web form and replies with a friendly `Hello <name>!`
* Deployed on Render (live!)
* Simple HTML frontend to test the service easily

## 🌐 Live Demo

👉 Web Form (Frontend):
[https://wsdl-soap-service-oegj.onrender.com/hello](https://wsdl-soap-service-oegj.onrender.com/hello)

👉 SOAP Endpoint (POST):
[https://wsdl-soap-service-oegj.onrender.com/](https://wsdl-soap-service-oegj.onrender.com/)

## 🧼 SOAP Request Example

Here’s an example SOAP request body to use with tools like SoapUI or Postman:

```xml
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:hel="spyne.examples.hello">
   <soapenv:Header/>
   <soapenv:Body>
      <hel:say_hello>
         <hel:name>Baby</hel:name>
      </hel:say_hello>
   </soapenv:Body>
</soapenv:Envelope>
```

## 🧪 How to Run Locally

```bash
# Clone the repo
git clone https://github.com/your-username/your-repo.git
cd your-repo

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
python soap_service.py
```

Then open your browser and go to `http://localhost:10000/hello`

## 🛠️ Tech Stack

* Python 3.x
* Flask
* Spyne
* Render.com

