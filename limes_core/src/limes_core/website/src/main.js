// ================ ui ================
const BUTTONS = document.getElementById("side-block").children
const btnMS = BUTTONS[3]
const btnCL = BUTTONS[4]

let log
function updateLog(i, msg) {
    if (msg) log[i] = msg;

    let full = '';
    for (let s of log) {
        if (!s) continue;
        full += s + '\n';
    }
    document.getElementById('lblLog').innerText = full;
}

class CodeProcessor {
    constructor(btn) {
        for (let b of BUTTONS) {
            b.style.borderColor = "transparent";
        }
        btn.style.borderColor = "white";
        updateLog(0, 'nothing scanned');
        this.done = false;
    }

    lookupBarcode(code) {
        if(this.done) {
            blinkBorder('yellow');
            updateLog(0, 'reset to start new task');
            return;
        }

        updateLog(0, `scanned ${code}`);

        askELab('get', `barcode/${code}`).then((res) => {
            console.log(res)
            updateLog(0, `scanned '${code}' is ${res.type} `);
            let fn = processor[res.type];
            // console.log(">"+ res.type + "<")
            if (fn) {
                processor[res.type](res.id);
            } else {
                updateLog(0, `unrecognized '${code}' is '${res.type}'`);
                blinkBorder('red')
            }

        }).catch((err) => {
            updateLog(0, `bad scan '${code}', elab: ${err}`);
            blinkBorder('red');
        })
    }

    STORAGELAYER(id) {
        askELab('get', `storageLayers/${id}/freeLocation`).then((res) => {
            this.storageID = res.storageLayerID;
            this.position = res.position;
            this.sample = res;

            updateLog(2, `storing in ${res.name}, position ${res.positionName}`);
            blinkBorder('green');
        }).catch((err) => {
            updateLog(0, `bad location, elab: ${err}`);
            blinkBorder('red');
        })
    }
}

class MSProcessor extends CodeProcessor {
    constructor() {
        super(btnMS)

        log[1] = 'please scan a sample';
        log[2] = 'please scan a location';
        updateLog();
    }

    SAMPLE(id) {
        askELab('get', `samples/${id}`).then((res) => {
            this.sampleID = id;
            this.sampleName = res.name;
            updateLog(1, `selected ${res.name}`);
            // updateLog(3, res.description)
            blinkBorder('green')
        }).catch((err) => {
            updateLog(0, `bad sample, elab: ${err}`);
            blinkBorder('red');
        })
    }

    confirm() {
        if(this.done){
            return;
        }

        let go = true;
        if (!this.storageID || !this.position) {
            go = false
            updateLog(2, `please scan a location`);
        }
        if (!this.sampleID) {
            go = false
            updateLog(1, `please scan a sample`);
        }
        if (!go) return;

        setLogBorder('cyan');
        askELab('post', `samples/${this.sampleID}/moveToLayer/${this.storageID}`, {
            position: this.position
        }).then(() => {
            this.done = true;
            blinkBorder('green');
            updateLog(3, `\n** successfully moved '${this.sampleName}' **`);
            lastcode = 0;
        }).catch((err) => {
            updateLog(9, `failed to move sample, elab: ${err}\nplease try again`)
            blinkBorder('red');
        })
    }
}

class CLProcessor extends CodeProcessor {
    constructor() {
        super(btnCL)
        this.samples = []
        this.maxParents = 0;

        log[1] = 'please scan parents';
        log[2] = 'please scan a location';
        log[3] = 'please scan a sample template';
        updateLog();
    }

    updateParents() {
        let l = this.samples.length;
        let max = this.maxParents;
        if (this.maxParents && l > max) {
            this.samples = this.samples.splice(l - max)
        }

        let logSamples = ''
        for (let s of this.samples) {
            logSamples += `added parent: ${s.name}\n`
        }
        updateLog(1, logSamples);
    }

