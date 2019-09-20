from .date import convert_date
from .number import geez_num
from datetime import date
from json import dump, load, loads
from shutil import copy, move
from glob import glob
from os import path, remove
from re import sub

from telethon.sync import TelegramClient
from telethon.tl.types import PeerChannel, InputMessagesFilterEmpty
from telethon.tl.functions.messages import SearchRequest

MEZ_BEGIN = 'መዝ/'  # the beginning of the mez
# the data collection file
DATA_FILE = 'mez-data.json'
# today's date in amharic
TODAY = convert_date(date.today())

# these values are from telegram desktop
api_id = 17349
api_hash = '344583e45741c457fe1862106095a5eb'
phone = '+251920810739'
username = 'K1DV5'

def get_client():
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
        return client

    except ConnectionError:
        print('Connection problem.')

def get_chat(client):
    entity = 1199760564
    chat = client.get_entity(entity) # The main group
    # chat = client.get_entity('MezCollectorBot')
    return chat

def extract_title(mez: str):
    # the title is like:
    # መዝ/[category?]/[title]
    # replace numbers with geez
    mez = sub('\\d+', lambda mo: geez_num(int(mo.group(0))), mez.strip())
    catNtitle_start = mez.find(MEZ_BEGIN) + len(MEZ_BEGIN)
    catNtitle_end = mez.find('\n', catNtitle_start)
    catNtitle = mez[catNtitle_start: catNtitle_end]
    if '/' in catNtitle:
        category, title = catNtitle.split('/')
    else:
        category, title = 'የምስጋና', catNtitle.strip()
    body = mez[catNtitle_end + 1:].strip()
    return {
            'title': title,
            'body': body,
            'category': category,
            }

def search_messages(client, min_id):
    # option 1: get all messages and filter them here
    # messages = client.iter_messages(fk_entity)
    # messages = client.get_messages('MezCollectorBot')

    # option 2: get filtered messages from there
    chat = get_chat(client)
    result = client(SearchRequest(
        peer=chat,  # On which chat/conversation
        q=MEZ_BEGIN,  # What to search for
        filter=InputMessagesFilterEmpty(),  # Filter to use (maybe filter for media)
        min_date=date(2019, 8, 1),  # Minimum date
        max_date=None,  # Maximum date
        offset_id=0,  # ID of the message to use as offset
        add_offset=0,  # Additional offset
        limit=1000,  # How many results
        max_id=0,  # Maximum message ID
        min_id=min_id,  # Minimum message ID
        from_id=None,  # Who must have sent the message (peer)
        hash=0  # Special number to return nothing on no-change
        ))

    return result

def get_sender_info(sender):
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

    return {'name': sender_name, 'link': sender_link}

def get_mez_info(message, sender):
    message_cont = message.message
    mez_data = extract_title(message_cont)
    sender_info = get_sender_info(sender)
    return {
            'title': mez_data['title'],
            'category': mez_data['category'],
            'sender_name': sender_info['name'],
            'sender_link': sender_info['link'],
            'body': mez_data['body'],
            'id': message.id,
            'date': convert_date(message.date.date()),
            }

def merge_updates(client, collected):
    '''merge collected data and existing'''

    result = search_messages(client, collected['last_id'])
    messages = result.messages
    news = []  # new titles
    if messages: # there are new messages
        users = result.users

        collected['date'] = TODAY
        collected['last_id'] = messages[0].id

        for message in messages:
            message_cont = message.message
            if message_cont and message_cont.strip().startswith(MEZ_BEGIN):
                sender = [user for user in users if message.from_id == user.id][0]
                mez_info = get_mez_info(message, sender)
                # increment the total count
                collected['count_eng'] += 1
                # add to news
                news.append(mez_info['title'] + ' በ ' + mez_info['sender_name'])
                if mez_info['category'] in collected['data']:
                    collected['data'][mez_info['category']]['data'][mez_info['title']] = mez_info
                    # increment the category count
                    collected['data'][mez_info['category']]['count_eng'] += 1
                    collected['data'][mez_info['category']]['count'] = geez_num(collected['data'][mez_info['category']]['count_eng'])
                else:
                    collected['data'][mez_info['category']] = {
                            'count': geez_num(1),
                            'count_eng': 1,
                            'data': {mez_info['title']: mez_info}
                            }
        # count data
        collected['count'] = geez_num(collected['count_eng'])
    return collected, news

def update_data(client):

    if path.exists(DATA_FILE):
        # get the data in the file
        with open(DATA_FILE, encoding='utf-8') as file:
            collected = load(file)
    else:
        collected = {'data': {}, 'count_eng': 0, 'last_id': 0, 'count': 0}

    collected, news = merge_updates(client, collected)

    if news:  # there are new
        with open(DATA_FILE, 'w', encoding='utf-8') as file:
            dump(collected, file, ensure_ascii=False)

        print(f'Updated data in "{DATA_FILE}"')
        return news


# POST DATA

def insert_basic(template, data):

    # the subtitle under the main title
    built = template.replace('{{basicSubtitle}}', f'የ {data["date"]} ዕትም፣ {data["count"]} መዝሙሮች')

    toc = ''
    body = ''

    for category, cat_data in data['data'].items():
        category_id = category.replace(" ", "-")
        toc += f'<a class="toc-cat" id="toc:{category_id}" href="#{category_id}">{category}</a>'
        cat_head = f'<h2 id={category_id}><a href="#toc:{category_id}">{category}</a></h2>'
        cat_body = ''

        for title, mez in cat_data['data'].items():
            mez_id = mez['id']
            toc += f'<a class="toc-mez" id="toc:{mez_id}" href="#{mez_id}">{title}</a>'
            mez_head = f'<h3 id={mez_id}><a href="#toc:{mez_id}">{title}</a></h3>'

            mez_body = '<div class="mez-body">' + mez['body'].replace('\n', '<br />') + '</div>'
            cat_body += mez_head + mez_body

        body += cat_head + cat_body

    built = built.replace('{{basicToc}}', toc)
    built = built.replace('{{basicMain}}', body)

    return built

def post_output(news):
    # bring the built index.html
    with open('dist/index.html', encoding='utf-8') as file:
        template = file.read()
    # bring the data
    with open('mez-data.json', encoding='utf-8') as file:
        data = file.read()
    # build the final
    main_fname = f'dist/መዝሙር.html'
    with open(main_fname, 'w', encoding='utf-8') as file:
        # the main version
        built = template.replace('{{mezmurData}}', 
                f'<script type="text/javascript">mezmurData = {data}</script>')
        # build the basic version
        built = insert_basic(built, loads(data))
        # write file
        file.write(built)
        print('Built document')

    caption = ''
    if news:
        caption = f"የ {TODAY} ዕትም\nአዳዲስ የተጨመሩት፦\n\u2022" + '\n\u2022'.join(news)
    client.send_file(CHAT, main_fname, caption=caption)
    print('Uploaded doc.')

