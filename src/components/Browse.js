/** @jsx preact.h */
import preact from 'preact';
import Viewer from './Viewer'

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
                        <div key={index} onClick={() => gotoPage(`${mez.category}/${mez.title.replace(' ', '-')}`)} >
                            <div>
                                <div>
                                    {mez.title}
                                </div>
                                <div>
                                    {
                                        <preact.Fragment>
                                            {mez.category + '፣ ' + mez.date}
                                            <span style={contactStyle}>
                                                <a
                                                    href={'https://t.me/' + mez.sender}
                                                    style={contactLinkStyle}
                                                    target="_blank"
                                                >
                                                    {'@' + mez.sender}
                                                </a>
                                            </span>
                                        </preact.Fragment>
                                    }
                                </div>
                            </div>
                        </div>
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
                        <div onClick={() => gotoPage(`${activePage}/${title.replace(' ', '-')}`)} >
                            <div>
                                {title}
                            </div>
                            <div>
                                {
                                    <preact.Fragment>
                                        {mez.date}
                                        <span style={contactStyle}>
                                            <a
                                                href={'https://t.me/' + mez.sender}
                                                style={contactLinkStyle}
                                                target="_blank"
                                            >
                                                {'@' + mez.sender}
                                            </a>
                                        </span>
                                    </preact.Fragment>
                                }
                            </div>
                        </div>
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
            {categories.map((cat, index) => (
                <div key={index} onClick={() => gotoPage(cat)} >
                    <div>
                        {cat}
                    </div>
                    <div>
                        {data[cat].count + (data[cat].count_eng > 1 ? ' መዝሙሮች' : ' መዝሙር')}
                    </div>
                </div>
            ))}
        </div>
    )
}

let contactStyle = {
    float: 'right',
    style: 'inline-flex',
    alignItems: 'center',
    position: 'relative',
    bottom: '.3em',
}

let contactLinkStyle = {
    fontSize: 'smaller',
    textDecoration: 'none',
    position: 'relative',
    marginLeft: 3,
    bottom: '.5em'
}
