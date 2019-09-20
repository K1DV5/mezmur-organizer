from .telegram.__main__ import update_data, post_output
from .drive import authorized_service, update_file, download_file
from os import chdir, path, makedirs
from sys import argv
import json

# to have access to the session file from anywhere
script_dir = path.dirname(__package__)
if script_dir:
    # change the cwd so it works here wherever it is called
    chdir(script_dir)

if __name__ == '__main__':
    if len(argv) == 2:
        service = authorized_service()  # the google drive service
        with open('drive_file_ids.json') as file:
            file_ids = json.load(file)
        command = argv[1]
        if command == 'bot':
            # download session file and data
            download_file(service, 'K1DV5.session', file_ids['K1DV5.session'])
            download_file(service, 'mez-data.json', file_ids['mez-data.json'])
            # update data from telegram to drive
            news = update_data()
            if news:
                update_file(service, 'mez-data.json', file_ids['mez-data.json'])
            else:
                print('No new mez')
        elif command == 'build':
            # download session file, data, template
            download_file(service, 'K1DV5.session', file_ids['K1DV5.session'])
            download_file(service, 'mez-data.json', file_ids['mez-data.json'])
            makedirs('dist', exist_ok=True)
            download_file(service, 'dist/index.html', file_ids['index.html'])
            # update data from telegram to drive
            news = update_data()
            if news:
                update_file(service, 'mez-data.json', file_ids['mez-data.json'])
                # post on telegram
                post_output([])
            else:
                print('No new mez')
        elif command == 'template':
            # build template (npm run build) and update on drive
            update_file(service, 'dist/index.html', file_ids['index.html'])

        # FOR LOCAL TESTING
        elif command == 'lbot':
            news = update_data()
            # news = 1
            if news:
                update_file(service, 'mez-data.json', file_ids['mez-data.json'])
            else:
                print('No new mez')
        elif command == 'lbuild':
            # update data from telegram to drive
            news = update_data()
            if news:
                update_file(service, 'mez-data.json', file_ids['mez-data.json'])
                # post on telegram
                post_output([])
            else:
                print('No new mez')
        elif command == 'ltemplate':
            # build template (npm run build) before this and update on drive
            update_file(service, 'dist/index.html', file_ids['index.html'])

        else:
            raise ValueError('Command should be in [bot, build, template]')
    else:
        raise ValueError('One argument needed')
