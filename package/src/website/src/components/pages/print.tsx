import React from "react";
import { PrintProps } from '../../models/props';
import { Typography, TextField, Grid, Card, Button, LinearProgress, Fade, CircularProgress } from '@material-ui/core';
import { DataGrid, GridColDef, GridRowParams } from '@material-ui/data-grid';
import { ApiService } from "../../services/api";

enum LabelType {
    SAMPLE = 'Sample',
    STORAGE_LOCATION = 'Storage'
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
            labels: [
                {
                    id: '005000009764619',
                    name: 'example box',
                    type: LabelType.STORAGE_LOCATION,
                    disabled: true,
                },
                {
                    id: '1234567',
                    name: 'example sample',
                    type: LabelType.SAMPLE,
                },
            ],
            labelsRaw: '12345\n1x\n0001\na',
            // labelsRaw: '',
            printDisabled: true,
            printAllDisabled: false,
            lastChange: Date.now(),
            sendingPrint: true,
            gettingData: false,
        }

        setTimeout(() => {
        this.elabService.BarcodeLookup(['008000000783959', '005000009764619', '005000009764621'])
        }, 500)
    }

    private parseLabels() {
        const labels = this.state.labelsRaw.split('\n')
        const barcodes = labels
        .filter((v) => !/[^0-9]/.test(v))

        this.elabService.BarcodeLookup(barcodes)
        .then((x)=>{

        }).catch((err)=>{
            console.error(err);
        })

        this.setState({
            gettingData: true
        })
        setTimeout(() => {
            this.setState({
                gettingData: false
            })
        }, 1000);
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
            { field: 'id', headerName: 'Barcode', width: 150, sortable: false },
            { field: 'name', headerName: 'Name', width: 150, sortable: false },
            { field: 'type', headerName: 'Type', width: 150, sortable: false },
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