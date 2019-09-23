import React from 'react'

function Line(props) {
    if (/\[.*?\]/.test(props.line)) {
        return (
            <React.Fragment>{props.line.split(/\[([^]*?\] *[\u1369-\u1371])/).map((part, i) => {
                if (i % 2) { // in parens
                    let [text, number] = part.split(']')
                    return <React.Fragment key={i}>
                                <u>{text}</u> {number}
                            </React.Fragment>
                }
                return <React.Fragment key={i}>{part}</React.Fragment>
            })}
            </React.Fragment>
        )
    }
    return props.line.trim()? props.line : null
}

function Verse(props) {
    // like a paragraph, without any blank line
    let text = props.children.replace(/\(([^\n]*?)\)/, '[$1]')  // for lines

    return (
        <div style={{marginBottom: '1em'}}>
            {text.split(/\(([^]*?\) *[\u1369-\u1371])/).map((part, i) => { // take care of multiline repeats
                let [text, number] = part.split(')')
                let partLines = text.trim().split('\n')
                if (i % 2) {  // in parens
                    return (
                        <div
                            key={i}
                            style={{
                                display: 'flex',
                                alignItems: 'center',
                            }}
                        >
                            <div>
                                {partLines.map((line, j) =>
                                    <React.Fragment key={j}>
                                        <Line line={line} />
                                        <br />
                                    </React.Fragment>)}
                            </div>
                            <div
                                style={{
                                    fontSize: partLines.length + 'em',
                                    marginBottom: '.15em'
                                }}>{'}'}</div> {number}
                        </div>
                    )
                } else {
                    return (
                        <React.Fragment key={i}>
                            {partLines.map((line, j) =>
                                <React.Fragment key={j}>
                                    <Line line={line} />
                                    <br />
                                </React.Fragment>
                            )}
                        </React.Fragment>
                    )
                }
            })}
        </div>
    )
}

export default (props) => {
    return (
        <div>
            <h2>{props.title}</h2>
            <div style={{fontSize: '19pt'}}>
                {props.body.split('\n\n').map((verse, key) => {
                    if (verse.trim())
                        return <Verse key={key}>{verse.trim()}</Verse>
                })}
            </div>
        </div>
    )
}
