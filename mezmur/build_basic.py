'''this module is to be imported in teleg.py'''

from os import chdir, path, remove
from json import load


def build_basic():
    with open('../src/basic-template.html', encoding='utf-8') as file:
        template = file.read()

    with open('mez-data.json', encoding='utf-8') as file:
        data = load(file)


    # the subtitle under the main title
    built = template.replace('{subtitle}', f'የ {data["date"]} ዕትም፣ {data["count"]} መዝሙሮች')

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

    built = built.replace('{toc}', toc)
    built = built.replace('{main}', body)

    out_name = f'staging/መዝሙር-{data["date"].replace(" ", "-")}-basic.html'
    with open(out_name, 'w', encoding='utf-8') as file:
        file.write(built)

    return out_name

# build_basic()
