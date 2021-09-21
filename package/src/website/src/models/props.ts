import { Theme } from "@material-ui/core";
import { ApiService } from "../services/api";

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

export interface PrintProps {
    elabService: ApiService
}

export interface LoginProps {
    elabService: ApiService 
}