import React from 'react'

export default (props) => {
    return (
        <div>
            <h2>{props.title}</h2>
            <div  style={{fontSize: '19pt'}}>
                {props.body.split('\n').map((line, key) => 
                    <React.Fragment key={key}>{line}<br /></React.Fragment>
                )}
            </div>
        </div>
    )
}
