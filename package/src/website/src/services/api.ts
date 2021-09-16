import { RequestService, POST } from "./requests"
import { U, P, T } from "../credentials/elab"
import { DEBUG } from "../config"

export abstract class ApiService {
    protected clientID: string
    protected firstname: string
    protected lastname: string
    private readonly requester: RequestService

    constructor() {
        // actually threading through server due to CORS security
        // does not significantly slow requests
        this.requester = new RequestService('api/d1')
        this.clientID = ''
        this.firstname = ''
        this.lastname = ''
    }

    private makeBody(body: any) {
        body.ClientID = this.clientID;
        console.log(this.clientID)
        return body
    }

    public Login(username: string, password: string): Promise<[boolean, string]> {
        const that = this
        return this.requester.POST({
            path: 'login',
            body: {
                Username: username,
                Password: password
            }
        })
        .then(raw => {
            const res = raw.data;
            switch(res.Code) {
                case 200:
                    that.clientID = res.ClientID
                    that.firstname = res.FirstName
                    that.lastname = res.LastName
                    console.log(that)
                    return [true, '']
                case 401:
                    return [false, 'Incorrect username/password']
                default:
                    return Promise.reject('Oops, something crashed...')
            }
        })
    }

    public BarcodeLookup(barcodes: string[]): Promise<any> {
        const b = this.makeBody({
            Barcodes: barcodes
        })
        console.log(b)
        return this.requester.POST({
            path: 'barcodes',
            body: b
        })
            .then(raw => {
                const res = raw.data.Results;
                
                console.log(raw)
        })
    }
}

class Prod_ApiService extends ApiService {

}

class Dev_ApiService extends ApiService {
    constructor() {
        super()
        this.Login(U, P)
    }
}

export class ApiServiceFactory {
    private static I: ApiService

    public static GetApiService() {
        if(!this.I) {
            this.I = DEBUG? new Dev_ApiService(): new Prod_ApiService()
        }

        return this.I
    }
}