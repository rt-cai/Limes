import React from "react";
import { StorageSearchProps } from '../../models/props';
import { Typography, TextField, Grid, Card, Button, LinearProgress, Fade, CircularProgress } from '@material-ui/core';
import { DataGrid, GridColDef, GridRowParams } from '@material-ui/data-grid';
import { ApiService } from "../../services/api";

interface Storage {
    id: number
    name: string
    parent: number
    children: Storage[]
}

interface SampleRow {
    id: number
    name: string
    type: string
}

interface SearchState {
    searching: boolean
    currentLocation: string
    results: string
    lastChange: number
    storages: Storage[]
    selectedSamples: SampleRow[]
    errorText: string
    errorCands: string
    reloadingStorage: boolean
    searchText: string
}

export class StorageSearchComponent extends React.Component<StorageSearchProps, SearchState> {
    private apiService: ApiService
    private readonly UPDATE_DELAY = 650;
    constructor(props: StorageSearchProps) {
        super(props)
        this.apiService = props.elabService
        this.state = {
            searching: false,
            results: '',
            lastChange: Date.now(),
            storages: [],
            selectedSamples: [],
            errorText: '',
            errorCands: '',
            currentLocation: '',
            reloadingStorage: false,
            searchText: '',
        }
    }

    private setup() {
        this.apiService.GetStorages().then(res => {
            if (!res) return 0
            const allmap: Map<number, Storage> = res.reduce((acc: Map<number, Storage>, s: any) => {
                const name: string = s['name']
                const id = s['storageLayerID']
                const v: Storage = {
                    id: id,
                    name: name.toLowerCase(),
                    parent: s['parentStorageLayerID'],
                    children: [],
                }
                acc.set(id, v)
                return acc
            }, new Map())

            const parents: Storage[] = []
            allmap.forEach((v, k, map) => {
                if (v.parent === 0) {
                    parents.push(v)
                }else{
                    allmap.get(v.parent)?.children.push(v)
                }
            })

            this.setState({
                storages: parents
            })
        })
    }

    public componentDidMount() {
        let tries = 5
        const doTry = () => {
            if (this.apiService.LoggedIn()) {
                this.setup()
            } else {
                tries --;
                if (tries <= 0) return
                setTimeout(() => {
                    doTry()
                }, 100);
            }
        }
        doTry()
    }

    private doSearch(text: string) {
        return new Promise<number>((resolve) => {
            const search = text.split(',').map((x)=> {return x.trim()})

            const subsearch = (arr: Storage[], q: string) => {
                const terms = q.split(' ')
                const cands = arr.filter((s) => {
                    return terms.reduce((acc: boolean, term) => {
                        return acc && s.name.includes(term)
                    }, true)
                })
                return cands
            }

            this.setState({
                errorText: '',
                errorCands: '',
                currentLocation: '',
            })

            let res = []
            let found
            let success = true
            let domain = this.state.storages
            for (let term of search) {
                term = term.toLowerCase()
                const cands = subsearch(domain, term)
                if (cands.length === 1) {
                    const s = cands[0]
                    domain = s.children
                    res.push(s.name)
                    found = s
                } else if (cands.length === 0) {
                    success = false
                    const currentLoc = res.join(', ')
                    this.setState({
                        searching: false,
                        errorText: term && term.length>0? `No storage location with name [${term}]`: `Maybe you have an extra comma?`,
                        errorCands: currentLoc.length>0? ` in ${currentLoc}` : ``,
                    })
                    break
                } else { // more than one
                    success = false
                    this.setState({
                        searching: false,
                        errorText: term && term.length>0? `Ambiguity for [${term}] between:` : `Specify one of:`,
                        errorCands: `${cands.map((s) => {return s.name}).join(', ')}`,
                    })
                    break
                }
            }
    
            if (success && found) {
                let bar = `${found.id}`
                while (bar.length < 12) bar = `0${bar}`
                if (bar.length == 12) bar = `008${bar}`
                while (bar.length < 15) bar = `0${bar}`
                this.setState({
                    currentLocation: `${res.join(', ')} - ${bar}`
                })
                resolve(found.id)
            } else {
                return resolve(0)
            }
        })
    }

    private getSamples(id: number) {
        return this.apiService.GetSamplesByStorage(id).then((samples: any[]) => {
            if (!samples) samples = []
            this.setState({
                selectedSamples: samples.map((s) => {
                    return {
                        id: s.sampleID,
                        name: s.name,
                        type: s.sampleType.name
                    }
                }),
                searching: false
            })
        })
    }

