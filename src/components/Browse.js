/** @jsx preact.h */
import preact from 'preact';
import Viewer from './Viewer'

function ListItem(props) {
    let contactLink
    let contactText
    if (props.contact) {
        if (isNaN(props.contact)) {  // username
            contactLink = 'https://t.me/' + props.contact
            contactLink = '@' + props.contact
        } else { // phone number 2519...
            contactLink = 'tel:+' + props.contact
            contactText = contactLink
        }
    }
    return (
        <div class="list-item" onClick={props.onClick}>
            {props.primary}
            <div class="secondary-text">
                {props.secondary}
                {contactLink ?
                    <span class="contact">
                        <a
                            href={contactLink}
                            class="contact-link"
                            target="_blank"
                        >
                            {contactText}
                        </a>
                    </span>
                    : null}
            </div>
        </div>
    )
}

export default (props) => {
    let activePage = props.activePage
    let data = props.data.data
    let categories = Object.keys(data)
    let gotoPage = props.gotoPage

    if (props.visibleItems) { // for filtered list
        return (
            props.visibleItems !== [] ? (
                <div>
                    {props.visibleItems.map((mez, index) =>
                        <ListItem
                            onClick={() => gotoPage(`${mez.category}/${mez.title.replace(' ', '-')}`)}
                            key={index}
                            primary={mez.title}
                            secondary={mez.category + '፣ ' + mez.date}
                            contact={mez.sender}
                        />
                    )}
                </div>
            ) : <div>No results</div>
        )
    } else if (categories.includes(activePage)) { // list mez in category
        let titles = Object.keys(data[activePage].data)
        return (
            <div>
                {titles.map((title, index) => {
                    let mez = data[activePage].data[title]
                    return (
                        <ListItem
                            onClick={() => gotoPage(`${activePage}/${title.replace(' ', '-')}`)}
                            key={index}
                            primary={title}
                            secondary={mez.date}
                            contact={mez.sender}
                        />
                    )
                })}
            </div>
        )
    } else if (activePage) { // for viewing mez
        let [category, title] = activePage.split('/')
        if (category && title && categories.includes(category)) {
            title = title.replace('-', ' ')
            let mezData = data[category].data[title]
            let body = mezData.body
            if (body) {
                return <Viewer title={title} body={body} />
            }
        }
    }
    return ( // default: list categories
        <div>
            {categories.map((cat, index) =>
                <ListItem
                    onClick={() => gotoPage(cat)}
                    key={index}
                    primary={cat}
                    secondary={data[cat].count + (data[cat].count_eng > 1 ? ' መዝሙሮች' : ' መዝሙር')}
                />
            )}
        </div>
    )
}

