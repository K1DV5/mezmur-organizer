from .telegram.__main__ import get_client, get_chat, update_data, build_doc, post_doc
from .drive import authorized_service, update_file, download_file
from os import chdir, path, makedirs
from sys import argv
import json

# to have access to the session file from anywhere
package_dir = path.dirname(__package__)
if package_dir:
    # change the cwd so it works here wherever it is called
    chdir(package_dir)

if __name__ == '__main__':
    if len(argv) == 2:
        service = authorized_service()  # the google drive service
        with open('drive_file_ids.json') as file:
            file_ids = json.load(file)
        command = argv[1]
        if command == 'build':  # once a week or so
            # download data, template
            download_file(service, 'mez-data.json', file_ids['mez-data.json'])
            makedirs('dist', exist_ok=True)
            download_file(service, 'dist/index.html', file_ids['index.html'])
            # update data from telegram to drive
            client = get_client()
            chat = get_chat(client)
            updates = update_data(client, chat)
            if updates:  # None if there is no update
                # to drive
                update_file(service, 'mez-data.json', file_ids['mez-data.json'])
                # post on telegram
                file = build_doc()
                post_doc(client, chat, file, updates)
            else:
                print('No new mez')
        elif command == 'template':
            # build template (npm run build) and update on drive
            update_file(service, 'dist/index.html', file_ids['index.html'])

        # FOR LOCAL TESTING
        elif command == 'lbuild':
            # update data from telegram to drive
            client = get_client()
            chat = get_chat(client, 'me')
            updates = update_data(client, chat)
            if updates:  # None if there is no update
                # to drive
                # update_file(service, 'mez-data.json', file_ids['mez-data.json'])
                # post on telegram
                file = build_doc()
                post_doc(client, chat, file, updates)
            else:
                print('No new mez')
        elif command == 'ltemplate':
            # build template (npm run build) before this and update on drive
            update_file(service, 'dist/index.html', file_ids['index.html'])
        elif command == 'lgetdata':
            download_file(service, 'mez-data.json', file_ids['mez-data.json'])
        elif command == 'lupdatedata':
            update_file(service, 'mez-data.json', file_ids['mez-data.json'])
        elif command == 'lbuild-only':
            build_doc()
        else:
            raise ValueError('Command should be in [bot, build, template]')
    else:
        raise ValueError('One argument needed')
