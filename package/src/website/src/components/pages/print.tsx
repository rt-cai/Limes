import React from "react";
import { PrintProps } from '../../models/props';
import { Typography, TextField, Grid, Card, Button, LinearProgress, Fade, CircularProgress, MenuItem} from '@material-ui/core';
import { DataGrid, GridColDef, GridRowParams } from '@material-ui/data-grid';
import RefreshRoundedIcon from '@mui/icons-material/RefreshRounded';
import { ApiService } from "../../services/api";
import { Sample } from "../../models/common";

enum LabelType {
    SAMPLE = 'Sample',
    STORAGE_LOCATION = 'Location',
    CUSTOM = 'Unknown',
}

interface LabelData {
    id: number
    bar: string
    bardisp: string
    name: string 
    addText: string
    type: LabelType
    tokens: string[]
}

interface PrintState {
    labels: LabelData[]
    labelsRaw: string
    printDisabled: boolean
    printAllDisabled: boolean
    printing: boolean
    gettingData: boolean
    labelTemplateName: string
    printerName: string
    availablePrinters: string[]
    availableTemplates: string[]
    refreshing: boolean
    copied: number
}

export class PrintComponent extends React.Component<PrintProps, PrintState> {
    private apiService: ApiService;
    private readonly UPDATE_DELAY = 650;
    private lastChange: number;
    private readonly NO_ELAB_RECORD = '*(No eLab Record)';

    constructor(props: PrintProps) {
        super(props)
        this.apiService = props.elabService
        this.lastChange = Date.now();
        this.state = {
            labels: [],
            labelsRaw: '',
            printDisabled: true,
            printAllDisabled: false,
            printing: false,
            gettingData: false,
            labelTemplateName: '',
            printerName: '',
            availablePrinters: [],
            availableTemplates: [],
            refreshing: false,
            copied: 0
        }
    }

    private toBarcodes(samples: Sample[] | undefined) {
        if (!samples) return []
        return samples.map((samp) => {
            const S = samp.barcode
            const BAR_L = 15
            const PRE = '005'
            let bar = `${S}`
            while (bar.length < BAR_L - PRE.length) {
                bar = `0${bar}`
            }
            return `${PRE}${bar}`
        })
    }

    public componentDidMount() {
        if (this.props.startingBarcodes) {
            this.parseLabels(this.props.startingBarcodes.map((n)=>`${n}`))
        }
        this.onRefresh()
    }

    private parseLabels(labels:string[]=[]) {
        if (labels.length===0) {
            labels = this.state.labelsRaw.split('\n')
        }
        labels = labels.filter((s)=>{return s.trim().length>0})
        const l_tokens: string[][] = labels.map((l)=>l.includes('\t')? l.split('\t'): l.split(',').map(t=>t.trim()))
        // const isInteger = (v: string) => !/[^0-9]/.test(v)
        const barcodes: string[] = l_tokens.map((tok)=>tok[0])

        const dispBar = (bar: string) => {
            const cut = Math.max(0, bar.length - 5)
            return cut? `...${bar.substring(cut,)}` : bar
        }

        this.apiService.BarcodeLookup(barcodes)
        .then((raw)=>{
            const data = raw? raw : {}
            let id = 0;
            const newLabels: LabelData[] = l_tokens.map((tokens) => {
                const tf = tokens.shift()
                const ret = {
                    id: id,
                    bar: tf? tf:'',
                    bardisp: tf? dispBar(tf): '',
                    addText: tokens.join(', '),
                    name: this.NO_ELAB_RECORD,
                    type: LabelType.CUSTOM,
                    tokens: tokens,
                }

                if (tf) {
                    let bar: string = tf
                    if (Number(bar)) {
                        while (bar.length < 12) bar = `0${bar}`
                        if (bar.length == 12) bar = `005${bar}`
                        while (bar.length < 15) bar = `0${bar}`
                    }
                    // console.log(data)
                    // console.log(bar) 
                    if (data[bar]) {
                        const d: any = data[bar]
                        ret.name = d?.name
                        const altbar = data[bar]?.altID
                        if (altbar) {
                            ret.bar = altbar
                            ret.bardisp = altbar
                        } else {
                            ret.bar = bar
                        }
                        ret.type = d?.sampleID? LabelType.SAMPLE: LabelType.STORAGE_LOCATION
                        // console.log(ret)
                    }
                }

                id += 1
                return ret
            })
            this.setState({
                labels: newLabels
            })
        }).catch((err)=>{
            console.error(err);
        }).finally(()=>{
            this.setState({
                gettingData: false
            })
        })

        this.setState({
            gettingData: true
        })
    }

