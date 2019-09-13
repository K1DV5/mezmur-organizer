import React from 'react'
import ReactDOM from 'react-dom'
import Search from './components/Search'
import mez from '../mezmur/mez.json'
import filterEngData from './amhMatch.json'
import Browse from './components/Browse'

window.mezmurData = mez
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
        this.filterable = this.getFilterableData(mez)
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
            for (let m of data[category].data) {
                filterableList.push({
                    ...m,
                    category: category,
                    titleEng: this.transliterate(m.title)
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
                <Search
                    style={{position: 'relative'}}
                    back={this.back}
                    searchOpen={this.state.searchOpen}
                    toggleSearch = {this.toggleSearch}
                    Title={this.state.barTitle}
                    filterItems={this.filterItems}
                    homeTitle={this.homeTitle}
                    date={mez.date}
                    count={mez.count}
                />
                <div style={{padding: '.25em'}}>
                    <Browse
                        data={mez}
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
