import React from "react";
import "./mainFunctionsGrid.css"
import { Grid } from '@material-ui/core';
import { MainFunctionCard } from "../cards/mainFunctionCard";
import { MainFunctionsGridProperties } from "../../models/props";

export class MainFunctionsGridComponent extends React.Component<MainFunctionsGridProperties> {
    private _functions: any[];

    constructor(props: MainFunctionsGridProperties) {
        super(props)
        this._functions = props.functions;
    }
    render(): JSX.Element {
        return (
            <Grid className='grid'>
                <Grid container justifyContent="center" spacing={5} xs={12}>
                    {this._functions.map((fn) => (
                        <Grid key={fn.name} item>
                            <MainFunctionCard text={fn.name} />
                        </Grid>
                    ))}
                </Grid>
            </Grid>
        )
    }
}