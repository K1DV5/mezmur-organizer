import React from 'react'
import ReactDOM from 'react-dom'
import Head from './components/Head'
import filterEngData from './amhMatch.json'
import Browse from './components/Browse'

// the data is from the template html, has the following form:
console.info('\nThe data is in the variable "mezmurData".\n"copy(mezmurData)" to copy it to the clipboard.\n\n')

class App extends React.Component {
    constructor(props) {
        super(props)
        this.homeTitle = 'መዝሙር'
        this.state = {
            searchOpen: false,
            activePage: null,
            barTitle: this.homeTitle,
            visibleItems: null
        }
        this.filterable = this.getFilterableData(mezmurData)
        this.getFilterableData = this.getFilterableData.bind(this)
        this.filterItems = this.filterItems.bind(this)
        this.gotoPage = this.gotoPage.bind(this)
        this.back = this.back.bind(this)
        this.toggleSearch = this.toggleSearch.bind(this)
    }

    gotoPage(path) {
        this.setState({
            activePage: path, 
            barTitle: path,
            visibleItems: null,
            searchOpen: false
        })
    }

    back() {
        let currentPage = this.state.activePage? this.state.activePage : ''
        let newPage = currentPage.includes('/')? currentPage.split('/', 1)[0] : null
        this.gotoPage(newPage)
    }

    toggleSearch(open) {
        this.setState({
            searchOpen: open,
            visibleItems: null
        })
    }

    transliterate(amh) {
        let eng = ''
        for (let char of amh) {
            eng += filterEngData[char] || ' '
        }
        return eng
    }

    getFilterableData(main) {
        let filterableList = []
        let data = main.data
        for (let category of Object.keys(data)) {
            for (let title of Object.keys(data[category].data)) {
                filterableList.push({
                    title,
                    ...data[category].data[title],
                    category: category,
                    titleEng: this.transliterate(title)
                })
            }
        }
        return filterableList
    }

    filterItems(event) {
        let by = event.target.value
        let patt = new RegExp(by.toLowerCase().split('').join('.*?')) // for the english
        if (by) {
            let filtered = []
            for (let m of this.filterable) {
                if (m.title.includes(by) ||
                    m.body.includes(by) ||
                    patt.test(m.titleEng)) {
                    filtered.push(m)
                }
            }
            this.setState({visibleItems: filtered})
        } else {
            this.setState({visibleItems: null})
        }
    }

    render() {
        return (
            <div>
                <Head
                    style={{position: 'relative'}}
                    back={this.back}
                    searchOpen={this.state.searchOpen}
                    toggleSearch = {this.toggleSearch}
                    Title={this.state.barTitle}
                    filterItems={this.filterItems}
                    homeTitle={this.homeTitle}
                    date={mezmurData.date}
                    count={mezmurData.count}
                />
                <div style={{padding: '.25em', marginTop: 56}}>
                    <Browse
                        data={mezmurData}
                        gotoPage={this.gotoPage}
                        activePage={this.state.activePage}
                        visibleItems={this.state.visibleItems}
                    />
                </div>
            </div>
        )
    }
}

ReactDOM.render(<App />, document.getElementById('app'))
