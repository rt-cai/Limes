import React from 'react';
// import './header.css';
import { AppBar, Toolbar, Typography, Box, Button } from '@material-ui/core';
import HomeRoundedIcon from '@mui/icons-material/HomeRounded';
import elabLogo from '../../images/elabLogo.svg'
import { HeaderProps } from '../../models/props'
import Link from '@mui/material/Link';

interface HeaderState {

}

export class HeaderComponent extends React.Component<HeaderProps, HeaderState> {
    render(): JSX.Element {
        const textStyle: React.CSSProperties = {
            padding: '0.2em 0.2em'
        }
        const linkStyle: React.CSSProperties = {
            padding: '0.2em 0.2em',
            color: '#ffffff'
        }
        const titleStyle: React.CSSProperties = {
            paddingLeft: '1em',
            paddingRight: '0.2em'
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
                    <img src={elabLogo} alt='eLab' height='35em' width='35em'/>
                    <div style={textStyle}>
                        <Typography variant="subtitle1">
                            Powered by
                        </Typography>
                    </div>
                    <div style={linkStyle}>
                        <Link href="https://elab.msl.ubc.ca/" target="_blank" rel="noreferrer noopener" color="inherit">
                            eLab ↗
                        </Link>
                    </div>
                    <div style={textStyle}>
                        <Typography variant="subtitle1">
                            |
                        </Typography>
                    </div>
                    <div style={linkStyle}>
                        <Link href="https://limes-inventory.readthedocs.io/en/latest/portal.html" target="_blank" rel="noreferrer noopener" color="inherit">
                            help ↗
                        </Link>
                    </div>
                    <div style={textStyle}>
                        <Typography variant="subtitle1">
                            
                        </Typography>
                    </div>
                </Toolbar>
            </AppBar>
        )
    }
}