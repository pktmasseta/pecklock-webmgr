from flask import Flask, Response, request, jsonify
import base64
import os
import time
import random
import json
import requests

app = Flask(__name__)

proxies = {
    'http': 'socks5h://localhost:9050',
    'https': 'socks5h://localhost:9050'
}

def check_token(token):
    valid_tokens = os.getenv('VALID_TOKENS').split(':')
    return token not in valid_tokens, Response('Access denied', status=403)

def get_tor_url():
    return os.getenv('TOR_HIDDEN_SERVICE')

def init_tor_session():
    sess = requests.session()
    sess.proxies = proxies
    return sess

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
    test_tor = sess.get(tor_url).text
    return Response("Hello %s (%s)\n%s" % (non_tor_ip, tor_ip, test_tor))

@app.route('/unlock/<token>/<name>')
def unlock(token, name):
    is_invalid, deny_resp = check_token(token)
    if is_invalid:
        return deny_resp
    sess = init_tor_session()
    r = sess.get(get_tor_url() + '/unlock/' + name)
    return Response(r.text, status=r.status_code)

@app.route('/last_failed_card/<token>')
def last_failed_card(token):
    is_invalid, deny_resp = check_token(token)
    if is_invalid:
        return deny_resp
    sess = init_tor_session()
    r = sess.get(get_tor_url() + '/last_failed_card')
    return Response(r.text, status=r.status_code)

@app.route('/register_last_card/<token>/<as_name>/<with_sponsor>')
def register_last_card(token, as_name, with_sponsor):
    is_invalid, deny_resp = check_token(token)
    if is_invalid:
        return deny_resp
    sess = init_tor_session()
    r = sess.get(get_tor_url() + '/register_last_card/' + as_name + '/' + with_sponsor)
    return Response(r.text, status=r.status_code)

@app.route('/get_sponsored_cards/<token>/<sponsor>')
def get_sponsored_cards(token, sponsor):
    is_invalid, deny_resp = check_token(token)
    if is_invalid:
        return deny_resp
    sess = init_tor_session()
    r = sess.get(get_tor_url() + '/get_sponsored_cards/' + sponsor)
    return Response(r.text, status=r.status_code)

@app.route('/deactivate/<token>/<sponsor_name>/<card_id>')
def deactivate(token, sponsor_name, card_id):
    is_invalid, deny_resp = check_token(token)
    if is_invalid:
        return deny_resp
    sess = init_tor_session()
    r = sess.get(get_tor_url() + '/deactivate/' + sponsor_name + '/' + card_id)
    return Response(r.text, status=r.status_code)

@app.route('/activate/<token>/<sponsor_name>/<card_id>')
def activate(token, sponsor_name, card_id):
    is_invalid, deny_resp = check_token(token)
    if is_invalid:
        return deny_resp
    sess = init_tor_session()
    r = sess.get(get_tor_url() + '/activate/' + sponsor_name + '/' + card_id)
    return Response(r.text, status=r.status_code)

@app.route('/adjust/<token>/<sponsor_name>/<card_id>/<minutes>/<hours>/<days>/<weeks>/<months>')
def adjust(token, sponsor_name, card_id, minutes, hours, days, weeks, months):
    is_invalid, deny_resp = check_token(token)
    if is_invalid:
        return deny_resp
    sess = init_tor_session()
    r = sess.get(get_tor_url() + '/adjust/' + sponsor_name + '/' + card_id + '/' + minutes + '/' + hours + '/' + days + '/' + weeks + '/' + months)
    return Response(r.text, status=r.status_code)

@app.route('/')
def index():
    return Response('Hello world')

if __name__ == '__main__':
    app.run(main)