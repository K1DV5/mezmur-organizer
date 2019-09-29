/** @jsx preact.h */
import preact from 'preact'

export default (props) => {
    let Title, subtitle
    if (props.Title) {
        if (props.Title.includes('/')) {
            // mez viewing
            [Title, subtitle] = props.Title.split('/')
            subtitle = subtitle.replace('-', ' ')
        } else {
            // mez list in category
            Title = props.Title
            subtitle = props.catCount + (props.catCount === '፩' ? ' መዝሙር' : ' መዝሙሮች')
        }
    } else {
        // main category list
        Title = props.homeTitle
        subtitle = 'የ ' + props.date + ' ዕትም፣ ' + props.count + ' መዝሙሮች'
    }

    return (
        <preact.Fragment>
            {props.searchOpen ? (
                <div style={appBarStyle}>
                    <input
                        style={searchStyle}
                        autofocus={true}
                        onInput={props.filterItems}
                    />
                    <button style={{marginLeft: '1em'}} onClick={() => props.toggleSearch(false)} >
                        Close
                    </button>
                </div>
            ) : (
                <div style={appBarStyle}>
                    <button onClick={props.back} style={{display: Title === props.homeTitle ? 'none' : '', marginRight: '1em'}} >
                        Back
                    </button>
                    <div style={{ flexGrow: 1 }} >
                        <div style={{
                            wrap: 'no-wrap',
                            textOverflow: 'ellipsis',
                        }} >
                            {Title}
                        </div>
                        <div style={{fontSize: '80%'}} > {subtitle} </div>
                    </div>
                    <button style={{marginLeft: '1em'}} onClick={() => props.toggleSearch(true)} >
                        Search
                    </button>
                </div>
            )}
        </preact.Fragment>
    )
}

let appBarStyle = {
    width: '100%',
    backgroundColor: '#4055B2',
    boxShadow: '0 0 0.5em 0.3em #777',
    color: 'white',
    height: '2.1em',
    padding: '1.5em',
    position: 'fixed',
    display: 'flex',
    alignItems: 'center',
    boxSizing: 'border-box',
    top: 0,
    left: 0
}

let searchStyle = {
    flexGrow: 1,
    background: 'transparent',
    border: 'transparent',
    color: 'white'
}
