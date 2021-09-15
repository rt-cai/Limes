import axios, { AxiosStatic } from "axios";

export const GET = 'GET'
export const POST = 'POST'

export class RequestService {
    private readonly baseUrl: string
    private readonly requester: AxiosStatic

    constructor(baseUrl: string = '') {
        this.baseUrl = baseUrl;
        this.requester = axios

        // const ep = 'call'
        // console.log('start')
        // axios.post(`api/d1/${ep}`, {
        //     ProviderName: 'elab',
        //     RequestPayload: {
        //         TargetEndpoint: 'auth/user',
        //         Method: 'POST',
        //         Body: {
        //             username: username,
        //             password: password
        //         }
        //     }
        // }).then(x => {
        //     console.log(x)
        // }).catch(e => {
        //     console.log('err')
        //     console.log(e)
        // }).finally(() => {
        //     console.log('done')
        // })
    }

    private genUrl(path: string) {
        const url = `${this.baseUrl}/${path}`
        return url.endsWith('/')? url.substring(0, url.length - 1): url;
    }

    // public GET(path: string): Promise<any> {
    //     console.log(this.genUrl(path))
    //     return this.requester.get(this.ge`${this.baseUrl}/${path}`nUrl(path)).then(x => {
    //         console.log(x)
    //         return 'done'
    //     }).catch(e => {
    //         console.log(e)
    //     })
    // }

    public POST({path = '', body = {}}): Promise<any> {
        return this.requester.post(this.genUrl(path), body)
    }
}