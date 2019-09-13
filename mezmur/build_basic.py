'''this module is to be imported in teleg.py'''

from os import chdir, path, remove
from json import load


def build_basic():
    with open('../src/basic-template.html', encoding='utf-8') as file:
        template = file.read()

    with open('mez.json', encoding='utf-8') as file:
        data = load(file)


    # the subtitle under the main title
    built = template.replace('{subtitle}', f'የ {data["date"]} ዕትም፣ {data["count"]} መዝሙሮች')

    toc = ''
    body = ''

    for category, cat_data in data['data'].items():
        category_id = category.replace(" ", "-")
        toc += f'<a class="toc-cat" href="#{category_id}">{category}</a>'
        cat_head = f'<h2 id={category_id}>{category}</h2>'
        cat_body = ''

        for mez in cat_data['data']:
            mez_id = mez['id']
            toc += f'<a class="toc-mez" href="#{mez_id}">{mez["title"]}</a>'
            mez_head = f'<h3 id={mez_id}>{mez["title"]}</h3>'

            mez_body = '<div class="mez-body">' + mez['body'].replace('\n', '<br />') + '</div>'
            cat_body += mez_head + mez_body

        body += cat_head + cat_body

    built = built.replace('{toc}', toc)
    built = built.replace('{main}', body)

    out_name = f'staging/መዝሙር-{data["date"].replace(" ", "-")}-basic.html'
    with open(out_name, 'w', encoding='utf-8') as file:
        file.write(built)

    return out_name

# build_basic()
