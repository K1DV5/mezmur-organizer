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
    Title = Title.includes('/') ? Title.split('/').slice(-2, -1) : Title
    return (
        <div style={{width: '100%', backgroundColor: '#adf', position: 'fixed', top: 0}}>
            <div class="appbar">
                <div class="toolbar">
                    {props.searchOpen ? (
                        <div style={{display: 'flex'}}>
                            <input
                                style={{flexGrow: 1}}
                                autoFocus={true}
                                onInput={props.filterItems}
                            />
                            <button onClick={() => props.toggleSearch(false)} >
                                Close
                            </button>
                        </div>
                    ) : (
                            <div style={{
                                display: 'flex',
                                alignItems: 'center',
                                wrap: 'no-wrap',
                                textOverflow: 'ellipsis',
                                width: '100%'
                            }}
                            >
                                <div class="item" style={{display: Title === props.homeTitle ? 'none' : ''}} >
                                    <button onClick={props.back} >
                                        Back
                                    </button>
                                </div>
                                <div class="item" style={{flexGrow: 1}} >
                                    <div class="typography" >
                                        {Title}
                                    </div>
                                    <div class="typography" > {subtitle} </div>
                                </div>
                                <div class="item" >
                                    <button
                                        onClick={() => props.toggleSearch(true)}
                                    >
                                        Search
                                    </button>
                                </div>
                            </div>
                        )}
                </div>
            </div>
        </div>
    )
}