    private onLabelInputChanged(e: any) {
        const sampleInputText = e.target.value;
        this.lastChange = Date.now()
        setTimeout(() => {
            const now = Date.now()
            if (now - this.lastChange >= this.UPDATE_DELAY) {
                this.setState({
                    labelsRaw: sampleInputText,
                })
                this.parseLabels()
            }
        }, this.UPDATE_DELAY);
    }

    private awaitResults(id: any): Promise<any> {
        return new Promise((resolve, reject)=> {
            let tries = 25
            const poll = () => {
                tries--;
                if (tries <= 0) {
                    reject()
                }
                setTimeout(() => {
                    this.apiService.PollPrintInfo(id).then((data) => {
                        if (data.Success) {
                            resolve(data.Data)
                        } else {
                            poll()
                        }
                    })
                }, 500);
            }
            poll();
        })
    }

    private onPrintAll() {
        const data = {
            Labels: this.state.labels.map((l) => {
                const first = l.name===this.NO_ELAB_RECORD? [] : [l.name]
                return { Barcode: l.bar, Texts: first.concat(l.tokens) }
            }),
            TemplateName: this.state.labelTemplateName,
            PrinterName: this.state.printerName,
        }

        this.setState({
            printing: true
        })

        this.apiService.PrintLabels(data).then(id=>{
            return this.awaitResults(id)
        }).then((data: any) => {
            console.log(data)
            alert(data.Message)
        }).catch(() => {
            // ignore
        }).finally(()=> [
            this.setState({
                printing: false
            })
        ])


    }

    private onRefresh() {
        this.setState({
            refreshing: true,
        })
        this.apiService.RefreshPrintInfo().then(id=>{
            return this.awaitResults(id)
        }).then((data)=> {
            // console.log(data)
            const printers = data.printers && data.printers.length>0? 
                data.printers.filter((p: string)=>{
                    return p.toLowerCase().includes('label')
                }) : ['default']
            const templates = data.templates && data.templates.length>0? data.templates : ['default']
            this.setState({
                availablePrinters: printers,
                availableTemplates: templates,
                refreshing: false,
            })
        })
    }

    private onToClipboard() {
        this.setState({
            copied: this.state.copied + 1
        })
        const DELIM = '\t'
        const header: string = [`Name (don't copy back)`, `Barcode`, `Addtional Text`].join(DELIM)
        const rows: string[] = this.state.labels.map((l)=>{
            return [l.name, l.bar, l.addText].join(DELIM)
        })
        const full: string = [header].concat(rows).join('\n')
        navigator.clipboard.writeText(full)

        setTimeout(() => {
            this.setState({
                copied: this.state.copied - 1
            })
        }, 1000);
    }

