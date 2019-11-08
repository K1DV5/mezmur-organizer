# -*- coding: utf-8 -*-

from .date import convert_date
from .number import geez_num
from datetime import date
from json import dump, dumps, load, loads
from shutil import copy, move
from glob import glob
from os import path, remove
from re import sub

from telethon.sync import TelegramClient
from telethon.sessions import StringSession
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
with open('.session') as file:
    session = file.read().strip()

def get_client():
    client = TelegramClient(StringSession(session), api_id, api_hash)
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

def get_chat(client, username=None):
    # default is the group chat
    entity = PeerChannel(1199760564) if not username else username
    chat = client.get_entity(entity)
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

def search_messages(client, chat, min_id):
    # option 1: get all messages and filter them here
    # messages = client.iter_messages(fk_entity)
    # messages = client.get_messages('MezCollectorBot')

    # option 2: get filtered messages from there
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

def transliterate(amh):
    with open(path.join(path.dirname(__file__), './amhMatch.json'), encoding='utf-8') as file:
        lang_data = load(file)
    eng = ''
    for char in amh:
       eng += lang_data[char] if char in lang_data else ' '
    return eng

def get_mez_info(message, sender):
    message_cont = message.message
    mez_data = extract_title(message_cont)
    return {
            'title': mez_data['title'],
            'category': mez_data['category'],
            'props': {
                'sender': '@' + sender.username if sender.username else '+' + sender.phone,
                'body': mez_data['body'],
                'id': message.id,
                'date': convert_date(message.date.date()),
                'title_eng': transliterate(mez_data['title']),
                }
            }

def add_mez(message, collected, sender, updates):
    mez_info = get_mez_info(message, sender)
    title, category = mez_info['title'], mez_info['category']
    props = mez_info['props']
    if category in collected['data']:
        cat_info = collected['data'][category]
        if title in cat_info['data']:
            # add to updates
            updates[title] = {'type': 'edit', 'sender': props['sender']}
        else:
            # add to updates
            updates[title] = {'type': 'new', 'sender': props['sender']}
            # increment the total count
            collected['count_eng'] += 1
            # increment the category count
            cat_info['count_eng'] += 1
            # convert the count number
            cat_info['count'] = geez_num(cat_info['count_eng'])
        cat_info['data'][title] = props
    else:
        # increment the total count
        collected['count_eng'] += 1
        collected['data'][mez_info['category']] = {
                'count': geez_num(1),
                'count_eng': 1,
                'data': {mez_info['title']: props}
                }
    return collected, updates

def remove_mez(message, collected, updates):
    # remove existing
    path = message.message[len(MEZ_BEGIN)+1:]
    category, title = path.split('/') if path.count('/') == 1 else ('የምስጋና', path)
    if category in collected['data']:
        if title in collected['data'][category]['data']:
            cat_info = collected['data'][category]
            sender = cat_info['data'][title]['sender']
            updates[title] = {'type': 'remove', 'sender': sender}
            # update counts
            collected['count_eng'] -= 1
            if cat_info['count_eng'] == 1:  # if it is the last of its kind
                del collected['data'][category]
            else:
                cat_info['count_eng'] -= 1
                cat_info['count'] = geez_num(cat_info['count_eng'])
                del cat_info['data'][title]
    return collected, updates

def merge_updates(client, chat, collected):
    '''merge collected data and existing'''

    result = search_messages(client, chat, collected['last_id'])
    messages = result.messages
    updates = {}
    if messages:  # there are new messages
        users = result.users

        collected['date'] = TODAY
        collected['last_id'] = messages[0].id
        messages.reverse()  # to get them in the order written

        for message in messages:
            message_cont = message.message
            if message_cont:
                message_cont = message_cont.strip()
                sender = [user for user in users if message.from_id == user.id][0]
                if message_cont.startswith(MEZ_BEGIN):  # add or edit
                    collected, updates = add_mez(message, collected, sender, updates)
                elif message_cont.startswith('-' + MEZ_BEGIN):  # delete
                    # only if the sender is authorized
                    if sender.phone in ['251921326733', '251941627376', '251920810739']:
                        collected, updates = remove_mez(message, collected, updates)
        # count data
        collected['count'] = geez_num(collected['count_eng'])
    return collected, updates

def update_data(client, chat):

    if path.exists(DATA_FILE):
        # get the data in the file
        with open(DATA_FILE, encoding='utf-8') as file:
            collected = load(file)
    else:
        collected = {'data': {}, 'count_eng': 0, 'last_id': 0, 'count': 0}

    collected, updates = merge_updates(client, chat, collected)

    if updates:  # there are news
        with open(DATA_FILE, 'w', encoding='utf-8') as file:
            dump(collected, file, ensure_ascii=False)

        print(f'Updated data in "{DATA_FILE}"')
        return updates


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

def build_doc():
    # bring the built index.html
    with open('dist/index.html', encoding='utf-8') as file:
        template = file.read()
    # bring the data
    with open('mez-data.json', encoding='utf-8') as file:
        data = loads(file.read())
    # build the final
    main_fname = f'dist/መዝሙር.html'
    with open(main_fname, 'w', encoding='utf-8') as file:
        # the main version
        data_obj = sub('"(\\w+)":', '\\1:', dumps(data, separators=(',', ':'), ensure_ascii=False)).replace('\\', '\\\\')
        built = sub(r'(?s)<script id="mezmurData".+?</script>',
                f'<script type="text/javascript">const mezmurData = {data_obj}</script>',
                template)
        # build the basic version
        built = insert_basic(built, data)
        # write file
        file.write(built)
        print('Built document')
    return main_fname

def post_doc(client, chat, file, updates):
    caption = f'የ {TODAY} ዕትም'
    change_log = ''
    update_caps = {'new': [], 'edit': [], 'remove': []}
    for title, props in updates.items():
        update_caps[props['type']].append(title + ' በ ' + props['sender'])
    if update_caps['new']:
        change_log += f"\nአዳዲስ የተጨመሩት፦\n \u2022 " + '\n \u2022 '.join(update_caps['new'])
    if update_caps['edit']:
        change_log += f"\nየተስተካከሉት፦\n \u2022 " + '\n \u2022 '.join(update_caps['edit'])
    if update_caps['remove']:
        change_log += f"\nየጠፉት፦\n \u2022 " + '\n \u2022 '.join(update_caps['remove'])
    client.send_file(chat, file, caption=caption)
    client.send_message(chat, change_log.strip())
    print('Uploaded doc.')

