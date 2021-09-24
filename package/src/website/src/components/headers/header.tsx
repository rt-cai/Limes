import React from 'react';
// import './header.css';
import { AppBar, Toolbar, Typography, Box, Button } from '@material-ui/core';
import HomeRoundedIcon from '@mui/icons-material/HomeRounded';
import elabLogo from '../../images/elabLogo.svg'
import { HeaderProps } from '../../models/props'

interface HeaderState {

}

export class HeaderComponent extends React.Component<HeaderProps, HeaderState> {
    render(): JSX.Element {
        const textStyle: React.CSSProperties = {
            padding: '2vh 0.5vw'
        }
        const titleStyle: React.CSSProperties = {
            paddingLeft: '10vw',
            paddingRight: '0.2vw'
        }
        return (
            <AppBar position="static">
                <Toolbar>
                    <div>
                        <Button
                            variant="contained"
                            color="primary"
                            disableElevation
                            onClick={(e) => {this.props.onHome()}}
                            style={{
                                height: '3.5em',
                                width: '3.5em',
                                padding: '0'
                            }}
                        >
                            <HomeRoundedIcon/>
                        </Button>
                    </div>
                    <div style={textStyle}>
                        <Typography variant='h4' style={titleStyle}>
                            <Box fontWeight='fontWeightBold'>
                                Limes Portal
                            </Box>
                        </Typography>
                    </div>
                    <img src={elabLogo} alt='eLab' height='40vw' width='40vw'/>
                    <div style={textStyle}>
                        <Typography variant="subtitle1">
                            Powered by eLab
                        </Typography>
                    </div>
                </Toolbar>
            </AppBar>
        )
    }
}