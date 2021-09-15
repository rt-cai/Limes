import { RequestService, POST } from "./requests"
import { T } from "../credentials/elab"
import { DEBUG } from "../config"

interface CallProviderRequest {
    ProviderName: string
    RequestPayload: {
        TargetEndpoint: string,
        Method: string,
        Body: any
    }
}

export abstract class ElabService {
    protected token: string
    private readonly requester: RequestService

    constructor() {
        // actually threading through server due to CORS security
        // does not significantly slow requests
        this.requester = new RequestService('api/d1/call')
        this.token = ''
    }

    private genRequest(TargetEndpoint: string, Method: string, Body: any = {}): CallProviderRequest {
        return {
            ProviderName: 'elab',
            RequestPayload: {
                TargetEndpoint: TargetEndpoint,
                Method: Method,
                Body: Body
            }
        }
    }

    public Login(username: string, password: string): Promise<[boolean, string]> {
        return this.requester.POST({body: this.genRequest(
            'auth/user', POST, {
                username: username,
                password: password
            })})
        .then(raw => {
            const res = raw.data.ResponsePayload;
            // console.log(res)
            switch(res.Code) {
                case 200:
                    this.token = res.Body.token
                    return [true, this.token]
                case 401:
                    return [false, 'Incorrect username/password']
                default:
                    return Promise.reject(res.Body.message)
            }
        })
    }
}

class Prod_ElabService extends ElabService {

}

class Dev_ElabService extends ElabService {
    constructor() {
        super()
        this.token = T
    }
}

export const ConcreteElabService = DEBUG? Dev_ElabService: Prod_ElabService;