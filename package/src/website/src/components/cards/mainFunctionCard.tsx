import React from 'react';
// import "./mainFunctionCard.css"
import { Typography, Grid, Card } from '@material-ui/core';
import { MainFunctionCardProps, MainFunctionCardSettings } from '../../models/props';

interface MainFunctionCardState {
    disabled: boolean
    cardStyle: React.CSSProperties
}

export class MainFunctionCard extends React.Component<MainFunctionCardProps, MainFunctionCardState> {
    private mainText: string;
    private onClick: (settings: MainFunctionCardSettings) => void;
    private settings: MainFunctionCardSettings;

    constructor(props: MainFunctionCardProps) {
        super(props);
        const s = props.settings

        this.settings = props.settings
        this.mainText = s.name
        this.state = {
            disabled: s.disabled,
            cardStyle: {
                width: '200px',
                height: '200px',
                border: '2px solid transparent',
                background: s.disabled? 'lightgrey': '',
                cursor: s.disabled? '': 'pointer',
            }
        }
        this.onClick = props.onClick
    }

    private onHover() {
        if (this.state.disabled) return
        const newStyle: any = {}
        Object.assign(newStyle, this.state.cardStyle)
        newStyle.border = `2px solid ${this.props.theme.palette.primary.main}`
        this.setState({cardStyle: newStyle})
    }

    private onLeave() {
        if (this.state.disabled) return
        const newStyle: any = {}
        Object.assign(newStyle, this.state.cardStyle)
        newStyle.border = '2px solid transparent'
        this.setState({cardStyle: newStyle})
    }

    render(): JSX.Element {
        const colStyle: React.CSSProperties = {
            // border: '1px solid red'
            height: '100%'
        }

        return (
            <Card
                style={this.state.cardStyle}
                onClick={this.state.disabled? ()=>{} : () => this.onClick(this.settings)}
                onMouseEnter={()=>{this.onHover()}}
                onMouseLeave={()=>{this.onLeave()}}>
                <Grid
                    container
                    spacing={0}
                    justifyContent='center'
                    alignItems='center'
                    direction='column'
                    style={colStyle}
                >
                    <Grid item>
                        <Typography variant="h5" component="h2">
                            {this.mainText}
                        </Typography>
                    </Grid>
                </Grid>
            </Card>
        )
    }
}