    SAMPLE(id) {
        askELab('get', `samples/${id}`).then((res) => {
            this.samples.push(res);
            console.log(res);

            this.updateParents();
            blinkBorder('green')
        }).catch((err) => {
            updateLog(0, `bad sample, elab: ${err}`);
            blinkBorder('red');
        })
    }

    SAMPLETYPE(id) {
        askELab('get', `sampleTypes/${id}`).then((res) => {
            // console.log(JSON.stringify(res));
            updateLog(3, `selected template: ${res.name}`);
            this.type = res;
            return askELab('get', `sampleTypes/${id}/meta`)
        }).then((res) => {
            // console.log(JSON.stringify(res))
            let parents = 0;
            for (let field of res.data) {
                if (field.sampleDataType == 'SAMPLELINK') {
                    parents++;
                }
                else if (field.key == "Parents") {
                    this.metaID = field.sampleTypeMetaID;
                }
            }
            this.maxParents = parents;
            this.updateParents();

            let pre = log[3];
            let s = parents > 1 ? 's' : '';
            updateLog(3, pre + `\ntemplate for ${parents} parent${s}`)
            blinkBorder('green')
        }).catch((err) => {
            updateLog(0, `bad sample, elab: ${err}`);
            blinkBorder('red');
        })
    }

    confirm() {
        if(this.done){
            return;
        }

        let go = true;
        if (!this.storageID || !this.position) {
            go = false
            updateLog(2, `please scan a location`);
        }
        if (this.samples.length == 0) {
            go = false
            updateLog(1, `please scan atleast 1 parent`);
        }
        if (!this.type) {
            go = false
            updateLog(1, `please scan a sample type`);
        }
        if (!go) return;

        let t = this.type
        console.log(t);
        let sample = {
            sampleTypeID: t.sampleTypeID,
            name: `New ${t.name}`,
            storageLayerID: this.storageID,
            position: this.position
        }

        let rawSampleID;

        setLogBorder('cyan');
        askELab('post', `samples`, sample).then((res) => {
            console.log(res);
            let val = ''
            for(let p of this.samples){
                val += `(${p.name}: ${p.barcode}), `;
            }
            val = val.substring(0, val.length - 2)
            let meta = {
                    sampleDataType: "TEXT",
                    value: 'These will be actual links: ' + val,
                    key: "Parents",
                    sampleTypeMetaID: this.metaID,
            }
            rawSampleID = res;
            return askELab('put', `samples/${res}/meta`, meta)
        }).then((res)=>{
            // console.log(res);
            this.done = true;
            blinkBorder('green');
            updateLog(4, `\n** successfully created 'New ${this.type.name}' **`);
            lastcode = 0;
        }).catch((err) => {
            updateLog(9, `failed to create sample, elab: ${err}\nplease try again`)
            blinkBorder('red');

            if(rawSampleID)
            {
             return askELab('delete', `samples/${rawSampleID}`)   
            }
        }).catch((err) => {
            console.log(err)
            console.log('cleanup on fail has itself failed')
        })
    }
}

let processor;
let remakeProcessor = () => { processor = new MSProcessor(); };
let lastcode = 0;

function reset() {
    lastcode = 0;
    log = Array(10);
    // this will upate the log
    remakeProcessor();
}
reset(); // init on start

//sleep
BUTTONS[0].addEventListener("click", () => {
    window.location.href = '/sleep'
});
//reset
BUTTONS[1].addEventListener("click", () => {
    reset();
});
//confirm
BUTTONS[2].addEventListener("click", () => {
    processor.confirm();
});

BUTTONS[3].addEventListener("click", () => {
    remakeProcessor = () => { processor = new MSProcessor(); };
    reset();
});
BUTTONS[4].addEventListener("click", () => {
    remakeProcessor = () => { processor = new CLProcessor(); };
    reset();
});

// ================ elab ================

