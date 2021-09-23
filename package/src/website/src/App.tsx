// import logo from './logo.svg';
import React from 'react';
import './App.css';
import { MuiThemeProvider, createTheme } from '@material-ui/core/styles';
import { HeaderComponent } from './components/headers/header';
import { ConcreteLoginModal } from './popups/login';
import { MainFunctionsComponent } from './components/pages/mainFunctions';
import { PrintComponent } from './components/pages/print';
import { StorageSearchComponent } from './components/pages/storageSearch';

import { AppProps, MainFunctionCardSettings } from './models/props';
import { ApiService, ApiServiceFactory } from './services/api';
import { DEBUG } from './config'

const theme = createTheme({
  palette: {
    primary: {
      main: '#00abab',
      contrastText: '#FFFFFF',
    },
    secondary: {
      main: '#d32f2f',
    },
    contrastThreshold: 3,
    tonalOffset: 0.2,
  },
});

interface AppState {
  activeComponent: any
}

export class App extends React.Component<AppProps, AppState> {
  private defaultActiveComponent: any
  private elabService: ApiService

  constructor(props: AppProps) {
    super(props)
    this.elabService = ApiServiceFactory.GetApiService()

    const makePrintComponent = () => <PrintComponent elabService={this.elabService}/>
    const makeStorageSearchComponent = () => <StorageSearchComponent elabService={this.elabService} onPrintCallback={
      (samples) => {
        this.setState({
          activeComponent: <PrintComponent elabService={this.elabService} startingSamples={samples}/>
        })
      }
    }/>
    const mainFunctions: MainFunctionCardSettings[] = [
      {
        name: 'Print',
        disabled: false,
        makeNextPage: makePrintComponent
      },
      {
        name: 'Search Storage Locations',
        disabled: false,
        makeNextPage: makeStorageSearchComponent
      },
      {
        name: 'Scanner coming soon!',
        disabled: true,
      }
    ]
    this.defaultActiveComponent = (
      <MainFunctionsComponent
        theme={theme}
        functions={mainFunctions}
        clicked={(settings: MainFunctionCardSettings) => this.toFunctionPage(settings)}
      />)
    this.state = {
      activeComponent: DEBUG? <PrintComponent elabService={this.elabService} startingSamples={[
        9763616,
        9763617,
        9763618,
        9763619,
        9763620,
      ].map(i=>{return {id: i, name:'s', type: 't'}})}/>: this.defaultActiveComponent,
    }
  }

  private toFunctionPage(settings: MainFunctionCardSettings) {
    if (settings && settings.makeNextPage) {
      this.setState({activeComponent: settings.makeNextPage()})
    }
  }

  render(): JSX.Element {
    const fav: any = document.getElementById("favicon");
    fav.href = '/forcefavicon'
    return (
      <MuiThemeProvider theme={theme}>
        <div className='app-container'>
        <HeaderComponent />
        <ConcreteLoginModal elabService={this.elabService}/>
        {this.state.activeComponent}
        </div>
      </MuiThemeProvider>
    )
  }
}