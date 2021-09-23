import { Theme } from "@material-ui/core";
import { ApiService } from "../services/api";
import { Sample } from "./common";

export interface AppProps {}

export interface MainFunctionCardProps {
    theme: Theme
    settings: MainFunctionCardSettings
    onClick: (settings: MainFunctionCardSettings) => void
}

export interface MainFunctionCardSettings {
    name: string
    disabled: boolean
    makeNextPage?: () => any
}

export interface MainFunctionsGridProps {
    theme: Theme
    functions: MainFunctionCardSettings[]
    clicked: (settings: MainFunctionCardSettings) => void
}

interface WithElabServiceProp {
    elabService: ApiService
    startingSamples?: Sample[]
}

export interface PrintProps extends WithElabServiceProp { }

export interface LoginProps extends WithElabServiceProp { }

export interface StorageSearchProps extends WithElabServiceProp {
    onPrintCallback: (samples: Sample[]) => void
}