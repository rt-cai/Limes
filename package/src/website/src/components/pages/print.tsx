import React from "react";
import { PrintProps } from '../../models/props';
import { Typography, TextField, Grid, Card, Button, LinearProgress, Fade, CircularProgress } from '@material-ui/core';
import { DataGrid, GridColDef, GridRowParams } from '@material-ui/data-grid';
import { ApiService } from "../../services/api";

enum LabelType {
    SAMPLE = 'Sample',
    STORAGE_LOCATION = 'Location',
    CUSTOM = 'Unknown',
}

interface SampleInfo {
    id: string // barcode
    name: string
    type: LabelType
    disabled?: boolean
}

interface PrintState {
    labels: SampleInfo[]
    labelsRaw: string
    printDisabled: boolean
    printAllDisabled: boolean
    lastChange: number
    sendingPrint: boolean
    gettingData: boolean
}

export class PrintComponent extends React.Component<PrintProps, PrintState> {
    private elabService: ApiService
    private readonly UPDATE_DELAY = 650;

    constructor(props: PrintProps) {
        super(props)
        this.elabService = props.elabService
        this.state = {
            labels: [],
            labelsRaw: '',
            // labelsRaw: '',
            printDisabled: true,
            printAllDisabled: false,
            lastChange: Date.now(),
            sendingPrint: true,
            gettingData: false,
        }
    }

    private parseLabels() {
        const labels = this.state.labelsRaw.split('\n')
        const isInteger = (v: string) => !/[^0-9]/.test(v)
        const isBarcode = labels.map(isInteger)
        const barcodes = labels
        .filter(isInteger)

        this.elabService.BarcodeLookup(barcodes)
        .then((data)=>{
            const newLabels: SampleInfo[] = labels.map((l) => {
                if (data[l] == undefined) {
                    const tokens = l.split(' ')
                    const ret = {
                        id: '',
                        name: '',
                        type: LabelType.CUSTOM,
                    }
                    if (tokens.length > 1 && isInteger(tokens[0])) {
                        const temp = tokens.shift();
                        ret.id = temp? temp: ''
                        ret.name = tokens.join(' ');
                    } else {
                        ret.id = ''
                        ret.name = l
                    }
                    return ret
                } else {
                    // console.log(data[l])
                    const d: any = data[l]
                    return {
                        id: `...${l.substring(10,)}`,
                        name: d.name,
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
        console.log(this.state.labelsRaw)
    }

    render(): JSX.Element {
        const sampleColumns: GridColDef[] = [
            { field: 'disabled', hide: true },
            { field: 'id', headerName: 'Barcode', width: 100, sortable: false },
            { field: 'name', headerName: 'Name', width: 400, sortable: false },
            { field: 'type', headerName: 'Type', width: 100, sortable: false },
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
            'box 23',
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
                                checkboxSelection
                                disableSelectionOnClick
                                disableColumnMenu
                                disableColumnFilter
                                disableColumnSelector
                                style={{opacity: this.state.gettingData? 0.25: 1}}
                            />
                            <Grid item>
                                <Fade in={this.state.sendingPrint}>
                                    <LinearProgress />
                                </Fade>
                            </Grid>
                        </Grid>
                        <Grid item>
                            <Button
                                variant="contained"
                                color="primary"
                                disabled={this.state.printDisabled}
                                style={buttonStyle}
                                onClick={() => this.onPrint()}>
                                Print
                            </Button>
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