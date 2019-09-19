import React from 'react'
import List from '@material-ui/core/List'
import ListItem from '@material-ui/core/ListItem'
import ListItemText from '@material-ui/core/ListItemText'
import PersonIcon from '@material-ui/icons/Person'
import Viewer from './Viewer'

export default (props) => {
    let activePage = props.activePage
    let data = props.data.data
    let categories = Object.keys(data)
    let gotoPage = props.gotoPage

    if (props.visibleItems) { // for filtered list
        return (
            props.visibleItems !== [] ? (
                <List>
                    {props.visibleItems.map((mez, index) =>
                        <ListItem key={index} button dense onClick={() => gotoPage(`${mez.category}/${mez.title.replace(' ', '-')}`)} >
                            <ListItemText
                                primary={mez.title}
                                secondary={
                                    <React.Fragment>
                                        {mez.category + '፣ ' + mez.date}
                                        <span style={contactStyle}>
                                            <PersonIcon />
                                            <a
                                                href={mez.sender_link}
                                                style={contactLinkStyle}
                                                target="_blank"
                                            >
                                                {mez.sender_name}
                                            </a>
                                        </span>
                                    </React.Fragment>
                                } />
                        </ListItem>
                    )}
                </List>
            ) : <div>No results</div>
        )
    } else if (categories.includes(activePage)) { // list mez in category
        let titles = Object.keys(data[activePage].data)
        return (
            <List>
                {titles.map((title, index) => {
                    let mez = data[activePage].data[title]
                    return (
                        <ListItem key={index} button dense onClick={() => gotoPage(`${activePage}/${title.replace(' ', '-')}`)} >
                            <ListItemText
                                primary={title}
                                secondary={
                                    <React.Fragment>
                                        {mez.date}
                                        <span style={contactStyle}>
                                            <PersonIcon />
                                            <a
                                                href={mez.sender_link}
                                                style={contactLinkStyle}
                                                target="_blank"
                                            >
                                                {mez.sender_name}
                                            </a>
                                        </span>
                                    </React.Fragment>
                                } />
                        </ListItem>
                    )
                })}
            </List>
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
        <List>
            {categories.map((cat, index) => (
                <ListItem key={index} button dense onClick={() => gotoPage(cat)} >
                    <ListItemText primary={cat} secondary={data[cat].count + (data[cat].count_eng > 1 ? ' መዝሙሮች' : ' መዝሙር')} />
                </ListItem>
            ))}
        </List>
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
