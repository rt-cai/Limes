(this.webpackJsonpwebsite=this.webpackJsonpwebsite||[]).push([[0],{280:function(e,t,n){},389:function(e,t,n){},392:function(e,t,n){"use strict";n.r(t);var a,i=n(0),r=n.n(i),o=n(22),s=n.n(o),c=n(19),l=n(18),d=n(28),u=n(27),h=(n(280),n(83)),b=n(460),m=n(448),p=n(451),f=n(92),v=n(396),j=n(464),g=n(242),y=n.n(g),O=n.p+"static/media/elabLogo.6161d4d0.svg",S=n(2),x=function(e){Object(d.a)(n,e);var t=Object(u.a)(n);function n(){return Object(c.a)(this,n),t.apply(this,arguments)}return Object(l.a)(n,[{key:"render",value:function(){var e=this,t={padding:"1em 0.2em"};return Object(S.jsx)(m.a,{position:"static",children:Object(S.jsxs)(p.a,{children:[Object(S.jsx)("div",{children:Object(S.jsx)(f.a,{variant:"contained",color:"primary",disableElevation:!0,onClick:function(t){e.props.onHome()},style:{height:"3.5em",width:"3.5em",padding:"0"},children:Object(S.jsx)(y.a,{})})}),Object(S.jsx)("div",{style:t,children:Object(S.jsx)(v.a,{variant:"h4",style:{paddingLeft:"1em",paddingRight:"0.2em"},children:Object(S.jsx)(j.a,{fontWeight:"fontWeightBold",children:"Limes Portal"})})}),Object(S.jsx)("img",{src:O,alt:"eLab",height:"35em",width:"35em"}),Object(S.jsx)("div",{style:t,children:Object(S.jsx)(v.a,{variant:"subtitle1",children:"Powered by eLab"})})]})})}}]),n}(r.a.Component),C=n(6),k=n(469),w=n(455),L=n(456),T=n(181),P=n(459),B=n(399),I=function(e){Object(d.a)(n,e);var t=Object(u.a)(n);function n(e){var a;return Object(c.a)(this,n),(a=t.call(this,e)).passwordRef=void 0,a.loginRef=void 0,a.defaultLabel="",a.elabService=void 0,a.state={username:"",password:"",open:!0,error:!1,label:a.defaultLabel,loading:!1,tried:!1},a.elabService=e.elabService,a}return Object(l.a)(n,[{key:"loginFailed",value:function(e){var t=!(arguments.length>1&&void 0!==arguments[1])||arguments[1];this.setState({error:!0,label:e,loading:!1,tried:t})}},{key:"loginSuccess",value:function(){this.setState({open:!1,loading:!1,tried:!1})}},{key:"login",value:function(){var e=this;this.state.tried||(this.setState({label:"",loading:!0}),this.state.username&&this.state.password?this.elabService.Login(this.state.username,this.state.password).then((function(t){var n=Object(C.a)(t,2),a=n[0],i=n[1];a?e.loginSuccess():e.loginFailed(i)})).catch((function(t){console.error(t),e.loginFailed("string"===typeof t?t:"No response. Are you on the UBC network?",!1)})):this.loginFailed("fields cannot be empty"))}},{key:"onClose",value:function(){}},{key:"render",value:function(){var e=this,t={},n={width:"100%",marginBottom:"1em"},a=[{name:"username",label:"Username",placeholder:"username",onchange:function(t){e.setState({error:!1,tried:!1,username:t.target.value})}},{name:"password",label:"Password",placeholder:"*****",type:"password",onchange:function(t){e.setState({error:!1,tried:!1,password:t.target.value})},onkeydown:function(t){var n;"Enter"===t.key&&(null===(n=e.loginRef)||void 0===n||n.focus())}}];return Object(S.jsx)(k.a,{open:this.state.open,onClose:this.onClose,style:{},children:Object(S.jsx)(w.a,{container:!0,spacing:0,direction:"column",alignItems:"center",justify:"center",style:{outline:"transparent",height:"100%"},children:Object(S.jsx)(L.a,{style:{outline:"transparent",padding:"1em 2em 1.2em 2em",width:"25em"},children:Object(S.jsxs)(w.a,{container:!0,justify:"center",direction:"column",style:{},spacing:0,children:[Object(S.jsx)(v.a,{variant:"h5",component:"h2",align:"center",style:t,children:"Login"}),Object(S.jsx)(v.a,{variant:"subtitle1",align:"center",color:"error",style:t,children:this.state.label}),Object(S.jsx)(w.a,{item:!0,container:!0,justifyContent:"center",direction:"column",children:Object(S.jsx)("form",{children:a.map((function(t){return Object(S.jsx)(w.a,{item:!0,children:Object(S.jsx)(T.a,{label:t.label,name:t.name,placeholder:t.placeholder,style:n,type:t.type,error:e.state.error,onChange:t.onchange,onKeyDown:t.onkeydown})},t.name)}))})}),Object(S.jsx)(w.a,{container:!0,justify:"center",children:Object(S.jsxs)(f.a,{variant:"contained",color:"primary",style:{width:"10em"},disabled:this.state.loading,onClick:function(){e.login()},ref:function(t){e.loginRef=t},children:["Login",Object(S.jsx)(P.a,{in:this.state.loading,children:Object(S.jsx)(B.a,{size:20,thickness:5,style:{position:"absolute"}})})]})})]})})})})}}]),n}(r.a.Component),D=function(e){Object(d.a)(n,e);var t=Object(u.a)(n);function n(){return Object(c.a)(this,n),t.apply(this,arguments)}return n}(I),N=D,A=function(e){Object(d.a)(n,e);var t=Object(u.a)(n);function n(e){var a;Object(c.a)(this,n),(a=t.call(this,e)).mainText=void 0,a.onClick=void 0,a.settings=void 0;var i=e.settings;return a.settings=e.settings,a.mainText=i.name,a.state={disabled:i.disabled,cardStyle:{width:"200px",height:"200px",border:"2px solid transparent",background:i.disabled?"lightgrey":"",cursor:i.disabled?"":"pointer"}},a.onClick=e.onClick,a}return Object(l.a)(n,[{key:"onHover",value:function(){if(!this.state.disabled){var e={};Object.assign(e,this.state.cardStyle),e.border="2px solid ".concat(this.props.theme.palette.primary.main),this.setState({cardStyle:e})}}},{key:"onLeave",value:function(){if(!this.state.disabled){var e={};Object.assign(e,this.state.cardStyle),e.border="2px solid transparent",this.setState({cardStyle:e})}}},{key:"render",value:function(){var e=this;return Object(S.jsx)(L.a,{style:this.state.cardStyle,onClick:this.state.disabled?function(){}:function(){return e.onClick(e.settings)},onMouseEnter:function(){e.onHover()},onMouseLeave:function(){e.onLeave()},children:Object(S.jsx)(w.a,{container:!0,spacing:0,justifyContent:"center",alignItems:"center",direction:"column",style:{height:"100%"},children:Object(S.jsx)(w.a,{item:!0,children:Object(S.jsx)(v.a,{variant:"h5",component:"h2",children:this.mainText})})})})}}]),n}(r.a.Component),R=function(e){Object(d.a)(n,e);var t=Object(u.a)(n);function n(e){var a;return Object(c.a)(this,n),(a=t.call(this,e)).cardClicked=void 0,a.state={functions:e.functions},a.cardClicked=e.clicked,a}return Object(l.a)(n,[{key:"render",value:function(){var e=this;return Object(S.jsx)(w.a,{style:{marginTop:"10vh"},children:Object(S.jsx)(w.a,{container:!0,justifyContent:"center",spacing:5,children:this.state.functions.map((function(t){return Object(S.jsx)(w.a,{item:!0,children:Object(S.jsx)(A,{theme:e.props.theme,settings:t,onClick:e.cardClicked})},t.name)}))})})}}]),n}(r.a.Component),E=n(461),M=n(64),_=n(139),U=n(245),F=n.n(U);!function(e){e.SAMPLE="Sample",e.STORAGE_LOCATION="Location",e.CUSTOM="Unknown"}(a||(a={}));var q=function(e){Object(d.a)(n,e);var t=Object(u.a)(n);function n(e){var a;return Object(c.a)(this,n),(a=t.call(this,e)).apiService=void 0,a.UPDATE_DELAY=650,a.lastChange=void 0,a.NO_ELAB_RECORD="*(No eLab Record)",a.apiService=e.elabService,a.lastChange=Date.now(),a.state={labels:[],labelsRaw:"",printDisabled:!0,printAllDisabled:!1,printing:!1,gettingData:!1,labelTemplateName:"",printerName:"",availablePrinters:[],availableTemplates:[],refreshing:!1,copied:0},a}return Object(l.a)(n,[{key:"toBarcodes",value:function(e){return e?e.map((function(e){for(var t=e.barcode,n="".concat(t);n.length<15-"005".length;)n="0".concat(n);return"".concat("005").concat(n)})):[]}},{key:"componentDidMount",value:function(){this.props.startingBarcodes&&this.parseLabels(this.props.startingBarcodes.map((function(e){return"".concat(e)}))),this.onRefresh()}},{key:"parseLabels",value:function(){var e=this,t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:[];0===t.length&&(t=this.state.labelsRaw.split("\n"));var n=(t=t.filter((function(e){return e.trim().length>0}))).map((function(e){return e.includes("\t")?e.split("\t"):e.split(",").map((function(e){return e.trim()}))})),i=n.map((function(e){return e[0]})),r=function(e){var t=Math.max(0,e.length-5);return t?"...".concat(e.substring(t)):e};this.apiService.BarcodeLookup(i).then((function(t){var i=t||{},o=0,s=n.map((function(t){var n=t.shift(),s={id:o,bar:n||"",bardisp:n?r(n):"",addText:t.join(", "),name:e.NO_ELAB_RECORD,type:a.CUSTOM,tokens:t};if(n){var c=n;if(Number(c)){for(;c.length<12;)c="0".concat(c);for(12==c.length&&(c="005".concat(c));c.length<15;)c="0".concat(c)}if(i[c]){var l,d=i[c];s.name=null===d||void 0===d?void 0:d.name;var u=null===(l=i[c])||void 0===l?void 0:l.altID;u?(s.bar=u,s.bardisp=u):s.bar=c,s.type=(null===d||void 0===d?void 0:d.sampleID)?a.SAMPLE:a.STORAGE_LOCATION}}return o+=1,s}));e.setState({labels:s})})).catch((function(e){console.error(e)})).finally((function(){e.setState({gettingData:!1})})),this.setState({gettingData:!0})}},{key:"onLabelInputChanged",value:function(e){var t=this,n=e.target.value;this.lastChange=Date.now(),setTimeout((function(){Date.now()-t.lastChange>=t.UPDATE_DELAY&&(t.setState({labelsRaw:n}),t.parseLabels())}),this.UPDATE_DELAY)}},{key:"awaitResults",value:function(e){var t=this;return new Promise((function(n,a){var i=25;!function r(){--i<=0&&a(),setTimeout((function(){t.apiService.PollPrintInfo(e).then((function(e){e.Success?n(e.Data):r()}))}),500)}()}))}},{key:"onPrintAll",value:function(){var e=this,t={Labels:this.state.labels.map((function(t){var n=t.name===e.NO_ELAB_RECORD?[]:[t.name];return{Barcode:t.bar,Texts:n.concat(t.tokens)}})),TemplateName:this.state.labelTemplateName,PrinterName:this.state.printerName};this.setState({printing:!0}),this.apiService.PrintLabels(t).then((function(t){return e.awaitResults(t)})).then((function(e){console.log(e),alert(e.Message)})).catch((function(){})).finally((function(){return[e.setState({printing:!1})]}))}},{key:"onRefresh",value:function(){var e=this;this.setState({refreshing:!0}),this.apiService.RefreshPrintInfo().then((function(t){return e.awaitResults(t)})).then((function(t){var n=t.printers&&t.printers.length>0?t.printers.filter((function(e){return e.toLowerCase().includes("label")})):["default"],a=t.templates&&t.templates.length>0?t.templates:["default"];e.setState({availablePrinters:n,availableTemplates:a,refreshing:!1})}))}},{key:"onToClipboard",value:function(){var e=this;this.setState({copied:this.state.copied+1});var t=["Name (don't copy back)","Barcode","Addtional Text"].join("\t"),n=this.state.labels.map((function(e){return[e.name,e.bar,e.addText].join("\t")})),a=[t].concat(n).join("\n");navigator.clipboard.writeText(a),setTimeout((function(){e.setState({copied:e.state.copied-1})}),1e3)}},{key:"render",value:function(){var e,t=this,n={margin:"0 1em 0 1em"},a=["005000000123456","005000000123456, some additional info","..."].join("\n");return Object(S.jsx)(w.a,{container:!0,justifyContent:"center",style:{marginTop:"5vh",justifyContent:"center",alignItems:"center",alignContent:"center"},children:Object(S.jsx)(L.a,{style:{padding:"2em"},children:Object(S.jsxs)(w.a,{container:!0,direction:"column",spacing:3,children:[Object(S.jsx)(w.a,{item:!0,children:Object(S.jsx)(v.a,{variant:"h5",component:"h2",align:"left",gutterBottom:!0,style:{},children:"Print Labels"})}),Object(S.jsx)(w.a,{item:!0,children:Object(S.jsx)(T.a,{label:"Items",placeholder:a,multiline:!0,variant:"outlined",style:{width:"70em"},defaultValue:null===(e=this.props.startingBarcodes)||void 0===e?void 0:e.map((function(e){return"".concat(e)})).join("\n"),onChange:function(e){t.onLabelInputChanged(e)}})}),Object(S.jsxs)(w.a,{item:!0,style:{height:"30em"},justify:"center",children:[Object(S.jsx)(P.a,{in:this.state.gettingData,style:{position:"absolute",marginTop:"5em"},children:Object(S.jsx)(B.a,{size:50})}),Object(S.jsx)(_.a,{rows:this.state.labels,columns:[{field:"disabled",hide:!0},{field:"id",headerName:"ID",hide:!0},{field:"bardisp",headerName:"Barcode",width:100,sortable:!1},{field:"name",headerName:"Item Name",width:400,sortable:!1},{field:"addText",headerName:"Additional Text",width:600,sortable:!1}],rowsPerPageOptions:[100],onPageSizeChange:function(){},isRowSelectable:function(e){return!e.row.disabled},disableSelectionOnClick:!0,disableColumnMenu:!0,disableColumnFilter:!0,disableColumnSelector:!0,style:{opacity:this.state.gettingData?.25:1}}),Object(S.jsx)(w.a,{item:!0,children:Object(S.jsx)(P.a,{in:this.state.printing,children:Object(S.jsx)(E.a,{})})})]}),Object(S.jsxs)(w.a,{item:!0,children:[Object(S.jsx)(T.a,{select:!0,label:"Label Template",variant:"outlined",style:{width:"20.5em",marginRight:"1em"},value:this.state.labelTemplateName,onChange:function(e){t.setState({labelTemplateName:e.target.value})},children:this.state.availableTemplates.map((function(e){return Object(S.jsx)(M.a,{value:e,children:e},e)}))}),Object(S.jsx)(T.a,{select:!0,label:"Printer Name",variant:"outlined",style:{width:"20em"},value:this.state.printerName,onChange:function(e){t.setState({printerName:e.target.value})},children:this.state.availablePrinters.map((function(e){return Object(S.jsx)(M.a,{value:e,children:e},e)}))}),Object(S.jsxs)(f.a,{variant:"contained",color:"primary",onClick:this.onRefresh.bind(this),disabled:this.state.refreshing,style:{margin:"0.6em"},children:[Object(S.jsx)(P.a,{in:this.state.refreshing,style:{position:"absolute"},children:Object(S.jsx)(B.a,{size:33})}),Object(S.jsx)(F.a,{})]})]}),Object(S.jsxs)(w.a,{item:!0,children:[Object(S.jsx)(f.a,{variant:"contained",color:"primary",disabled:!this.state.labelTemplateName||!this.state.printerName,style:n,onClick:function(){return t.onPrintAll()},children:"Print All"}),Object(S.jsxs)(f.a,{variant:"contained",color:"primary",style:n,onClick:this.onToClipboard.bind(this),children:["Copy to Clipboard ",this.state.copied>0?"\u2714":""]})]})]})})})}}]),n}(r.a.Component),G=n(246),z=function(e){Object(d.a)(n,e);var t=Object(u.a)(n);function n(e){var a;return Object(c.a)(this,n),(a=t.call(this,e)).apiService=void 0,a.UPDATE_DELAY=650,a.apiService=e.elabService,a.state={searching:!1,results:"",lastChange:Date.now(),storages:[],selectedSamples:[],errorText:"",errorCands:"",currentLocation:"",reloadingStorage:!1,searchText:""},a}return Object(l.a)(n,[{key:"setup",value:function(){var e=this;this.apiService.GetStorages().then((function(t){if(!t)return 0;var n=t.reduce((function(e,t){var n=t.name,a=t.storageLayerID,i={id:a,name:n.toLowerCase(),parent:t.parentStorageLayerID,children:[]};return e.set(a,i),e}),new Map),a=[];n.forEach((function(e,t,i){var r;0===e.parent?a.push(e):null===(r=n.get(e.parent))||void 0===r||r.children.push(e)})),e.setState({storages:a})}))}},{key:"componentDidMount",value:function(){var e=this,t=5;!function n(){if(e.apiService.LoggedIn())e.setup();else{if(--t<=0)return;setTimeout((function(){n()}),100)}}()}},{key:"doSearch",value:function(e){var t=this;return new Promise((function(n){var a=e.split(",").map((function(e){return e.trim()})),i=function(e,t){var n=t.split(" ");return e.filter((function(e){return n.reduce((function(t,n){return t&&e.name.includes(n)}),!0)}))};t.setState({errorText:"",errorCands:"",currentLocation:""});var r,o,s=[],c=!0,l=t.state.storages,d=Object(G.a)(a);try{for(d.s();!(o=d.n()).done;){var u=o.value,h=i(l,u=u.toLowerCase());if(1!==h.length){if(0===h.length){c=!1;var b=s.join(", ");t.setState({searching:!1,errorText:u&&u.length>0?"No storage location with name [".concat(u,"]"):"Maybe you have an extra comma?",errorCands:b.length>0?" in ".concat(b):""});break}c=!1,t.setState({searching:!1,errorText:u&&u.length>0?"Ambiguity for [".concat(u,"] between:"):"Specify one of:",errorCands:"".concat(h.map((function(e){return e.name})).join(", "))});break}var m=h[0];l=m.children,s.push(m.name),r=m}}catch(f){d.e(f)}finally{d.f()}if(!c||!r)return n(0);for(var p="".concat(r.id);p.length<12;)p="0".concat(p);for(12==p.length&&(p="008".concat(p));p.length<15;)p="0".concat(p);t.setState({currentLocation:"".concat(s.join(", ")," - ").concat(p)}),n(r.id)}))}},{key:"getSamples",value:function(e){var t=this;return this.apiService.GetSamplesByStorage(e).then((function(e){e||(e=[]),t.setState({selectedSamples:e.map((function(e){return{id:e.sampleID,name:e.name,type:e.sampleType.name}})),searching:!1})}))}},{key:"onSearchChanged",value:function(){var e=this,t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:void 0,n=t?t.target.value:this.state.searchText;this.setState({lastChange:Date.now(),searchText:n}),setTimeout((function(){Date.now()-e.state.lastChange>=e.UPDATE_DELAY&&(e.setState({searching:!0}),e.doSearch(n).then((function(t){if(0!==t)return e.getSamples(t)})))}),this.UPDATE_DELAY)}},{key:"onReloadStorages",value:function(){var e=this;this.setState({reloadingStorage:!0}),this.apiService.ReloadStorages().then((function(t){200==t&&(e.setup(),e.onSearchChanged()),e.setState({reloadingStorage:!1})}))}},{key:"render",value:function(){var e=this,t={margin:"0 1em 0 1em"};return Object(S.jsx)(w.a,{container:!0,justifyContent:"center",style:{marginTop:"5vh",justifyContent:"center",alignItems:"center",alignContent:"center"},children:Object(S.jsx)(L.a,{style:{width:"90vw",padding:"2em"},children:Object(S.jsxs)(w.a,{container:!0,direction:"column",spacing:3,children:[Object(S.jsx)(w.a,{item:!0,children:Object(S.jsx)(v.a,{variant:"h5",component:"h2",align:"left",gutterBottom:!0,style:{},children:"Samples By Storage Location"})}),Object(S.jsx)(w.a,{item:!0,children:Object(S.jsx)(T.a,{label:"Search",placeholder:"freezer 7, self 2, rack 3",variant:"outlined",onChange:this.onSearchChanged.bind(this),style:{width:"90vw"}})}),Object(S.jsxs)(w.a,{item:!0,children:[Object(S.jsx)(v.a,{align:"left",style:{color:"primary"},children:this.state.currentLocation}),Object(S.jsx)(v.a,{align:"left",style:{color:"red"},children:this.state.errorText}),Object(S.jsx)(v.a,{align:"left",style:{color:"red"},children:this.state.errorCands})]}),Object(S.jsxs)(w.a,{item:!0,style:{height:"30em"},justify:"center",children:[Object(S.jsx)(P.a,{in:this.state.searching,style:{position:"absolute",marginTop:"5em"},children:Object(S.jsx)(B.a,{size:50})}),Object(S.jsx)(_.a,{rows:this.state.selectedSamples,columns:[{field:"disabled",hide:!0},{field:"id",headerName:"Barcode",width:100,sortable:!1},{field:"name",headerName:"Name",width:400,sortable:!1},{field:"type",headerName:"Type",width:350,sortable:!1}],rowsPerPageOptions:[100],onPageSizeChange:function(){},isRowSelectable:function(e){return!e.row.disabled},disableSelectionOnClick:!0,disableColumnMenu:!0,disableColumnFilter:!0,disableColumnSelector:!0,style:{opacity:this.state.searching?.25:1}})]}),Object(S.jsxs)(w.a,{item:!0,children:[Object(S.jsx)(f.a,{variant:"contained",color:"primary",onClick:function(){e.props.onPrintCallback(e.state.selectedSamples.map((function(e){return e.id})))},style:t,children:"Print Labels"}),Object(S.jsxs)(f.a,{variant:"contained",color:"secondary",disabled:this.state.reloadingStorage,onClick:this.onReloadStorages.bind(this),style:t,children:["Reload Storages",Object(S.jsx)(P.a,{in:this.state.reloadingStorage,style:{position:"absolute"},children:Object(S.jsx)(B.a,{size:33,color:"secondary"})})]})]})]})})})}}]),n}(r.a.Component),K=n(247),Y=n.n(K),H=function(){function e(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:"";Object(c.a)(this,e),this.baseUrl=void 0,this.requester=void 0,this.baseUrl=t,this.requester=Y.a}return Object(l.a)(e,[{key:"genUrl",value:function(e){var t="".concat(this.baseUrl,"/").concat(e);return t.endsWith("/")?t.substring(0,t.length-1):t}},{key:"POST",value:function(e){var t=e.path,n=void 0===t?"":t,a=e.body,i=void 0===a?{}:a;return this.requester.post(this.genUrl(n),i)}}]),e}(),W=function(){function e(){Object(c.a)(this,e),this.clientID=void 0,this.firstname=void 0,this.lastname=void 0,this.requester=void 0,this.requester=new H("api/d1"),this.clientID="",this.firstname="",this.lastname=""}return Object(l.a)(e,[{key:"makeBody",value:function(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};return e.ClientID=this.clientID,e}},{key:"LoggedIn",value:function(){return""!==this.clientID}},{key:"Login",value:function(e,t){var n=this;return this.requester.POST({path:"login",body:{Username:e,Password:t}}).then((function(e){var t=e.data;switch(t.Code){case 200:return n.clientID=t.ClientID,n.firstname=t.FirstName,n.lastname=t.LastName,console.log("logged in as ".concat(t.FirstName)),[!0,""];case 401:return[!1,"Incorrect username/password"];default:return Promise.reject("Oops, something crashed...")}}))}},{key:"BarcodeLookup",value:function(e){var t=this.makeBody({Barcodes:e});return this.requester.POST({path:"barcodes",body:t}).then((function(e){return e.data.Results}))}},{key:"GetStorages",value:function(){var e=this.makeBody();return this.requester.POST({path:"allstorages",body:e}).then((function(e){return e.data.Results}))}},{key:"GetSamplesByStorage",value:function(e){var t=this.makeBody({StorageLayerID:e});return this.requester.POST({path:"samplesbystorage",body:t}).then((function(e){return e.data.Results}))}},{key:"ReloadStorages",value:function(){var e=this.makeBody();return this.requester.POST({path:"reloadcache",body:e}).then((function(e){return e.status}))}},{key:"PrintLabels",value:function(e){var t=this.makeBody(e);return t.Op="print",this.requester.POST({path:"printops",body:t}).then((function(e){return e.data.ID}))}},{key:"PollPrintInfo",value:function(e){var t=this.makeBody({ID:e,Op:"poll"});return this.requester.POST({path:"printops",body:t}).then((function(e){return e.data}))}},{key:"RefreshPrintInfo",value:function(){var e=this.makeBody({Op:"refreshinfo"});return this.requester.POST({path:"printops",body:e}).then((function(e){return e.data.ID}))}},{key:"LinkBarcode",value:function(e,t){var n=this.makeBody({AltBarcode:e,SampleBarcode:t});return this.requester.POST({path:"setaltid",body:n}).then((function(e){var t=e.data;return console.log(t),t}))}}]),e}(),J=function(e){Object(d.a)(n,e);var t=Object(u.a)(n);function n(){return Object(c.a)(this,n),t.apply(this,arguments)}return n}(W),V=function(){function e(){Object(c.a)(this,e)}return Object(l.a)(e,null,[{key:"GetApiService",value:function(){return this.I||(this.I=new J),this.I}}]),e}();V.I=void 0;var Q,X=n(248),Z=n.n(X),$=n(463),ee=n(468),te=n(465),ne=n(467),ae=n(462);!function(e){e[e.ELAB=0]="ELAB",e[e.LINK=1]="LINK"}(Q||(Q={}));var ie=function(e){Object(d.a)(n,e);var t=Object(u.a)(n);function n(e){var a;return Object(c.a)(this,n),(a=t.call(this,e)).apiService=void 0,a.lastCode=void 0,a.NO_SCAN="Nothing Scanned",a.barcodes=void 0,a.setIDPair=void 0,a.apiService=e.elabService,a.lastCode=null,a.barcodes={},a.setIDPair=null,a.state={currentCode:"",cardBorderColour:"transparent",w:300,h:300,mode:Q.ELAB,scanInfo:[a.NO_SCAN],actionButtonName:"Go",actionDisabled:!0},a}return Object(l.a)(n,[{key:"componentDidMount",value:function(){var e=[window.innerWidth,window.innerHeight],t=e[0],n=e[1];(t<n?t:n)<this.state.w&&this.setState({w:t-20,h:t-20})}},{key:"onScan",value:function(e){var t=this;return this.state.currentCode!=e&&(this.lastCode=this.state.currentCode),new Promise((function(n,a){t.setState({currentCode:e,cardBorderColour:t.props.theme.palette.primary.main},(function(){return n()}));var i=function(e,n){return new Promise((function(a,i){setTimeout((function(){t.setState({cardBorderColour:e}),a()}),n)}))};i("transparent",100).then((function(){return i(t.props.theme.palette.primary.main,60)})).then((function(){return i("transparent",500)}))}))}},{key:"tryGetBarcode",value:function(e){var t=this,n=this.barcodes[e];return n?Promise.resolve(n):this.apiService.BarcodeLookup([e]).then((function(n){var a=Object.keys(n).filter((function(t){return t===e})),i=a.length>0?n[a[0]]:null;if(i)return t.barcodes[e]=i,i}))}},{key:"updateInfo",value:function(){var e=this;this.state.currentCode&&this.tryGetBarcode(this.state.currentCode).then((function(t){var n;t?console.log(t):console.log("nada");var a=e.barcodes[e.state.currentCode];e.setIDPair=null;var i=!1;switch(+e.state.mode){case Q.ELAB:n=["Barcode: [".concat(e.state.currentCode,"]")],a&&(n=n.concat(["".concat(a.name)]),i=!0);break;case Q.LINK:e.lastCode?(a?(n=["Link [".concat(e.lastCode,"]"),"to [".concat(a.name,"] ?")],i=!0):n=["[".concat(e.state.currentCode,"] has no attached sample!"),"try again"],e.setIDPair=[e.lastCode,e.state.currentCode],e.lastCode=null):a?(n=["Link [awaiting scan]","to sample barcode","","[".concat(e.state.currentCode,"] is already attached to"),"".concat(a.name)],e.lastCode=null):n=["Link [".concat(e.state.currentCode,"]"),"to [awaiting scan]"];break;default:n=[e.NO_SCAN]}e.setState({scanInfo:n,actionDisabled:!i})}))}},{key:"onAct",value:function(){var e=this;switch(+this.state.mode){case Q.ELAB:window.open(this.barcodes[this.state.currentCode].link,"_blank");break;case Q.LINK:if(this.setIDPair){var t=Object(C.a)(this.setIDPair,2),n=t[0],a=t[1];this.apiService.LinkBarcode(n,a).then((function(t){204==t.Code?alert("success!"):alert("failed to link"),e.updateInfo()}))}}}},{key:"onClear",value:function(){var e=this;this.lastCode=null,this.setState({scanInfo:[this.NO_SCAN],currentCode:""},(function(){return e.updateInfo()}))}},{key:"onToClipboard",value:function(){navigator.clipboard.writeText(this.state.currentCode)}},{key:"render",value:function(){var e=this,t={padding:"2em 0 2em 0",border:"5px solid",borderColor:this.state.cardBorderColour},n={margin:"0 1em 0 1em",width:"6em"};return Object(S.jsx)(w.a,{container:!0,justifyContent:"center",style:{marginTop:"5vh",justifyContent:"center",alignItems:"center",alignContent:"center"},children:Object(S.jsx)(L.a,{style:t,children:Object(S.jsxs)(w.a,{container:!0,direction:"column",spacing:0,children:[Object(S.jsx)(w.a,{item:!0,children:Object(S.jsx)(v.a,{variant:"h5",component:"h2",align:"center",gutterBottom:!1,style:{},children:"Scanner"})}),Object(S.jsx)(w.a,{item:!0,children:Object(S.jsx)(ae.a,{style:{},children:Object(S.jsx)(Z.a,{width:this.state.w,height:this.state.h,facingMode:"environment",onUpdate:function(t,n){n&&e.onScan(n.getText()).then((function(){return e.updateInfo()}))}})})}),Object(S.jsx)(w.a,{item:!0,children:Object(S.jsxs)(ne.a,{component:"fieldset",children:[Object(S.jsx)(v.a,{variant:"h6",component:"h6",align:"center",gutterBottom:!1,children:"After Scanning:"}),Object(S.jsxs)(ee.a,{row:!0,value:this.state.mode,onChange:function(t){var n=t.target.value,a=+n===Q.ELAB.valueOf()?"Go":"Link";e.setState({mode:n,actionButtonName:a},(function(){return e.updateInfo()}))},children:[Object(S.jsx)(te.a,{value:Q.ELAB,label:"Open in eLab",control:Object(S.jsx)($.a,{sx:{"&.Mui-checked":{color:this.props.theme.palette.primary.main}}})}),Object(S.jsx)(te.a,{value:Q.LINK,label:"Link Barcodes",control:Object(S.jsx)($.a,{sx:{"&.Mui-checked":{color:this.props.theme.palette.primary.main}}})})]})]})}),Object(S.jsx)(w.a,{item:!0,children:Object(S.jsx)(ae.a,{style:{marginBottom:"1em",border:"1px solid",borderRadius:"0.3em",width:this.state.w,borderColor:this.props.theme.palette.primary.main},children:this.state.scanInfo.map((function(e,t){return Object(S.jsx)(v.a,{align:"left",style:{color:"primary"},children:e},t)}))})}),Object(S.jsxs)(w.a,{item:!0,children:[Object(S.jsx)(f.a,{variant:"contained",color:"secondary",style:n,onClick:function(){return e.onClear()},children:"Clear"}),Object(S.jsx)(f.a,{variant:"contained",color:"primary",style:n,disabled:this.state.actionDisabled,onClick:function(){return e.onAct()},children:this.state.actionButtonName})]}),Object(S.jsx)(w.a,{item:!0,children:Object(S.jsx)(f.a,{variant:"contained",color:"primary",style:{marginTop:"1em"},onClick:function(){e.onToClipboard()},children:"Copy to Clipboard"})})]})})})}}]),n}(r.a.Component),re=Object(h.b)({palette:{primary:{main:"#00abab",contrastText:"#FFFFFF"},secondary:{main:"#d32f2f"},contrastThreshold:3,tonalOffset:.2}}),oe=function(e){Object(d.a)(n,e);var t=Object(u.a)(n);function n(e){var a;Object(c.a)(this,n),(a=t.call(this,e)).defaultActiveComponent=void 0,a.elabService=void 0,a.elabService=V.GetApiService();var i=function(){return Object(S.jsx)(z,{elabService:a.elabService,onPrintCallback:function(e){a.setState({activeComponent:Object(S.jsx)(q,{elabService:a.elabService,startingBarcodes:e})})}})},r=[{name:"Print",disabled:!1,makeNextPage:function(){return Object(S.jsx)(q,{elabService:a.elabService})}},{name:"Search By Storage Location",disabled:!1,makeNextPage:i},{name:"Scanner",disabled:!1,makeNextPage:function(){return Object(S.jsx)(ie,{elabService:a.elabService,theme:re})}}];return a.defaultActiveComponent=Object(S.jsx)(R,{theme:re,functions:r,clicked:function(e){return a.toFunctionPage(e)}}),a.state={activeComponent:a.defaultActiveComponent},a}return Object(l.a)(n,[{key:"toFunctionPage",value:function(e){e&&e.makeNextPage&&this.setState({activeComponent:e.makeNextPage()})}},{key:"render",value:function(){var e=this;return document.getElementById("favicon").href="/forcefavicon",Object(S.jsx)(b.a,{theme:re,children:Object(S.jsxs)("div",{className:"app-container",children:[Object(S.jsx)(x,{onHome:function(){e.setState({activeComponent:e.defaultActiveComponent})}}),Object(S.jsx)(N,{elabService:this.elabService}),this.state.activeComponent]})})}}]),n}(r.a.Component);n(389),n(390);s.a.render(Object(S.jsx)(r.a.StrictMode,{children:Object(S.jsx)(oe,{})}),document.getElementById("root"))}},[[392,1,2]]]);
//# sourceMappingURL=main.64a0452d.chunk.js.map