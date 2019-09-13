import React from 'react'
import List from '@material-ui/core/List'
import ListItem from '@material-ui/core/ListItem'
import ListItemText from '@material-ui/core/ListItemText'
import Viewer from './Viewer'

export default (props) => {
    let activePage = props.activePage
    let data = props.data.data
    let categories = Object.keys(data)
    let gotoPage = props.gotoPage
    
    if (props.visibleItems) { // for filtered list
        return (
            props.visibleItems !== []? (
            <List>
                {props.visibleItems.map((mez, index) =>
                    <ListItem key={index} button dense onClick={() => gotoPage(`${mez.category}/${index}`)} >
                        <ListItemText
                            primary={mez.title}
                            secondary={
                                <React.Fragment>
                                    {mez.category + '፣ ' + mez.date + '፣ በ '}
                                    <a href={mez.sender_link} style={{fontSize: 'smaller', textDecoration: 'none'}}>
                                        {mez.sender_name}
                                    </a>
                                </React.Fragment>
                            } />
                    </ListItem>
                )}
            </List>
            ) : <div>No results</div>
        )
    } else if (categories.includes(activePage)) { // list mez in category
        return (
            <List>
                {data[activePage].data.map((mez, index) => (
                    <ListItem key={index} button dense onClick={() => gotoPage(`${activePage}/${index}`)} >
                        <ListItemText
                            primary={mez.title}
                            secondary={
                                <React.Fragment>
                                    {mez.date + '፣ በ '}
                                    <a href={mez.sender_link} style={{fontSize: 'smaller', textDecoration: 'none'}}>
                                        {mez.sender_name}
                                    </a>
                                </React.Fragment>
                            } />
                    </ListItem>
                ))}
            </List>
        )
    } else if (activePage) { // for viewing mez
        let [category, mez] = activePage.split('/')
        if (category && mez && categories.includes(category)) {
            let {title, body} = data[category].data[Number(mez)]
            if (title) {
                return <Viewer title={title} body={body} />
            }
        }
    }
    return ( // default: list categories
        <List>
            {categories.map((cat, index) => (
                <ListItem key={index} button dense onClick={() => gotoPage(cat)} >
                    <ListItemText primary={cat} secondary={data[cat].count + (data[cat].count_eng > 1? ' መዝሙሮች' : ' መዝሙር')} />
                </ListItem>
            ))}
        </List>
    )
}
