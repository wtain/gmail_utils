from functools import partial

from flask import Flask, json, request
from flask_cors import CORS, cross_origin

from EmailRepository import EmailRepository


api = Flask(__name__)
CORS(api)
cache = EmailRepository("mongodb://localhost:27017")


class log_call:

    def __init__(self, function):
        self.function = function

    def __get__(self, instance, owner):
        return partial(self.__call__, instance)

    def __call__(self, obj, *args, **kwargs):
        print("Calling " + self.function.__name__)
        print("Parameters: " + str(*args))
        result = self.function(obj, *args, **kwargs)
        if type(result) is list:
            print("Returning list len=" + len(result))
        else:
            print("Returning " + result)
        return result


@log_call
@api.route('/emails', methods=['GET'])
def get_emails():
    return json.dumps(cache.list_all())


@log_call
@api.route('/page', methods=['GET'])
def get_emails_page():
    page_num = request.args.get('page', default=1, type=int)
    page_size = request.args.get('page_size', default=20, type=int)
    return json.dumps(cache.list_page(page_size, page_num))


@log_call
@api.route('/page_count', methods=['GET'])
def get_emails_page_count():
    page_size = request.args.get('page_size', default=20, type=int)
    return json.dumps(cache.get_page_count(page_size))


@log_call
@api.route('/list_by_sender', methods=['GET'])
def get_emails_by_sender():
    sender = request.args.get('sender', type=str)
    return json.dumps(cache.list_by_sender(sender))


@log_call
@api.route('/list_page_by_sender', methods=['GET'])
def get_emails_page_by_sender():
    page_num = request.args.get('page', default=1, type=int)
    page_size = request.args.get('page_size', default=20, type=int)
    sender = request.args.get('sender', type=str)
    return json.dumps(cache.list_page_by_sender(sender, page_num, page_size))


@log_call
@api.route('/page_count_by_sender', methods=['GET'])
def get_emails_page_count_by_sender():
    page_size = request.args.get('page_size', default=20, type=int)
    sender = request.args.get('sender', type=str)
    return json.dumps(cache.get_page_count_by_sender(page_size, sender))


if __name__ == '__main__':
    api.run()
