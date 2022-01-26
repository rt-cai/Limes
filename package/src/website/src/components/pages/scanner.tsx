import React from "react";
import BarcodeScannerComponent from "react-qr-barcode-scanner";
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormControl from '@mui/material/FormControl';
import FormLabel from '@mui/material/FormLabel';
import { Typography, Grid, Card, Button, CircularProgress, Fade, Container } from '@material-ui/core';
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
    actionButtonName: string
    actionDisabled: boolean
    working: boolean
}

export class ScannerComponent extends React.Component<ScannerProps, ScannerState> {
    private apiService: ApiService
    private lastCode: string | null
    private readonly NO_SCAN: string = "Nothing Scanned"
    private barcodes: any;
    private setIDPair: [string, string] | null;

    constructor(props: ScannerProps) {
        super(props)
        this.apiService = props.elabService
        this.lastCode = null
        this.barcodes = {}
        this.setIDPair = null
        this.state = {
            currentCode: '',
            cardBorderColour: 'transparent',
            w: 300,
            h: 300,
            mode: Modes.ELAB,
            scanInfo: [this.NO_SCAN],
            actionButtonName: 'Go',
            actionDisabled: true,
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

    private tryGetBarcode(code: string) {
        const local = this.barcodes[code]
        if (local) {
            return Promise.resolve(local)
        } else {
            return this.apiService.BarcodeLookup([code]).then((results) => {
                const remote = Object.keys(results).filter((c) => c === code)
                const result = remote.length > 0 ? results[remote[0]] : null
                if (result) {
                    this.barcodes[code] = result
                    return result
                }
            })
        }
    }

    private updateInfo() {
        if (!this.state.currentCode) return

        this.tryGetBarcode(this.state.currentCode).then((bar) => {
            if (bar) {
                console.log(bar)
            } else {
                console.log('nada')
            }

            let info: string[];
            const barInfo = this.barcodes[this.state.currentCode]
            this.setIDPair = null;
            let canAct: boolean = false
            let working = this.state.working
            switch (+this.state.mode) {
                case Modes.ELAB:
                    info = [
                        `Barcode: [${this.state.currentCode}]`
                    ]
                    if (barInfo) {
                        info = info.concat([
                            `${barInfo.name}`
                        ])
                        canAct = true;
                        working = false;
                    }
                    break
                case Modes.LINK:
                    info = [
                        `Barcode: [${this.state.currentCode}]`
                    ]
                    canAct = true;
                    break
                    // if (this.lastCode) {
                    //     if(barInfo) { // this is sample that can be linked to
                    //         info = [
                    //             `Link [${this.lastCode}]`,
                    //             `to [${barInfo.name}] ?`,
                    //         ]
                    //         canAct = true;
                    //     } else {
                    //         info = [
                    //             `[${this.state.currentCode}] has no attached sample!`,
                    //             `try again`
                    //         ]
                    //     }
                    //     this.setIDPair = [this.lastCode, this.state.currentCode];
                    //     this.lastCode = null // reset
                    // } else {
                    //     if(barInfo) { // last is already in system, can't use
                    //         info = [
                    //             `Link [awaiting scan]`,
                    //             `to sample barcode`,
                    //             ``,
                    //             `[${this.state.currentCode}] is already attached to`,
                    //             `${barInfo.name}`
                    //         ]
                    //         this.lastCode = null
                    //     } else {
                    //         info = [
                    //             `Link [${this.state.currentCode}]`,
                    //             `to [awaiting scan]`,
                    //         ]
                    //     }
                    // }
                    break
                default:
                    info = [this.NO_SCAN]
            }
            this.setState({
                scanInfo: info,
                actionDisabled: !canAct,
                working: working,
            })
        })
    }

    private onAct() {
        switch (+this.state.mode) {
            case Modes.ELAB:
                window.open(this.barcodes[this.state.currentCode].link, "_blank")
                break
            case Modes.LINK:
                this.setState({working: true})
                this.apiService.AddMmapSample(this.state.currentCode).then((r) => {
                    const info = this.state.scanInfo
                    if (info.length > 1) info.pop()
                    if (r.Code == 200) {
                        info.push('Add success')
                    } else {
                        if(r.Error === "Barcode exists"){
                            info.push('Sample already added')
                        } else if (r.Code == 404) {
                            info.push('Unknown barcode')
                        } else {
                            info.push('Error')
                        }
                    }

                    this.setState({working: false, scanInfo:info})
                })
                // if(this.setIDPair) {
                //     const [alt, sample] = this.setIDPair
                //     this.apiService.LinkBarcode(alt, sample).then((r) => {
                //         if(r.Code == 204) {
                //             alert('success!')
                //         } else {
                //             alert('failed to link')
                //         }
                //         this.updateInfo()
                //     })
                // }
                break
            default:
                break
        }
    }

    private onClear() {
        this.lastCode = null
        this.barcodes = []
        this.setState({
            scanInfo: [this.NO_SCAN],
            currentCode: '',
            actionDisabled: true,
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
                                    const actionName = +newMode === Modes.ELAB.valueOf() ? 'Go' : 'Add';
                                    this.setState({
                                        mode: newMode,
                                        actionButtonName: actionName
                                    }, () => this.updateInfo())
                                }}>
                                    <FormControlLabel value={Modes.ELAB} label="Open in eLab"
                                        control={
                                            <Radio sx={{
                                                '&.Mui-checked': {
                                                    color: this.props.theme.palette.primary.main
                                                }
                                            }} />
                                        } />
                                    <FormControlLabel value={Modes.LINK} label="Receive Sample"
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
                                disabled={this.state.actionDisabled || this.state.working}
                                onClick={()=> this.onAct()}
                            >
                                {this.state.actionButtonName}
                                <Fade in={this.state.working} style={{position: 'absolute'}}>
                                    <CircularProgress size={33}/>
                                </Fade>
                            </Button>
                        </Grid>
                        <Grid item>
                            <Button
                                variant="contained"
                                color="primary"
                                style={{ marginTop: '1em' }}
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