    render(): JSX.Element {
        const sampleColumns: GridColDef[] = [
            { field: 'disabled', hide: true },
            { field: 'id', headerName: 'ID', hide: true },
            { field: 'bardisp', headerName: 'Barcode', width: 100, sortable: false },
            { field: 'name', headerName: 'Item Name', width: 400, sortable: false },
            { field: 'addText', headerName: 'Additional Text', width: 600, sortable: false },
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
            // width: '80vw',
            padding: '2em',
        }
        const buttonStyle: React.CSSProperties = {
            margin: '0 1em 0 1em'
        }
        const inputPlaceholder = [
            '005000000123456',
            '005000000123456, some additional info',
            '...'
        ].join('\n')

        return (
            <Grid container justifyContent='center' style={outerStyle}>
                <Card style={cardStyle}>
                    <Grid container direction="column" spacing={3}>
                        <Grid item>
                            <Typography variant="h5" component="h2" align="left" gutterBottom={true} style={{}}>
                                Print Labels
                            </Typography>
                        </Grid>
                        <Grid item>
                            <TextField
                                label="Items"
                                placeholder={inputPlaceholder}
                                multiline
                                variant="outlined"
                                style={{ width: '70em'}}
                                defaultValue={this.props.startingBarcodes?.map((n)=>`${n}`).join('\n')}
                                onChange={(e) => { this.onLabelInputChanged(e) }}
                            >
                            </TextField>
                        </Grid>
                        <Grid item style={{ height: '30em'}} justify="center">
                            <Fade in={this.state.gettingData} style={{
                                position: 'absolute',
                                marginTop: '5em',
                            }}>
                                <CircularProgress size={50}/>
                            </Fade>
                            <DataGrid
                                rows={this.state.labels}
                                columns={sampleColumns}
                                rowsPerPageOptions={[100]}
                                onPageSizeChange={() => {}}
                                isRowSelectable={(params: GridRowParams) => !params.row.disabled}
                                disableSelectionOnClick
                                disableColumnMenu
                                disableColumnFilter
                                disableColumnSelector
                                style={{opacity: this.state.gettingData? 0.25: 1}}
                            />
                            <Grid item>
                                <Fade in={this.state.printing}>
                                    <LinearProgress />
                                </Fade>
                            </Grid>
                        </Grid>
                        <Grid item>
                            <TextField
                                select
                                label="Label Template"
                                variant="outlined"
                                style={{ width: '20.5em' , marginRight: '1em' }}
                                value={this.state.labelTemplateName}
                                // onChange={handleChange}
                                onChange={(e) => { this.setState({labelTemplateName: e.target.value}) }}
                            >
                                {this.state.availableTemplates.map((option) => (
                                    <MenuItem key={option} value={option}>
                                        {option}
                                    </MenuItem>
                                ))}
                            </TextField>
                            <TextField
                                select
                                label="Printer Name"
                                variant="outlined"
                                style={{ width: '20em' }}
                                value={this.state.printerName}
                                onChange={(e) => { this.setState({ printerName: e.target.value }) }}
                            >
                                {this.state.availablePrinters.map((option) => (
                                    <MenuItem key={option} value={option}>
                                        {option}
                                    </MenuItem>
                                ))}
                            </TextField>
                            <Button
                                variant="contained"
                                color="primary"
                                onClick={this.onRefresh.bind(this)}
                                disabled={this.state.refreshing}
                                style={{
                                    margin: '0.6em',
                                }}
                            >
                                <Fade in={this.state.refreshing} style={{position: 'absolute'}}>
                                    <CircularProgress size={33}/>
                                </Fade>
                                <RefreshRoundedIcon />
                            </Button>
                        </Grid>
                        <Grid item>
                            <Button
                                variant="contained"
                                color="primary"
                                disabled={!this.state.labelTemplateName || !this.state.printerName}
                                style={buttonStyle}
                                onClick={() => this.onPrintAll()}>
                                Print All
                            </Button>
                            <Button
                                variant="contained"
                                color="primary"
                                style={buttonStyle}
                                onClick={this.onToClipboard.bind(this)}>
                                Copy to Clipboard {this.state.copied>0? `✔` : ``}
                            </Button>
                        </Grid>
                    </Grid>
                </Card>
            </Grid>
        )
    }
}