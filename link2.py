from flask import Flask, redirect, request
import requests
import configparser
import requests.auth
import json
from data import secret_key, client_id

redirect_uri = r"http://127.0.0.1:5000/app"
auth_url = r"https://www.linkedin.com/uas/oauth2/authorization"
api_url = r"https://www.linkedin.com/uas/oauth2/accessToken"

application = Flask(__name__)

@application.route("/")
def index():

    reqtext = auth_url + "?response_type=code" +\
	"&client_id=" + client_id +\
    "&redirect_uri=" + redirect_uri +\
	"&state=987654321" 
       
    return redirect(reqtext, 302)

@application.route("/app", methods=['GET'])
def app():
    """
    Getting authorization_code
    """
    confirm_code = request.args.get('code')
    if confirm_code is None:
        return "bad request"
    print(confirm_code)
    """auth = (client_id, secret_key)"""
    url = api_url 
    params = {'grant_type': 'authorization_code', 'code': confirm_code, 'redirect_uri': redirect_uri, 'client_id': client_id, 'client_secret': secret_key}
    """
    Getting an access_token
    """
    response = requests.post(url=url, data=params)
    print(response)
    if response.status_code != 200:
        return "Wrong auth"
    print ('------')
    for val in response:
        print (val)
    print ('------')
    access_token = response.json()["access_token"]

    """
    Using paypal REST API
    """
    url = r"https://api.linkedin.com/v1/people/~?format=json"
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + access_token}

    response = requests.get(url=url, headers=headers)
    print(response)
    if response.status_code != 200:
        return "Internal request error"

    text = response.text
    return text

if __name__ == "__main__":
    application.run()
