import React from 'react';
import './header.css';
import { AppBar, Toolbar, Typography, Box } from '@material-ui/core';
import elabLogo from '../../images/elabLogo.svg'

export class HeaderComponent extends React.Component {
    render(): JSX.Element {
        return (
            <AppBar position="static">
                <Toolbar>
                    <div className='text'>
                        <Typography variant='h4' className='title'>
                            <Box fontWeight='fontWeightBold'>
                                Limes Portal
                            </Box>
                        </Typography>
                    </div>
                    <img src={elabLogo} alt='eLab' height='40vw' width='40vw'/>
                    <div className='text'>
                        <Typography variant="subtitle1" className='desc'>
                            Powered by eLab
                        </Typography>
                    </div>
                </Toolbar>
            </AppBar>
        )
    }
}