import time
import json
import os
from flask import Flask, request, send_file

ISSUER = 'mock-auth-server'
LIFE_SPAN = 1800

app = Flask(__name__)

@app.route('/')
def health():
    return 'healthy'

@app.route('/getDoc')
def getDoc():
    # Checks if the access token is present and valid. 
    auth_header = request.headers.get('Authorization')
    if 'Bearer' not in auth_header:
        return json.dumps({
            'error': 'Access token does not exist.'
        }), 400
  
    access_token = auth_header[7:]

    if access_token and verify_access_token(access_token):
        name = request.args.get('name')
        return return_doc(name)
    else:
        return json.dumps({
            'error': 'Access token is invalid.'
        }), 400

@app.route('/getListDocs')
def getListDocs():
    # Checks if the access token is present and valid. 
    auth_header = request.headers.get('Authorization')
    if 'Bearer' not in auth_header:
        return json.dumps({
            'error': 'Access token does not exist.'
        }), 400
  
    access_token = auth_header[7:]

    if access_token and verify_access_token(access_token):
        return return_doc_list()
    else:
        return json.dumps({
            'error': 'Access token is invalid.'
        }), 400

@app.route('/oauth/token', methods = ['POST'])
def getToken():
    client_id = request.form.get('client_id')
    client_secret = request.form.get('client_secret')
    if None in [client_id, client_secret]:
        return json.dumps({
            "error": "invalid_request"
        }), 400
    if not authenticate_client(client_id, client_secret):
        return json.dumps({
            "error": "invalid_client"
        }), 400
    access_token = generate_access_token()
    return json.dumps({ 
        "access_token": access_token,
        "token_type": "JWT",
        "expires_in": LIFE_SPAN
    })

def return_doc(name):
    try:
        return send_file("documents/"+name)
    except Exception as e:
        return json.dumps({"error":str(e)})

def return_doc_list():
    files = os.listdir('documents')
    documents = []
    for x in files:
        documents.append({
            "name": x
        })
    return json.dumps({
        "documents": documents
    })

def generate_access_token():
    payload = {
        "iss": ISSUER,
        "exp": time.time() + LIFE_SPAN,
    }

    access_token = "accesstoken"
    return access_token

def authenticate_client(client_id, client_secret):
    return True

def verify_access_token(access_token):
    if access_token == "accesstoken":
        return True
    return False

if __name__ == '__main__':
   app.run(host='0.0.0.0')