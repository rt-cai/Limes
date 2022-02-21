import React from "react";
import BarcodeScannerComponent from "react-qr-barcode-scanner";
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormControl from '@mui/material/FormControl';
// import FormLabel from '@mui/material/FormLabel';
import { Typography, Grid, Card, Button, CircularProgress, Fade, Container } from '@material-ui/core';
import { ScannerProps } from '../../models/props';
import { ApiService } from "../../services/api";
import { DataGrid, GridColDef, GridRowParams, GridSelectionModel } from '@material-ui/data-grid';

// enum Modes {
//     ELAB, LINK
// }

enum ScanType {
    UNK, EXISTING
}

interface ScanInfo {
    barcode: string
    id: number
    info: string
    raw: any
    type: ScanType
}

interface ScannerState {
    scans: Map<number, ScanInfo>
    selectedScanIDs: GridSelectionModel
    lastID: number
    cardBorderColour: any
    w: number
    h: number
    // mode: Modes
    // actionButtonName: string
    actionDisabled: boolean
    redirecting: boolean
    working: boolean
}

export class ScannerComponent extends React.Component<ScannerProps, ScannerState> {
    private apiService: ApiService
    private readonly NO_SCAN: string = "Nothing Scanned"

    constructor(props: ScannerProps) {
        super(props)
        this.apiService = props.elabService
        this.state = {
            scans: new Map(),
            selectedScanIDs: [],
            lastID: -1,
            cardBorderColour: 'transparent',
            w: 300,
            h: 300,
            // mode: Modes.ELAB,
            // actionButtonName: 'Open',
            actionDisabled: true,
            redirecting: false,
            working: false,
        }
    }

    public componentDidMount() {
        const [w, h] = [window.innerWidth, window.innerHeight]
        const l = w < h ? w : h
        if (l < this.state.w) {
            this.setState({
                w: w - 20,
                h: w - 20,
            })
        }
    }

    private onScan(code: string) {
        const newscans = this.state.scans
        return new Promise<void>((resolve, reject) => {
            this.setState({
                cardBorderColour: this.props.theme.palette.primary.main,
                working: true,
            }, () => resolve());

            const setcol = (col: any, t: number) => {
                return new Promise<void>((r, j) => {
                    setTimeout(() => {
                        this.setState({
                            cardBorderColour: col
                        });
                        r();
                    }, t);
                })
            }

            setcol('transparent', 100)
                .then(() => setcol(this.props.theme.palette.primary.main, 60))
                .then(() => setcol('transparent', 500))

        }).then(() => {
            const ID = this.state.lastID+1

            const searchCache = (): Promise<ScanInfo|undefined> => {
                let foundScan: ScanInfo | null = null
                for (let [id, info] of newscans) {
                    if (info.barcode === code) {
                        foundScan = info
                        newscans.delete(id)
                        break
                    }
                }
                return Promise.resolve(foundScan? foundScan : undefined)
            }

            const searchELab = (): Promise<ScanInfo|undefined> => {
                return this.apiService.BarcodeLookup([code]).then((results) => {
                    const remote = Object.keys(results).filter((c) => c === code)
                    const result = remote.length > 0 ? results[remote[0]] : null
                    if (result) {
                        const newinfo: ScanInfo = {
                            barcode: code,
                            id: ID,
                            info: result.name,
                            type: ScanType.EXISTING,
                            raw: result,
                        }
                        return newinfo
                    }
                })
            }

            const methods = [searchCache, searchELab]

            const attempt = (i: number) => {
                return methods[i]()
            }

            const attemptAll = (i: number): Promise<ScanInfo> => {
                return attempt(i).then((result) => {
                    if (result) {
                        return result
                    } else if (i+1 < methods.length) {
                        return attemptAll(i+1)
                    } else {
                        const unk: ScanInfo = {
                            barcode: code,
                            id: ID,
                            info: "Unknown",
                            type: ScanType.UNK,
                            raw: {},
                        }
                        return unk
                    }
                })
            }
            return attemptAll(0)
        }).then((newinfo: ScanInfo) => {
            newscans.set(newinfo.id, newinfo)
            this.setState({
                scans: newscans,
                working: false,
                lastID: Math.max(newinfo.id, this.state.lastID),
            })
        })
    }

    private updateInfo() {
        // currently not used
        // for future feedback of actions
    }

    private updateCanAct() {
        const selected = this.state.selectedScanIDs
        const scans = this.state.scans
        let canAct: boolean = false

        canAct = selected
        .map((i) => scans.get(Number(i)))
        .reduce((p: boolean, c) => p || c?.type === ScanType.UNK, false)

        this.setState({
            actionDisabled: !canAct
        })
    }

    private tryNavigateRow(row: GridRowParams) {
        const scans = this.state.scans
        const info = scans.get(Number(row.id))
        if (info?.type === ScanType.EXISTING) {
            window.open(info.raw.link, "_blank")
        }
    }

    private onAct() {
        for(let selected of this.state.selectedScanIDs) {
            const info = this.state.scans.get(Number(selected))
            console.log(`impliment add - ${info?.barcode} ${info?.info}`)
        }   
        // this.setState({working: true})
        // this.apiService.AddMmapSample(this.state.lastCode).then((r) => {
        //     const info = this.state.scanInfo
        //     if (info.length > 1) info.pop()
        //     if (r.Code == 200) {
        //         info.push('Add success')
        //     } else {
        //         if(r.Error === "Barcode exists"){
        //             info.push('Sample already added')
        //         } else if (r.Code == 404) {
        //             info.push('Unknown barcode')
        //         } else {
        //             info.push('Error')
        //         }
        //     }

        //     this.setState({working: false, scanInfo:info})
        // })
    }

