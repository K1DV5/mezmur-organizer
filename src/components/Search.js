import React from 'react'
import AppBar from '@material-ui/core/AppBar'
import ToolBar from '@material-ui/core/Toolbar'
import Typography from '@material-ui/core/Typography'
import InputBase from '@material-ui/core/InputBase'
import IconButton from '@material-ui/core/IconButton';
import Grid from '@material-ui/core/Grid'
import BackIcon from '@material-ui/icons/ArrowBack'
import SearchIcon from '@material-ui/icons/Search'
import CloseIcon from '@material-ui/icons/Close'
import InputAdornment from '@material-ui/core/InputAdornment';

export default (props) => {
    let Title = props.Title ? props.Title : props.homeTitle
    Title = Title.includes('/') ? Title.split('/').slice(-2, -1) : Title
    return (
        <div style={{width: '100%'}}>
            <AppBar position="static" color="primary">
                <ToolBar>
                    {props.searchOpen? (
                        <InputBase
                            style={{color: 'white', width: '100%'}}
                            autoFocus={true}
                            startAdornment={(
                            <InputAdornment>
                                <SearchIcon style={{marginRight: 10}} />
                            </InputAdornment>
                            )}
                            endAdornment={(
                            <InputAdornment>
                            <IconButton
                                color="inherit"
                                aria-label="Cancel"
                                onClick={() => props.toggleSearch(false)}
                            >
                                <CloseIcon />
                            </IconButton>
                            </InputAdornment>
                            )}
                            onChange={props.filterItems}
                        />
                    ) : (
                    <Grid container alignItems="center" wrap="nowrap" style={{width: '100%'}}>
                        <Grid item style={{display: Title === props.homeTitle ? 'none' : ''}} >
                            <IconButton
                                color="inherit"
                                aria-label="Menu"
                                onClick={props.back}
                            >
                                <BackIcon />
                            </IconButton>
                        </Grid>
                        <Grid item style={{flexGrow: 1}} >
                            <Typography
                                style={{display: 'flex', alignItems: 'center'}}
                                noWrap={true}
                                variant="h6"
                                color="inherit"
                            >
                                {Title}
                            </Typography>
                            <Typography
                                variant="subtitle2"
                                style={{display: Title === props.homeTitle ? '' : 'none'}}
                            >
                                {'የ ' + props.date + ' ዕትም፣ ' + props.count + ' መዝሙሮች'}
                            </Typography>
                        </Grid>
                        <Grid item >
                            <IconButton
                                color="inherit"
                                aria-label="Menu"
                                onClick={() => props.toggleSearch(true)}
                            >
                                <SearchIcon />
                            </IconButton>
                        </Grid>
                    </Grid>
                    )}
                </ToolBar>
            </AppBar>
        </div>
    )
}
