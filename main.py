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

endpoints = {'tortest', 
             'unlock', 
             'last_failed_card', 
             'register_last_card', 
             'get_sponsored_cards', 
             'get_all_cards',
             'deactivate', 
             'activate',
             'adjust'}

token_name = 'Pecklock-Token'

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
    path_items = flask.request.path.split('/')
    for i in range(len(path_items)):
        if len(path_items[i]) > 0:
            break
    if path_items[i] not in endpoints:
        return Response('Invalid endpoint.', status=400)
    if not flask.request.headers.get(token_name):
        return Response('Invalid token.', status=400)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):
    tor_url = get_tor_url()
    if not tor_url:
        return Response('Tor hidden service URL not set', status=400)
    sess = init_tor_session()
    r = sess.get(get_tor_url() + '/' + path, headers={token_name: flask.request.headers.get('Pecklock-Token')})
    return Response(r.text, status=r.status_code)

"""
@app.route('/tortest/<token>')
def tortest(token):
    is_invalid, deny_resp = check_token(token)
    if is_invalid:
        return deny_resp
    tor_url = get_tor_url()
    if not tor_url:
        return Response('Tor hidden service URL not set', status=400)
    non_tor_ip = requests.get('https://ident.me').text
    sess = init_tor_session()
    tor_ip = sess.get('https://ident.me').text
    test_tor = sess.get(tor_url, headers={'Pecklock-Token': token}).text
    return Response("Hello %s (%s)\n%s" % (non_tor_ip, tor_ip, test_tor))



@app.route('/unlock/<token>/<name>')
def unlock(token, name):
    is_invalid, deny_resp = check_token(token)
    if is_invalid:
        return deny_resp
    sess = init_tor_session()
    r = sess.get(get_tor_url() + '/unlock/' + name, headers={'Pecklock-Token': flask.request.headers.get('Pecklock-Token')})
    return Response(r.text, status=r.status_code)

@app.route('/last_failed_card/<token>')
def last_failed_card(token):
    is_invalid, deny_resp = check_token(token)
    if is_invalid:
        return deny_resp
    sess = init_tor_session()
    r = sess.get(get_tor_url() + '/last_failed_card', headers={'Pecklock-Token': token})
    return Response(r.text, status=r.status_code)

@app.route('/register_last_card/<token>/<as_name>/<with_sponsor>')
def register_last_card(token, as_name, with_sponsor):
    is_invalid, deny_resp = check_token(token)
    if is_invalid:
        return deny_resp
    sess = init_tor_session()
    r = sess.get(get_tor_url() + '/register_last_card/' + as_name + '/' + with_sponsor, headers={'Pecklock-Token': token})
    return Response(r.text, status=r.status_code)

@app.route('/get_sponsored_cards/<token>/<sponsor>')
def get_sponsored_cards(token, sponsor):
    is_invalid, deny_resp = check_token(token)
    if is_invalid:
        return deny_resp
    sess = init_tor_session()
    r = sess.get(get_tor_url() + '/get_sponsored_cards/' + sponsor, headers={'Pecklock-Token': token})
    return Response(r.text, status=r.status_code)

@app.route('/deactivate/<token>/<sponsor_name>/<card_id>')
def deactivate(token, sponsor_name, card_id):
    is_invalid, deny_resp = check_token(token)
    if is_invalid:
        return deny_resp
    sess = init_tor_session()
    r = sess.get(get_tor_url() + '/deactivate/' + sponsor_name + '/' + card_id, headers={'Pecklock-Token': token})
    return Response(r.text, status=r.status_code)

@app.route('/activate/<token>/<sponsor_name>/<card_id>')
def activate(token, sponsor_name, card_id):
    is_invalid, deny_resp = check_token(token)
    if is_invalid:
        return deny_resp
    sess = init_tor_session()
    r = sess.get(get_tor_url() + '/activate/' + sponsor_name + '/' + card_id, headers={'Pecklock-Token': token})
    return Response(r.text, status=r.status_code)

@app.route('/adjust/<token>/<sponsor_name>/<card_id>/<minutes>/<hours>/<days>/<weeks>/<months>')
def adjust(token, sponsor_name, card_id, minutes, hours, days, weeks, months):
    is_invalid, deny_resp = check_token(token)
    if is_invalid:
        return deny_resp
    sess = init_tor_session()
    r = sess.get(get_tor_url() + '/adjust/' + sponsor_name + '/' + card_id + '/' + minutes + '/' + hours + '/' + days + '/' + weeks + '/' + months, headers={'Pecklock-Token': token})
    return Response(r.text, status=r.status_code)

@app.route('/get_all_cards/<token>/<web_name>')
def get_cards(token, web_name):
    is_invalid, deny_resp = check_token(token)
    if is_invalid:
        return deny_resp
    sess = init_tor_session()
    r = sess.get(get_tor_url() + '/admin/get_all_cards/' + web_name, headers={'Pecklock-Token': token})
    return Response(r.text, status=r.status_code)

@app.route('/')
def index():
    return Response('Hello world')
"""

if __name__ == '__main__':
    app.run(main)