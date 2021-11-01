import React from "react";
import BarcodeScannerComponent from "react-qr-barcode-scanner";
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormControl from '@mui/material/FormControl';
import FormLabel from '@mui/material/FormLabel';
import { Typography, Grid, Card, Button, CircularProgress, Fade, Chip, Container } from '@material-ui/core';
import { ScannerProps } from '../../models/props';
import { ApiService } from "../../services/api";

enum Modes {
    ELAB, LINK
}

interface ScannerState {
    currentCode: string
    cardBorderColour: any
    w: number
    h: number
    mode: Modes
    scanInfo: string[]
}

export class ScannerComponent extends React.Component<ScannerProps, ScannerState> {
    private apiService: ApiService
    private lastCode: string | null
    private readonly NO_SCAN: string = "Nothing Scanned"

    constructor(props: ScannerProps) {
        super(props)
        this.apiService = props.elabService
        this.lastCode = null
        this.state = {
            currentCode: '',
            cardBorderColour: 'transparent',
            w: 300,
            h: 300,
            mode: Modes.ELAB,
            scanInfo: [this.NO_SCAN],
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

    private onScan(data: string) {
        if (this.state.currentCode != data) {
            this.lastCode = this.state.currentCode
        }
        return new Promise<void>((resolve, reject) => {
            this.setState({
                currentCode: data,
                cardBorderColour: this.props.theme.palette.primary.main
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
        })
    }

    private updateInfo() {
        if (!this.state.currentCode) return

        this.apiService.BarcodeLookup([this.state.currentCode])
        .then((r) => {
            console.log(r)
        })

        let info: string[];
        switch (+this.state.mode) {
            case Modes.ELAB:
                info = [`Barcode: [${this.state.currentCode}]`]
                break
            case Modes.LINK:
                let last;
                let curr;
                if (this.lastCode) {
                    last = this.lastCode
                    curr = this.state.currentCode
                } else {
                    last = this.state.currentCode
                    curr = 'awaiting scan'
                }
                info = [
                    `Link [${last}]`,
                    `to [${curr}]?`,
                ]
                break
            default:
                info = [this.NO_SCAN]
        }
        this.setState({
            scanInfo: info,
        })
    }

    private onClear() {
        this.lastCode = null
        this.setState({
            scanInfo: [this.NO_SCAN],
            currentCode: '',
        }, () => this.updateInfo())
    }

    private onToClipboard() {
        navigator.clipboard.writeText(this.state.currentCode)
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
            border: '5px solid',
            borderColor: this.state.cardBorderColour,
        }
        const buttonStyle: React.CSSProperties = {
            margin: '0 1em 0 1em',
            width: '6em',
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
                            <FormControl component="fieldset">
                                <Typography variant="h6" component="h6" align="center" gutterBottom={false}>
                                    After Scanning:
                                </Typography>
                                <RadioGroup row value={this.state.mode} onChange={(e) => {
                                    const newMode = (e.target.value as any) as Modes
                                    this.setState({ mode: newMode }, () => this.updateInfo())
                                }}>
                                    <FormControlLabel value={Modes.ELAB} label="Open in eLab"
                                        control={
                                            <Radio sx={{
                                                '&.Mui-checked': {
                                                    color: this.props.theme.palette.primary.main
                                                }
                                            }} />
                                        } />
                                    <FormControlLabel value={Modes.LINK} label="Link Barcodes"
                                        control={
                                            <Radio sx={{
                                                '&.Mui-checked': {
                                                    color: this.props.theme.palette.primary.main
                                                }
                                            }} />
                                        } />
                                </RadioGroup>
                            </FormControl>
                        </Grid>
                        <Grid item>
                            <Container style={{
                                // margin: '0 0.3em 0 0.3em',
                                marginBottom: '1em',
                                border: '1px solid',
                                borderRadius: '0.3em',
                                width: this.state.w,
                                borderColor: this.props.theme.palette.primary.main,
                            }}>
                                {this.state.scanInfo.map((line, i) => {
                                    return <Typography align="left" key={i} style={{
                                        color: 'primary',
                                    }}>
                                        {line}
                                    </Typography>
                                })}
                            </Container>
                        </Grid>
                        <Grid item>
                            <Button
                                variant="contained"
                                color="secondary"
                                style={buttonStyle}
                                onClick={() => this.onClear()}
                            >
                                Clear
                            </Button>
                            <Button
                                variant="contained"
                                color="primary"
                                style={buttonStyle}
                            >
                                Confirm
                            </Button>
                        </Grid>
                        <Grid item>
                        <Button
                                variant="contained"
                                color="primary"
                                style={{marginTop: '1em'}}
                                onClick={() => {this.onToClipboard()}}
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