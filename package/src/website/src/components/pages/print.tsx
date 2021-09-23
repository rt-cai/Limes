import React from "react";
import { PrintProps } from '../../models/props';
import { Typography, TextField, Grid, Card, Button, LinearProgress, Fade, CircularProgress} from '@material-ui/core';
import { DataGrid, GridColDef, GridRowParams } from '@material-ui/data-grid';
import { ApiService } from "../../services/api";
import { Sample } from "../../models/common";

enum LabelType {
    SAMPLE = 'Sample',
    STORAGE_LOCATION = 'Location',
    CUSTOM = 'Unknown',
}

interface LabelData {
    id: string
    bar: string
    text: string
    type: LabelType
}

interface PrintState {
    labels: LabelData[]
    labelsRaw: string
    printDisabled: boolean
    printAllDisabled: boolean
    lastChange: number
    printing: boolean
    gettingData: boolean
    labelTemplateName: string
}

export class PrintComponent extends React.Component<PrintProps, PrintState> {
    private apiService: ApiService
    private readonly UPDATE_DELAY = 650;

    constructor(props: PrintProps) {
        super(props)
        this.apiService = props.elabService
        this.state = {
            labels: [],
            labelsRaw: '',
            printDisabled: true,
            printAllDisabled: false,
            lastChange: Date.now(),
            printing: false,
            gettingData: false,
            labelTemplateName: ''
        }
    }

    private toBarcodes(samples: Sample[] | undefined) {
        if (!samples) return []
        return samples.map((samp) => {
            const S = samp.id
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
        if (this.props.startingSamples) {
            this.parseLabels(this.toBarcodes(this.props.startingSamples))
        }
    }

    private parseLabels(labels:string[]=[]) {
        if (labels.length===0) {
            labels = this.state.labelsRaw.split('\n')
        }
        labels = labels.filter((s)=>{return s.trim().length>0})
        const isInteger = (v: string) => !/[^0-9]/.test(v)
        const isBarcode = labels.map(isInteger)
        const barcodes = labels.filter(isInteger)

        const dispBar = (bar: string) => {
            const cut = Math.max(0, bar.length - 5)
            return cut? `...${bar.substring(cut,)}` : bar
        }

        this.apiService.BarcodeLookup(barcodes)
        .then((data)=>{
            const newLabels: LabelData[] = labels.map((l) => {
                if (data[l] === undefined) {
                    const tokens = l.includes('\t')? l.split('\t'): l.split(' ')
                    const ret = {
                        id: '',
                        bar: '',
                        text: l,
                        type: LabelType.CUSTOM,
                    }
                    if (tokens.length > 1 && isInteger(tokens[0])) {
                        const temp = tokens.shift();
                        ret.bar = temp? dispBar(temp): '';
                        ret.id = temp? temp: '';
                        ret.text = tokens.join(' ');
                    } else {
                        ret.id = ''
                        ret.bar = ''
                        ret.text = l
                    }
                    return ret
                } else {
                    // console.log(data[l])
                    const d: any = data[l]
                    return {
                        bar: dispBar(l),
                        id: l,
                        text: d.name,
                        type: d['sampleID']? LabelType.SAMPLE: LabelType.STORAGE_LOCATION,
                    }
                }
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
        this.setState({
            labelsRaw: sampleInputText,
            lastChange: Date.now()
        })

        setTimeout(() => {
            const now = Date.now()
            if (now - this.state.lastChange >= this.UPDATE_DELAY) {
                this.parseLabels()
            }
        }, this.UPDATE_DELAY);
    }

    private onPrint() {

    }

    private onPrintAll() {
        const data = {
            Labels: this.state.labels.map((l) => {
                return { Barcode: l.id, Texts: [l.text] }
            }),
            TemplateName: this.state.labelTemplateName 
        }

        this.setState({
            printing: true
        })

        const stop = () => {
            this.setState({
                printing: false
            })
        }

        this.apiService.PrintLabels(data).then(id=>{
            let tries = 25
            const poll = () => {
                tries--;
                if (tries <= 0) {
                    stop()
                    return
                }
                setTimeout(() => {
                    this.apiService.PollPrintReport(id).then((m) => {
                        if (!m || m==='') {
                            poll()
                        } else {
                            stop()
                            alert(m)
                        }
                    })
                }, 500);
            }
            poll()
        })


    }

    render(): JSX.Element {
        const sampleColumns: GridColDef[] = [
            { field: 'disabled', hide: true },
            { field: 'id', headerName: 'ID', hide: true },
            { field: 'bar', headerName: 'Barcode', width: 100, sortable: false },
            { field: 'text', headerName: 'Text', width: 600, sortable: false },
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
            '123 box 23',
            '005000000123456',
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
                                style={{ width: '70em' }}
                                defaultValue={this.toBarcodes(this.props.startingSamples).join('\n')}
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
                                // checkboxSelection
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
                                label="Label Template Name"
                                placeholder={'default'}
                                variant="outlined"
                                style={{ width: '70em' }}
                                onChange={(e) => { this.setState({labelTemplateName: e.target.value}) }}
                            >
                            </TextField>
                        </Grid>
                        <Grid item>
                            {/* <Button
                                variant="contained"
                                color="primary"
                                disabled={this.state.printDisabled}
                                style={buttonStyle}
                                onClick={() => this.onPrint()}>
                                Print
                            </Button> */}
                            <Button
                                variant="contained"
                                color="primary"
                                disabled={this.state.printAllDisabled}
                                style={buttonStyle}
                                onClick={() => this.onPrintAll()}>
                                Print All
                            </Button>
                        </Grid>
                    </Grid>
                </Card>
            </Grid>
        )
    }
}