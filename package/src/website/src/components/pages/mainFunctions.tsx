import React from "react";
// import "./mainFunctionsGrid.css"
import { Grid } from "@material-ui/core";
import { MainFunctionCard } from "../cards/mainFunctionCard";
import { MainFunctionsGridProps, MainFunctionCardSettings } from "../../models/props";

interface MainFunctionsState {
    functions: MainFunctionCardSettings[]
}

export class MainFunctionsComponent extends React.Component<MainFunctionsGridProps, MainFunctionsState> {
    private cardClicked: (settings: MainFunctionCardSettings)=>void

    constructor(props: MainFunctionsGridProps) {
        super(props)
        this.state = {
            functions: props.functions,
        }
        this.cardClicked = props.clicked
    }
    render(): JSX.Element {
        return (
            <Grid
                style={{
                    marginTop: '10vh',
                    // border: '1px solid red'
                }}
            >
                <Grid container justifyContent='center' spacing={5}>
                    {this.state.functions.map((fn) => (
                        <Grid key={fn.name} item>
                            <MainFunctionCard
                                theme={this.props.theme}
                                settings={fn}
                                onClick={this.cardClicked}
                            />
                        </Grid>
                    ))}
                </Grid>
            </Grid>
        )
    }
}