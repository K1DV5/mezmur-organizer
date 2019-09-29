/** @jsx preact.h */
import preact from 'preact';
import Head from './components/Head'
import Browse from './components/Browse'

// import m from '../mez-data.json'
// mezmurData = m

// the data is from the template html
console.info('\nThe data is in the variable "mezmurData".\n"copy(mezmurData)" to copy it to the clipboard.\n\n')

class App extends preact.Component {
    constructor(props) {
        super(props)
        this.homeTitle = 'መዝሙር'
        this.state = {
            searchOpen: false,
            activePage: null,
            barTitle: null,
            visibleItems: null,
            catCount: null
        }
        this.filterable = this.getFilterableData(mezmurData)
        this.getFilterableData = this.getFilterableData.bind(this)
        this.filterItems = this.filterItems.bind(this)
        this.gotoPage = this.gotoPage.bind(this)
        this.back = this.back.bind(this)
        this.toggleSearch = this.toggleSearch.bind(this)
    }

    gotoPage(path) {
        let catCount = path && !path.includes('/') ? mezmurData.data[path.replace('-', ' ').trim()].count : null
        this.setState({
            activePage: path,
            barTitle: path,
            visibleItems: null,
            searchOpen: false,
            catCount: catCount
        })
    }

    back() {
        let currentPage = this.state.activePage ? this.state.activePage : ''
        let newPage = currentPage.includes('/') ? currentPage.split('/', 1)[0] : null
        this.gotoPage(newPage)
    }

    toggleSearch(open) {
        this.setState({
            searchOpen: open,
            visibleItems: null
        })
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
                    titleEng: data[category].data[title].title_eng
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
                    back={this.back}
                    searchOpen={this.state.searchOpen}
                    toggleSearch={this.toggleSearch}
                    Title={this.state.barTitle}
                    filterItems={this.filterItems}
                    homeTitle={this.homeTitle}
                    date={mezmurData.date}
                    count={mezmurData.count}
                    catCount={this.state.catCount}
                />
                <div style={{padding: '.25em', marginTop: 56}}>
                    {
                        <Browse
                            data={mezmurData}
                            gotoPage={this.gotoPage}
                            activePage={this.state.activePage}
                            visibleItems={this.state.visibleItems}
                        />
                    }
                </div>
            </div>
        )
    }
}

preact.render(<App />, document.getElementById('app'))
