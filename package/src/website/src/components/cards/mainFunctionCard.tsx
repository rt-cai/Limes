import React from 'react';
import "./mainFunctionCard.css"
import { Typography, Card, Paper } from '@material-ui/core';
import { MainFunctionCardProperties } from '../../models/props';

export class MainFunctionCard extends React.Component<MainFunctionCardProperties> {
    private _mainText: string;

    constructor(props: MainFunctionCardProperties) {
        super(props);
        this._mainText = props.text;
    }

    render(): JSX.Element {
        return (
            <Paper className='paper'>
            <Card className='card'>
                <Typography variant="h5" component="h2">
                    {this._mainText}
                </Typography>
            </Card>
            </Paper>

        )
    }
}