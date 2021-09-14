import React from 'react';
import { LoginProps } from '../models/props';
import { Dialog, Grid, TextField, Button } from '@material-ui/core';

interface LoginState {
    username: string
    password: string
    loginRef?: any
    open: boolean
}

export class LoginModal extends React.Component<LoginProps, LoginState> {
    private readonly UID = "username"
    private readonly PID = "password"

    constructor(props: LoginProps) {
        super(props)

        this.state = {
            username: "",
            password: "",
            open: true,
        }
    }

    private textChanged(id: string, e: any) {
        let newState: any = {};
        newState[id] = e.target.value;
        this.setState(newState);
    }

    private watchEnter(id: string, e: any) {
        if (e.key==="Enter" && id===this.PID) {
            this.state.loginRef?.focus()
            // this.login();
        }
    }

    private login() {
        this.setState({open: false})
    }

    private onClose() {

    }
    
    render(): JSX.Element {
        const dialogStyle: React.CSSProperties = {
            // width: '50vw',  
            // height: '50vh'
        }
        const gridStyle: React.CSSProperties = {
            // border: '1px solid red',
            padding: '1vw',
            // width: '50vw',
        }
        const inputStyle: React.CSSProperties = {
            width: '25vw',
            minWidth: '350px',
            marginTop: '1vh'
        }
        const buttonStyle: React.CSSProperties = {
            marginTop: '2vh',
            width: '10vw'
        }

        const textFields = [
            {
                id: this.UID,
                label: "Username",
                placeholder: "username",
            },
            {
                id: this.PID,
                label: "Password",
                placeholder: "*****" ,
                type: "password"
            }
        ]

        return (
            <Dialog open={this.state.open} onClose={this.onClose} style={dialogStyle}>
                <Grid container justifyContent="center" style={gridStyle}>
                    <form>
                        {textFields.map((f) => (
                            <Grid key={f.id} item>
                                <TextField
                                    id={f.id}
                                    label={f.label}
                                    placeholder={f.placeholder}
                                    style={inputStyle}
                                    type={f.type}
                                    onChange={(e) => { this.textChanged(f.id, e) }}
                                    onKeyDown={(e) => { this.watchEnter(f.id, e) }}
                                />
                            </Grid>
                        ))}
                    </form>
                    <Grid container justifyContent="center" >
                        <Button
                            variant="contained"
                            color="primary"
                            style={buttonStyle}
                            onClick={()=>{this.login()}}
                            ref={(e)=>{!this.state.loginRef && this.setState({loginRef: e})}}>
                            Login
                        </Button>
                    </Grid>
                </Grid>
            </Dialog>
        )
    }
}