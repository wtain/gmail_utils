from flask import Flask, json, request
from flask_cors import CORS

from EmailRepository import EmailRepository
from log_call import LogCall

api = Flask(__name__)
CORS(api)
cache = EmailRepository("mongodb://localhost:27017")


@LogCall
@api.route('/emails', methods=['GET'])
def get_emails():
    return json.dumps(cache.list_all())


@LogCall
@api.route('/page', methods=['GET'])
def get_emails_page():
    page_num = request.args.get('page', default=1, type=int)
    page_size = request.args.get('page_size', default=20, type=int)
    return json.dumps(cache.list_page(page_size, page_num))


@LogCall
@api.route('/page_count', methods=['GET'])
def get_emails_page_count():
    page_size = request.args.get('page_size', default=20, type=int)
    return json.dumps(cache.get_page_count(page_size))


@LogCall
@api.route('/list_by_sender', methods=['GET'])
def get_emails_by_sender():
    sender = request.args.get('sender', type=str)
    return json.dumps(cache.list_by_sender(sender))


@LogCall
@api.route('/list_page_by_sender', methods=['GET'])
def get_emails_page_by_sender():
    page_num = request.args.get('page', default=1, type=int)
    page_size = request.args.get('page_size', default=20, type=int)
    sender = request.args.get('sender', type=str)
    return json.dumps(cache.list_page_by_sender(sender, page_num, page_size))


@LogCall
@api.route('/page_count_by_sender', methods=['GET'])
def get_emails_page_count_by_sender():
    page_size = request.args.get('page_size', default=20, type=int)
    sender = request.args.get('sender', type=str)
    return json.dumps(cache.get_page_count_by_sender(page_size, sender))


if __name__ == '__main__':
    api.run()
