# -args(post)
from date import convert_date
from number import geez_num
from build_basic import build_basic
from datetime import date
from json import dump, load
from shutil import copy, move
from glob import glob
from os import chdir, path, remove
from sys import argv

from telethon.sync import TelegramClient
from telethon.tl.types import PeerChat, InputMessagesFilterEmpty
from telethon.tl.functions.messages import SearchRequest

MEZ_BEGIN = 'መዝ('  # the beginning of the mez
# the data collection file
DATA_FILE = 'mez-data.json'

# command line arguments
if len(argv) == 1:
    print('Need a command, give either of [get, post]')
    exit()
else:
    supported_args = ['get', 'post']
    if argv[1] not in supported_args:
        print('Command not supported.')
        exit()
    else:
        command = argv[1]

# to have access to the session file from anywhere
script_dir = path.dirname(__file__)
if script_dir:
    # change the cwd so it works here wherever it is called
    chdir(script_dir)

api_id = 17349
api_hash = '344583e45741c457fe1862106095a5eb'
phone = '+251920810739'
username = 'K1DV5'

client = TelegramClient(username, api_id, api_hash)
try:
    client.connect()
    # Ensure you're authorized
    if not client.is_user_authorized():
        client.send_code_request(phone)
        try:
            client.sign_in(phone, input('Enter the code: '))
        except:
            client.sign_in(password=input('Password: '))
    # chat = client.get_entity(PeerChat(269484381)) # The main group
    chat = client.get_entity('MezCollectorBot')
    CONNECTED = True

except ConnectionError:
    print('Connection problem.')
    CONNECTED = False

today = convert_date(date.today())

if command == 'post':
    # clean staging dir
    for file in glob('staging/መዝሙር-*.html'):
        remove(file)

    # bring the built index.html
    main_fname = f'staging/መዝሙር-{today.replace(" ", "-")}.html'
    copy('../dist/index.html', main_fname)
    # build the basic version
    basic_fname = build_basic()
    print('Built documents')

    if CONNECTED:
        client.send_file(chat, main_fname, caption="Normal version")
        client.send_file(chat, basic_fname, caption="Basic version")
        print('Uploaded data.')
    exit()


# get data

if path.exists(DATA_FILE):
    # get the data in the file
    with open(DATA_FILE, encoding='utf-8') as file:
        collected = load(file)
        offset_id = collected['last_id']
else:
    collected = {'data': {}, 'count_eng': 0}
    offset_id = 0

if CONNECTED:
    # option 1: get all messages and filter them here
    # messages = client.iter_messages(fk_entity)
    # messages = client.get_messages('MezCollectorBot')

    # option 2: get filtered messages from there
    filter = InputMessagesFilterEmpty()
    result = client(SearchRequest(
        peer=chat,  # On which chat/conversation
        q=MEZ_BEGIN,  # What to search for
        filter=filter,  # Filter to use (maybe filter for media)
        min_date=None,  # Minimum date
        max_date=None,  # Maximum date
        offset_id=offset_id,  # ID of the message to use as offset
        add_offset=0,  # Additional offset
        limit=5,  # How many results
        max_id=0,  # Maximum message ID
        min_id=0,  # Minimum message ID
        from_id=None,  # Who must have sent the message (peer)
        hash=0  # Special number to return nothing on no-change
        ))
    messages = result.messages

    def extract_title(mez: str):
        mez = mez.strip()
        in_parens_start = mez.find(MEZ_BEGIN) + len(MEZ_BEGIN)
        in_parens_end = mez.find(')', in_parens_start)
        in_parens = mez[in_parens_start: in_parens_end]
        if '/' in in_parens:
            category, title = in_parens.split('/')
        else:
            category, title = 'የምስጋና', in_parens.strip()
        body = mez[in_parens_end + 1:].strip()
        return {
                'title': title,
                'body': body,
                'category': category,
                }

    if messages: # there are new messages
        users = result.users

        collected['date'] = today
        collected['last_id'] = messages[0].id

        for message in messages:
            message_cont = message.message
            if message_cont and message_cont.strip().startswith(MEZ_BEGIN):
                collected['count_eng'] += 1
                message_id = message.id
                sender = [user for user in users if message.from_id == user.id][0]
                sender_username = sender.username
                sender_link = f'https://t.me/{sender_username}'
                sender_fname = sender.first_name
                sender_lname = sender.last_name
                if sender_fname and sender_lname:
                    sender_name = f'{sender_fname} {sender_lname}'
                elif sender_fname:
                    sender_name = sender_fname
                elif sender_lname:
                    sender_name = sender_lname
                else:
                    sender_name = sender_username

                mez_data = extract_title(message_cont)
                category = mez_data['category']
                mez_title = mez_data['title']
                mez_attrib = {
                        'sender_name': sender_name,
                        'sender_link': sender_link,
                        'body': mez_data['body'],
                        'id': message_id,
                        'date': convert_date(message.date.date()),
                        }
                # increment the total count
                collected['count_eng'] += 1
                if category in collected['data']:
                    collected['data'][category]['data'][mez_title] = mez_attrib
                    # increment the category count
                    collected['data'][category]['count_eng'] += 1
                    collected['data'][category]['count'] = geez_num(collected['data'][category]['count_eng'])
                else:
                    collected['data'][category] = {
                            'count': geez_num(1),
                            'count_eng': 1,
                            'data': {mez_title: mez_attrib}
                            }

                    # count data
        collected['count'] = geez_num(collected['count_eng'])


    else:
        print('There are no new messages')

with open(DATA_FILE, 'w', encoding='utf-8') as file:
    dump(collected, file, ensure_ascii=False)

print(f'Updated data in "{DATA_FILE}"')

