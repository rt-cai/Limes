export interface AppProps {

}

export interface MainFunctionCardProps {
    settings: MainFunctionCardSettings
    onClick: (settings: MainFunctionCardSettings) => void
}

export interface MainFunctionCardSettings {
    name: string
    disabled: boolean
    makeNextPage?: () => any
}

export interface MainFunctionsGridProps {
    functions: MainFunctionCardSettings[]
    clicked: (settings: MainFunctionCardSettings) => void
}

export interface PrintProps {
    
}