function askELab(method, endpoint, data = {}) {

    let body = {
        method: method,
        url: endpoint,
        data: data
    }

    let oReq = new XMLHttpRequest();
    oReq.open("POST", "/-cors");
    oReq.setRequestHeader("Content-Type", "application/json");

    return new Promise((resolve, reject) => {
        oReq.addEventListener("load", () => {
            // console.log(this);
            // console.log(oReq.responseText);
            try {
                let res = JSON.parse(oReq.responseText)
                if (typeof res == "string" && res != '') {
                    let start = res.indexOf('<h1>') + 4
                    let end = res.indexOf('</h1>')
                    reject(`'${res.substring(start, end)}'`);
                } else {
                    resolve(res);
                }
            } catch {
                reject(`elab error`)
            }
        });

        let failed = () => { reject('elab failed to respond') };

        oReq.addEventListener("load", failed);
        oReq.addEventListener("error", failed);
        oReq.addEventListener("abort", failed);

        oReq.send(JSON.stringify(body));
    });
}

function ping() {
    askELab('get', 'auth/user')
}

// ================ scanner ================

const wqrcode = window.qrcode;

const video = document.createElement("video");
const canvasElement = document.getElementById("qr-canvas");
const canvas = canvasElement.getContext("2d");

window.addEventListener('load', (event) => {
    // qr code and video
    navigator.mediaDevices.getUserMedia({
        video: { facingMode: "environment" }
    }).then((stream) => {
        video.setAttribute("playsinline", true); // required to tell iOS safari we don't want fullscreen
        video.srcObject = stream;

        video.play();
        console.log("qr started")

    }).then(() => {
        //barcode
        Quagga.init({
            inputStream: {
                name: "Live",
                type: "LiveStream",
                target: canvasElement // using stream here doesn't work
            },
            decoder: {
                readers: ["code_128_reader"]    // this is just guess
            }
        }, function (err) {
            if (err) {
                console.log(err);
                return
            }

            Quagga.start();
            console.log("bar started");

            //start display
            scanning = true;
            tick();
            scan();
        });
    })
});

wqrcode.callback = (res) => {
    if (res) {
        detected(res);
    }
};

Quagga.onDetected((res) => {
    if (res.codeResult.code) {
        let code = res.codeResult.code
        detected(code);
    }
})

function getSquare(w, h, method) {
    let l;
    if (method == "inner")
        l = w < h ? w : h;
    else
        l = w > h ? w : h;

    let xoff, yoff;

    xoff = -(l - w) / 2
    yoff = -(l - h) / 2
    return {
        l: l,
        left: xoff,
        top: yoff
    }
}

function tick() {
    if (!scanning) return;

    let vw = video.videoWidth;
    let vh = video.videoHeight;
    let v = getSquare(vw, vh, "inner")

    let cw = window.innerWidth;
    let ch = window.innerHeight;
    let c = getSquare(cw, ch, "outer")
    canvasElement.width = cw;
    canvasElement.height = ch;

    canvas.drawImage(video, v.left, v.top, v.l, v.l,
        c.left, c.top, c.l, c.l);

    requestAnimationFrame(tick);
}

function scan() {
    try {
        wqrcode.decode();
    } catch (e) {
        setTimeout(scan, 300);
    }
}

function detected(code) {
    // console.log(code);
    if (lastcode == code) {
        setLogBorder('yellow')
        setTimeout(() => {
            tick();
            scan();
        }, 300);

        setTimeout(() => { setLogBorder('black') }, 500)
        return
    }

    processor.lookupBarcode(code);
    lastcode = code;

    scanning = false;
    setLogBorder('yellow')
    setTimeout(() => {
        scanning = true;
        tick();
        scan();
    }, 1500);
}

function setLogBorder(col) {
    document.getElementById('log').style.borderColor = col
}

function blinkBorder(col) {
    setLogBorder(col)
    setTimeout(() => {
        setLogBorder('black')
    }, 1500);
}