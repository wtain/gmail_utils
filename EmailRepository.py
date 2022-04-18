from pprint import pprint

from pymongo import MongoClient

from track_time import track_time


class EmailRepository:

    def __init__(self, url):
        self.client = MongoClient(url)
        self.gmail_cache = self.client.gmail_cache
        serverStatusResult = self.gmail_cache.command("serverStatus")
        pprint(serverStatusResult)

        self.emails = self.gmail_cache.emails

    def get_message(self, id):
        return self.emails.find_one({'id': id})

    def store_message(self, message):
        self.emails.insert_one(message)

    @track_time
    def get_page_count(self, page_size: int) -> int:
        return (self.emails.count_documents({})-1) // page_size + 1

    @staticmethod
    def get_header(msg, name: str) -> str:
        try:
            return [h['value'] for h in msg.get('payload').get('headers') if h['name'].lower() == name.lower()][0]
        except IndexError as e:
            print(msg, name, e)

    @staticmethod
    def convert_message(msg):
        return {
                 "sender": EmailRepository.get_header(msg, 'From'),
                 "subject": EmailRepository.get_header(msg, 'Subject'),
                 "date": EmailRepository.get_header(msg, 'Date'),
                 "labels": msg.get("labelIds"),
                 "snippet": msg.get("snippet"),
               }

    @staticmethod
    def filter_by_sender(sender: str):
        return {
                "payload.headers": {
                    "$elemMatch": {
                        "name": "From",
                        "value": {
                            "$regex": f".*{sender}.*"
                        }
                    }
                }
            }

    @staticmethod
    def apply_pagination(iterator, page_number: int, page_size: int):
        # if page_number == 1:
        #     return iterator.limit(page_size)
        nskip = (page_number-1)*page_size
        print(f"Skipping {nskip}, page size = {page_size}")
        return iterator.skip(nskip).limit(page_size)

    @track_time
    def list_page(self, page_size: int, page_number: int):
        return list(map(self.convert_message,
                        self.apply_pagination(self.emails.find(), page_number, page_size)))

    @track_time
    def list_all(self):
        return list(map(self.convert_message, self.emails.find()))

    @track_time
    def list_by_sender(self, sender: str):
        # return list(self.emails.find({"payload.headers.name": "From", "payload.headers.value": {"$regex": f".*{sender}.*"}}))
        # return list(self.emails.find({"payload.headers": {"name": "From", "value": {"$regex": f".*{sender}.*"}}}))
        return list(map(self.convert_message, self.emails.find(
            self.filter_by_sender(sender)
        )))

    @track_time
    def list_page_by_sender(self, sender: str, page_num: int, page_size: int):
        return list(map(EmailRepository.convert_message,
                        EmailRepository.apply_pagination(
                            self.emails.find(
                                EmailRepository.filter_by_sender(sender)),
                            page_num, page_size)))

    @track_time
    def get_page_count_by_sender(self, page_size: int, sender: str) -> int:
        return (self.emails.count_documents(EmailRepository.filter_by_sender(sender)) - 1) // page_size + 1