    private onSearchChanged(e: any=undefined) {
        const searchText = e? e.target.value: this.state.searchText;
        this.setState({
            lastChange: Date.now(),
            searchText: searchText,
        })

        setTimeout(() => {
            const now = Date.now()
            if (now - this.state.lastChange >= this.UPDATE_DELAY) {
                this.setState({
                    searching: true
                })

                this.doSearch(searchText)
                .then((id: number) => {
                    if (id === 0) return
        
                    return this.getSamples(id)
                })
            }
        }, this.UPDATE_DELAY);
    }

    private onReloadStorages() {
        this.setState({
            reloadingStorage: true,
        })
        this.apiService.ReloadStorages().then((s)=>{
            if (s == 200) {
                this.setup()
                this.onSearchChanged()
            }
            this.setState({
                reloadingStorage: false,
            })
        })
    }

    render(): JSX.Element {
        // const classes = this.classes
        const sampleColumns: GridColDef[] = [
            { field: 'disabled', hide: true },
            { field: 'id', headerName: 'Barcode', width: 100, sortable: false },
            { field: 'name', headerName: 'Name', width: 400, sortable: false },
            { field: 'type', headerName: 'Type', width: 350, sortable: false },
        ]

        const outerStyle: React.CSSProperties = {
            marginTop: '5vh',
            justifyContent: 'center',
            alignItems: 'center',
            alignContent: 'center',
            // border: '1px solid orange'
        }
        const cardStyle: React.CSSProperties = {
            // border: '1px solid green',
            width: '90vw',
            padding: '2em',
        }
        const buttonStyle: React.CSSProperties = {
            margin: '0 1em 0 1em'
        }
        const inputPlaceholder = 'freezer 7, self 2, rack 3'
        return (
            <Grid container justifyContent='center' style={outerStyle}>
                <Card style={cardStyle}>
                    <Grid container direction="column" spacing={3}>
                        <Grid item>
                            <Typography variant="h5" component="h2" align="left" gutterBottom={true} style={{}}>
                                Samples By Storage Location
                            </Typography>
                        </Grid>
                        <Grid item>
                            <TextField
                                    label="Search"
                                    placeholder={inputPlaceholder}
                                    variant="outlined"
                                    onChange={this.onSearchChanged.bind(this)}
                                    style={{
                                        width: "90vw"
                                    }}
                                >
                            </TextField>
                        </Grid>
                        <Grid item>
                            <Typography align="left" style={{
                                color: 'primary',
                            }}>
                                {this.state.currentLocation}
                            </Typography>
                            <Typography align="left" style={{
                                color: 'red',
                            }}>
                                {this.state.errorText}
                            </Typography>
                            <Typography align="left" style={{
                                color: 'red',
                            }}>
                                {this.state.errorCands}
                            </Typography>
                        </Grid>
                        <Grid item style={{ height: '30em' }} justify="center">
                            <Fade in={this.state.searching} style={{
                                position: 'absolute',
                                marginTop: '5em',
                            }}>
                                <CircularProgress size={50} />
                            </Fade>
                            <DataGrid
                                rows={this.state.selectedSamples}
                                columns={sampleColumns}
                                rowsPerPageOptions={[100]}
                                onPageSizeChange={() => { }}
                                isRowSelectable={(params: GridRowParams) => !params.row.disabled}
                                disableSelectionOnClick
                                disableColumnMenu
                                disableColumnFilter
                                disableColumnSelector
                                style={{ opacity: this.state.searching ? 0.25 : 1 }}
                            />
                        </Grid>
                        <Grid item>
                            <Button
                                variant="contained"
                                color="primary"
                                onClick={() => {this.props.onPrintCallback(this.state.selectedSamples.map((s)=>s.id))}}
                                style={buttonStyle}
                            >
                                Print Labels
                            </Button>
                            <Button
                                variant="contained"
                                color="secondary"
                                disabled={this.state.reloadingStorage}
                                onClick={this.onReloadStorages.bind(this)}
                                style={buttonStyle}
                            >
                                Reload Storages
                                <Fade in={this.state.reloadingStorage} style={{position: 'absolute'}}>
                                    <CircularProgress size={33} color='secondary'/>
                                </Fade>
                            </Button>
                        </Grid>
                    </Grid>
                </Card>
            </Grid>
        )
    }
}