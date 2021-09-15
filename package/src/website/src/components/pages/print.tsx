import React from "react";
import { PrintProps } from '../../models/props';
import { Typography, TextField, Grid, Card, Button } from '@material-ui/core';
import { DataGrid, GridColDef } from '@material-ui/data-grid';

interface SampleInfo {
    id: number // barcode
    name: string
}

interface PrintState {
    samples: SampleInfo[]
    sampleRaw: string
    printDisabled: boolean
    printAllDisabled: boolean
}

export class PrintComponent extends React.Component<PrintProps, PrintState> {
    constructor(props: PrintProps) {
        super(props)

        this.state = {
            samples: [
                {id: 123, name: 'a'},
                {id: 456, name: 'b'},
            ],
            sampleRaw: '',
            printDisabled: true,
            printAllDisabled: false,
        }
    }

    private onSampleInputChanged(e: any) {
        const sampleInputText = e.target.value;
        this.setState({sampleRaw: sampleInputText})
        // console.log(sampleInputText)
    }

    private onPrint() {

    }

    private onPrintAll() {
        console.log(this.state.sampleRaw)
    }

    render(): JSX.Element {
        const sampleColumns: GridColDef[] = [
            { field: 'id', headerName: 'Barcode', width: 150 },
            { field: 'name', headerName: 'Name', width: 150 },
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
            padding: '2vw',
        }
        const titleStyle: React.CSSProperties = {
            // border: '1px solid red'
        }
        const inputStyle: React.CSSProperties = {
            // border: '1px solid orange',
            width: '80vw',
            marginTop: '1vh'
        }
        const dataGridStyle: React.CSSProperties = {
            height: '50vh',
            marginTop: '1vh'
        }
        const buttonStyle: React.CSSProperties = {
            marginTop: '2vh',
            marginLeft: '1vw',
            marginRight: '1vw',
        }
        // 9764608
        const inputPlaceholder = '1234567\nhttps://elab.msl.ubc.ca/... /sampleID=1234567\n...'
        return (
            <Grid container justifyContent='center' style={outerStyle}>
                <Card style={cardStyle}>
                    <Typography variant="h5" component="h2" align="left" gutterBottom={true} style={titleStyle}>
                        Print Samples
                    </Typography>
                    <TextField
                        id="samplesInput"
                        label="Samples"
                        placeholder={inputPlaceholder}
                        multiline
                        variant="outlined"
                        style={inputStyle}
                        onChange={(e)=>{this.onSampleInputChanged(e)}}
                    >
                    </TextField>
                    <Grid style={dataGridStyle}>
                        <DataGrid
                            rows={this.state.samples}
                            columns={sampleColumns}
                            rowsPerPageOptions={[100]}
                            onPageSizeChange={() => {}}
                            checkboxSelection
                            disableSelectionOnClick
                        />
                    </Grid>
                    <Grid>
                        <Button 
                            variant="contained"
                            color="primary" 
                            disabled={this.state.printDisabled}
                            style={buttonStyle} 
                            onClick={()=>this.onPrint()}>
                            Print
                        </Button>
                        <Button 
                            variant="contained" 
                            color="primary" 
                            disabled={this.state.printAllDisabled}
                            style={buttonStyle}
                            onClick={()=>this.onPrintAll()}>
                            Print All
                        </Button>
                    </Grid>
                </Card>
            </Grid>
        )
      }
}