from __future__ import print_function

# If modifying these scopes, delete the file token.json.
from EmailRepository import EmailRepository
from GMailClient import GMailClient
from GoogleAPICredentials import GoogleAPICredentials

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def main():

    # docker run -p 27017:27017 -d --name=gmail_db2 mongo:latest --noauth --bind_ip=0.0.0.0
    # babfe6ffdd39bc78a665e3544b62a1b33bdfebd3397981d2a93a1052ef3514f9

    credentials = GoogleAPICredentials(SCOPES)
    gmail = GMailClient(credentials)
    cache = EmailRepository("mongodb://localhost:27017")

    labels = gmail.get_labels()

    print('Labels:' + str(labels))

    counts, total = gmail.get_message_counts('CATEGORY_UPDATES', cache)

    print([rec[1] for rec in sorted([(-counts[email], (email, counts[email])) for email in counts])])
    print(total)

    groups = [
        'raiffeisen',
        'amazon',
        'google',
        'superjob',
        'aliexpress',
        'uber'
    ]

    for group in groups:
        from_group = cache.list_by_sender(group)
        print(f"From {group}: {len(from_group)}")


if __name__ == '__main__':
    main()
