import { Theme } from "@material-ui/core";
import { ElabService } from "../services/elab";

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
    elabService: ElabService
}

export interface LoginProps {
    elabService: ElabService 
}