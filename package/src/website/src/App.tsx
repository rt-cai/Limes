// import logo from './logo.svg';
import React from 'react';
import './App.css';
import { MuiThemeProvider, createTheme } from '@material-ui/core/styles';
import { HeaderComponent } from './components/headers/header';
import { MainFunctionsGridComponent } from './components/grids/mainFunctionsGrid';

const theme = createTheme({
  palette: {
    primary: {
      main: '#00abab',
      contrastText: 'white'
    },
    secondary: {
      main: '#98ff6d',
    },
    contrastThreshold: 3,
    tonalOffset: 0.2,
  },
});

export class App extends React.Component {
  render(): JSX.Element {
    return (
      <MuiThemeProvider theme={theme}>
        <div className='app-container'>
        <HeaderComponent />
        <MainFunctionsGridComponent functions={[{
          name: 'scan'
        },
        {
          name: 'print'
        }]}/>
        </div>
      </MuiThemeProvider>

    )
  }
}
