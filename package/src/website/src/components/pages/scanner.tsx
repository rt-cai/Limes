import React from "react";
import BarcodeScannerComponent from "react-qr-barcode-scanner";
import { Typography, Grid, Card, Button, CircularProgress, Fade, Chip, Container } from '@material-ui/core';
import { ScannerProps } from '../../models/props';
import { ApiService } from "../../services/api";

interface ScannerState {
    lastBar: String
    cardBorderColour: any
    w: number
    h: number
}

export class ScannerComponent extends React.Component<ScannerProps, ScannerState> {
    private apiService: ApiService

    constructor(props: ScannerProps) {
        super(props)
        this.apiService = props.elabService
        this.state = {
            lastBar: '',
            cardBorderColour: 'transparent',
            w: 300,
            h: 300,
        }
    }

    public componentDidMount() {
        const [w, h] = [window.innerWidth, window.innerHeight]
        const l = w < h? w: h
        if (l < this.state.w) {
            this.setState({
                w: w-20,
                h: w-20,
            })
        }
    }

    private onScan(data: String) {
        this.setState({
            lastBar: data,
            cardBorderColour: this.props.theme.palette.primary.main
        });

        setTimeout(() => {
            this.setState({
                cardBorderColour: 'transparent'
            })
        }, 500);
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
            // width: '500px',
            padding: '2em 0 2em 0',
            border: '3px solid',
            borderColor: this.state.cardBorderColour,
        }
        const buttonStyle: React.CSSProperties = {
            margin: '0 1em 0 1em'
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
                                        if (result) this.onScan(result.getText())
                                    }}
                                />
                            </Container>

                        </Grid>
                        <Grid item>
                            <Typography variant="h5" component="h2" align="center" gutterBottom={false} style={{
                                marginBottom: '1em'
                            }}>
                                {this.state.lastBar}
                            </Typography>
                        </Grid>
                        <Grid item>
                            <Button
                                variant="contained"
                                color="primary"
                                // onClick={() => {this.props.onPrintCallback(this.state.selectedSamples.map((s)=>s.id))}}
                                style={buttonStyle}
                            >
                                Open in Elab
                            </Button>
                            <Button
                                variant="contained"
                                color="primary"
                                // disabled={this.state.reloadingStorage}
                                // onClick={this.onReloadStorages.bind(this)}
                                style={buttonStyle}
                            >
                                Add Mining Sample
                                {/* <Fade in={this.state.reloadingStorage} style={{position: 'absolute'}}>
                                    <CircularProgress size={33} color='secondary'/>
                                </Fade> */}
                            </Button>
                        </Grid>
                    </Grid>
                </Card>
            </Grid>
        )
    }
}