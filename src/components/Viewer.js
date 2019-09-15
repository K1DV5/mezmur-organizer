import React from 'react'

export default (props) => {
    let body = props.body
    // take care of repeats
    let parts = []
    let inParens = false
    let key = 0
    for (let part of body.split(/\n\(([^]*)\)/)) {
        let partLines = part.split('\n')
        if (inParens) {
            key++
            parts.push(
                <div
                    key={key}
                    style={{
                        display: 'inline-flex',
                        alignItems: 'center',
                    }}>
                    <div>
                        {partLines.map((line, i) =>
                            <p style={{margin: 0}} key={i}>{line}</p>)}
                    </div>
                    <div style={{fontSize: partLines.length + 'em', marginBottom: '.15em'}}>{'}'}</div>
                </div>
            )
            inParens = false
        } else {
            for (let line of partLines) {
                key++
                parts.push(
                    <React.Fragment key={key}>{line}<br /></React.Fragment>
                )
            }
            inParens = true
        }
    }
    return (
        <div>
            <h2>{props.title}</h2>
            <div style={{fontSize: '19pt'}}>
                {parts.map((line, key) => line)}
            </div>
        </div>
    )
}