    private onDeleteSelected() {
        const selected = new Set(this.state.selectedScanIDs)
        const scans = this.state.scans
        for (let selected of this.state.selectedScanIDs) {
            scans.delete(Number(selected))
        }
        this.setState({
            scans: scans
        }, () => this.updateInfo())
    }

    private onToClipboard() {
        navigator.clipboard.writeText([...this.state.scans.values()].reduce((p, c: ScanInfo) => {
            return `${p}\n${c.barcode}\t${c.info}`
        }, ''))
    }

    render(): JSX.Element {
        const outerStyle: React.CSSProperties = {
            marginTop: '5vh',
            justifyContent: 'center',
            alignItems: 'center',
            alignContent: 'center',
            // border: '1px solid orange'
        }

        const cardStyle: React.CSSProperties = {
            // border: '1px solid green',
            width: '90%',
            padding: '2em 0 2em 0',
            border: '5px solid',
            borderColor: this.state.cardBorderColour,
        }
        const buttonStyle: React.CSSProperties = {
            margin: '1em 1em 0 1em',
            // width: '6em',
        }

        return (
            <Grid container justifyContent='center' style={outerStyle}>
                <Card style={cardStyle}>
                    <Grid container direction="column" spacing={0}>
                        <Grid item>
                            <Typography variant="h5" component="h2" align="center" gutterBottom={false} style={{}}>
                                Scanner
                            </Typography>
                        </Grid>
                        <Grid item>
                            <Container style={{
                                // margin: '-3em 0 -3em 0',
                            }}>
                                <BarcodeScannerComponent
                                    width={this.state.w}
                                    height={this.state.h}
                                    facingMode="environment"
                                    onUpdate={(err, result) => {
                                        if (result) {
                                            this.onScan(result.getText())
                                                .then(() => this.updateInfo());
                                        }
                                    }}
                                />
                            </Container>

                        </Grid>
                        <Grid item>
                            <Typography
                                style={{
                                    color: 'primary',
                                    marginBottom: '0.4em'
                                }}>
                                *Double click on added rows to open in eLab
                            </Typography>
                        </Grid>
                        <Grid item>
                            <Container style={{
                                // margin: '-3em 0 -3em 0',
                                // height: '48em'
                            }}>
                                <DataGrid
                                    rows={[...this.state.scans.values()].map((o: ScanInfo) => {
                                        let row: any = o
                                        row.inElab = o.type != ScanType.UNK? '✓' : ''
                                        return row
                                    }).reverse()}
                                    columns={[
                                        // { field: 'disabled', hide: true },
                                        { field: 'id', headerName: 'ID', hide: true },
                                        { field: 'barcode', headerName: 'Barcode', width: 200, sortable: false },
                                        { field: 'inElab', headerName: 'Added?', width: 85, sortable: false },
                                        { field: 'info', headerName: 'Info', width: 700, sortable: false },
                                        // { field: 'addText', headerName: 'Additional Text', width: 600, sortable: false },
                                    ]}
                                    rowsPerPageOptions={[100]}
                                    onPageSizeChange={() => {}}
                                    // isRowSelectable={(params: GridRowParams) => !params.row.disabled}
                                    onSelectionModelChange={(ids: GridSelectionModel) => {
                                        this.setState({
                                            selectedScanIDs: ids,
                                        }, () => this.updateCanAct())
                                    }}
                                    onRowDoubleClick={(row) => this.tryNavigateRow(row)}
                                    disableSelectionOnClick
                                    checkboxSelection={true}
                                    disableColumnMenu
                                    disableColumnFilter
                                    disableColumnSelector
                                    style={{
                                            opacity: this.state.working? 0.25: 1,
                                            minHeight: `${12+this.state.scans.size*4}em`,
                                            maxHeight: '48em'
                                    }}
                                />
                                <Fade in={this.state.working} style={{position: 'absolute'}}>
                                    <CircularProgress size={33}/>
                                </Fade>
                            </Container>
                        </Grid>
                        <Grid item>
                            <Button
                                variant="contained"
                                color="secondary"
                                style={buttonStyle}
                                onClick={() => this.onDeleteSelected()}
                            >
                                Remove Selected
                            </Button>
                            <Button
                                variant="contained"
                                color="primary"
                                style={buttonStyle}
                                disabled={this.state.actionDisabled || this.state.redirecting}
                                onClick={()=> this.onAct()}
                            >
                                {/* {this.state.actionButtonName} */}
                                Recieve & Add
                                <Fade in={this.state.redirecting} style={{position: 'absolute'}}>
                                    <CircularProgress size={33}/>
                                </Fade>
                            </Button>
                            <Button
                                variant="contained"
                                color="primary"
                                style={buttonStyle}
                                // style={{ marginTop: '1em' }}
                                onClick={() => { this.onToClipboard() }}
                            >
                                Copy to Clipboard
                            </Button>
                        </Grid>
                    </Grid>
                </Card >
            </Grid >
        )
    }
}