import React from 'react';
// import "./mainFunctionCard.css"
import { Typography, Grid, Card } from '@material-ui/core';
import { MainFunctionCardProps, MainFunctionCardSettings } from '../../models/props';

interface MainFunctionCardState {
    disabled: boolean
}

export class MainFunctionCard extends React.Component<MainFunctionCardProps, MainFunctionCardState> {
    private mainText: string;
    private cardStyle: React.CSSProperties;
    private onClick: (settings: MainFunctionCardSettings) => void;
    private settings: MainFunctionCardSettings;

    constructor(props: MainFunctionCardProps) {
        super(props);
        const s = props.settings

        this.settings = props.settings
        this.mainText = s.name
        this.state = {
            disabled: s.disabled
        }
        this.cardStyle = {
            width: '200px',
            height: '200px',
            // border: '1px solid red'
            background: s.disabled? 'lightgrey': '',
            cursor: s.disabled? '': 'pointer',
        }
        this.onClick = props.onClick
    }

    render(): JSX.Element {
        const cardStyle = this.cardStyle;
        const colStyle: React.CSSProperties = {
            // border: '1px solid red'
            height: '100%'
        }

        return (
            <Card style={cardStyle} onClick={this.state.disabled? ()=>{} : () => this.onClick(this.settings)}>
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