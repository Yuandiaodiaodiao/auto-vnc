let serverip='ip.oops-sdu.cn'
let serverport='9006'
let serverurl=`http://${serverip}:${serverport}`
if(NODE_ENV==="dev"){
    console.log("Dev")
}
export {serverurl,serverip}
