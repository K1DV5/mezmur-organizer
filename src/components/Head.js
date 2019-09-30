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

    if (props.searchOpen) {
        return (
            <div class="appbar">
                <div class="left-icon">
                    <svg class="icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/><path d="M0 0h24v24H0z" fill="none"/></svg>
                </div>
                <input
                    class="searchbar"
                    placeholder="Search"
                    autofocus={true}
                    onInput={props.filterItems}
                />
                <div class="right-icon" onClick={() => props.toggleSearch(false)} >
                    <svg class="icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/><path d="M0 0h24v24H0z" fill="none"/></svg>
                </div>
            </div>
        )
    }
    return (
        <div class="appbar">
            <div class="left-icon" onClick={props.back} style={{display: Title === props.homeTitle ? 'none' : ''}} >
                <svg class="icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/></svg>
            </div>
            <div class="appbar-text" >
                <div class="appbar-title">
                    {Title}
                </div>
                <div class="appbar-subtitle" > {subtitle} </div>
            </div>
            <div class="right-icon" onClick={() => props.toggleSearch(true)}>
                <svg class="icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/><path d="M0 0h24v24H0z" fill="none"/></svg>
            </div>
        </div>
    )
}
