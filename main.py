from flask import Flask, Response, jsonify
import base64
import os
import time
import random
import json
import requests
import flask

app = Flask(__name__)

proxies = {
    'http': 'socks5h://localhost:9050',
    'https': 'socks5h://localhost:9050'
}

endpoints = {'/door/info', 
             '/door/unlock', 
             '/card/register', 
             '/card/test/register',
             '/card/get/lastfail', 
             '/card/get/bysponsor', 
             '/card/get/all',
             '/card/get/byid',
             '/card/deactivate', 
             '/card/activate',
             '/card/adjust',
             }

hdr_token_name = 'Pecklock-Token'
hdr_performer_name = 'Pecklock-Performed-By'

def check_token(token):
    valid_tokens = os.getenv('VALID_TOKENS').split(':')
    return token not in valid_tokens, Response('Access denied', status=403)

def get_tor_url():
    return os.getenv('TOR_HIDDEN_SERVICE')

def init_tor_session():
    sess = requests.session()
    sess.proxies = proxies
    return sess

@app.before_request
def process():
    path = '/' + '/'.join([s for s in flask.request.path.split('/') if len(s) > 0])
    if len(path) > 1:
        is_valid_path = False
        for ep in endpoints:
            if path.startswith(ep):
                is_valid_path = True
                break
        if not is_valid_path:
            return Response('Invalid endpoint.', status=400)
    if not flask.request.headers.get(hdr_token_name):
        return Response('Invalid token.', status=400)
    if not flask.request.headers.get(hdr_performer_name):
        return Response('Performer not set.', status=400)

@app.route('/info')
def info():
    tor_url = get_tor_url()
    if not tor_url:
        return Response('Tor hidden service URL not set', status=400)
    non_tor_ip = requests.get('https://ident.me').text
    sess = init_tor_session()
    tor_ip = sess.get('https://ident.me').text
    test_tor = sess.get(tor_url).text
    r = sess.get(get_tor_url() + '/door/info', 
            headers={
                hdr_token_name: flask.request.headers.get(hdr_token_name),
                hdr_performer_name: flask.request.headers.get(hdr_performer_name)    
            })
    return Response(r.text, status=r.status_code)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):
    tor_url = get_tor_url()
    if not tor_url:
        return Response('Tor hidden service URL not set', status=400)
    sess = init_tor_session()
    r = sess.get(get_tor_url() + '/' + path, 
            headers={
                hdr_token_name: flask.request.headers.get(hdr_token_name),
                hdr_performer_name: flask.request.headers.get(hdr_performer_name)    
            })
    return Response(r.text, status=r.status_code)

if __name__ == '__main__':
    app.run(main)