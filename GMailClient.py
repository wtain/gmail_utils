import re
from collections import defaultdict

from GoogleAPICredentials import GoogleAPICredentials
from track_time import track_time


class GMailClient:

    def __init__(self, credentials: GoogleAPICredentials):
        self.service = credentials.build_api('gmail')

    @track_time
    def get_labels(self):
        results = self.service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])
        return list(label['name'] for label in labels)

    @track_time
    def list_messages(self, labelId, nextPageToken=None):
        if nextPageToken:
            messages = self.service.users().messages().list(userId='me', labelIds=labelId, pageToken=nextPageToken, maxResults=500).execute()
        else:
            messages = self.service.users().messages().list(userId='me', labelIds=labelId, maxResults=500).execute()
        return messages

    @track_time
    def get_sender(self, id, cache):
        message = cache.get_message(id)
        if not message:
            message = self.service.users().messages().get(userId='me', id=id, metadataHeaders=['from']).execute()
            cache.store_message(message)
        from_headers = list(filter(lambda h: h['name'] == 'From', message['payload']['headers']))
        sender = "EMPTY"
        if from_headers:
            sender = from_headers[0]['value']
            match = re.search(r'[A-Za-z0-9\._\-]+[@][A-Za-z0-9\._\-]+[.]\w{2,3}', sender)
            if match:
                sender = match.group()
            else:
                print("*** WARNING: Can't match sender email: " + sender)
        else:
            print("*** WARNING: No sender: " + str(from_headers))
        return sender

    @track_time
    def get_message_counts(self, labelId, cache):
        counts = defaultdict(int)
        messages = self.list_messages(labelId)
        total = 0

        while messages:
            for message in messages['messages']:
                sender = self.get_sender(message['id'], cache)
                counts[sender] = counts[sender] + 1

            total += len(messages['messages'])
            print(total)
            if 'nextPageToken' not in messages:
                break
            messages = self.list_messages(labelId, messages['nextPageToken'])
        return counts, total