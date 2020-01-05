<template>
    <div class="home" style="height: 100%">
        <el-container>
            <el-aside width="50px" v-if="connected===true">
                <el-button @click="fullscreen">全屏</el-button>
                <br/>
                <el-button @click="pasteToServer">粘贴</el-button>
                <br/>
                <el-input v-model="clipText" type="textarea" :autosize="{ minRows: 2, maxRows: 20}"></el-input>
            </el-aside>
            <el-container>
                <el-header v-if="connected===false">
                    <el-row>
                        <el-col :span="12">
                            <div style="margin-right: 20px"> {{username}}</div>
                        </el-col>
                        <el-col :span="12">
                            <el-button type="primary" @click="addDocker">add docker</el-button>
                        </el-col>
                        <el-col></el-col>
                    </el-row>
                </el-header>
                <el-main style="padding: 0px">
                    <div id="screen" style="width: 100%;height: 100%">
                    </div>

                </el-main>
            </el-container>
        </el-container>


        <!--    <img alt="Vue logo" src="../assets/logo.png">-->
        <!--    <HelloWorld msg="Welcome to Your Vue.js App"/>-->
    </div>
</template>

<script>
    // @ is an alias to /src

    import RFB from '@novnc/novnc/core/rfb.js'
    import {serverurl, serverip} from '../config.js'

    export default {
        name: 'home',

        data() {
            return {
                connected: false,
                rfb: null,
                url: undefined, //链接的url
                IsClean: false, //是否已断开并不可重新连接
                connectNum: 0, //重连次数
                username: undefined,
                port: '',
                clipText: '',
                timer: undefined
            }
        },
        methods: {
            resize() {
                let doc = document.getElementById("screen")
                let height = doc.offsetHeight
                let width = doc.offsetWidth
                let bi = 16 / 9
                if (height / width > bi) {
                    // eslint-disable-next-line no-console
                    console.log('change wid' + document.body.clientHeight)
                    doc.style.width = "" + Math.min(document.body.clientHeight, height * bi) + "px";
                } else {
                    doc.style.height = "" + Math.min(document.body.clientWidth, width / bi) + "px";
                }
            },
            fullscreen: function () {
                let full = document.getElementById("screen")
                this.launchIntoFullscreen(full)
            },
            launchIntoFullscreen: function (element) {
                if (element.requestFullscreen) {
                    element.requestFullscreen();
                } else if (element.mozRequestFullScreen) {
                    element.mozRequestFullScreen();
                } else if (element.webkitRequestFullscreen) {
                    element.webkitRequestFullscreen();
                } else if (element.msRequestFullscreen) {
                    element.msRequestFullscreen();
                }
            },
            addDocker: async function () {
                let username = this.username
                if (!this.username) return
                let sendjs = {
                    'username': username
                }
                let res = await this.axios.post(serverurl + '/api/add', JSON.stringify(sendjs))
                let dockerNow = res.data.dockerStatus
                // let link = res.data.link
                // window.open(link, '_blank')
                // eslint-disable-next-line no-console
                this.port = dockerNow[username].port
                this.connected = true

                this.connectVnc()
            },
            disconnectedFromServer(msg) {
                setTimeout(() => this.connectVnc(), 1000)
                clearTimeout(this.timer)
                if (msg.detail.clean) {
                    // 根据 断开信息的msg.detail.clean 来判断是否可以重新连接
                } else {
                    //这里做不可重新连接的一些操作
                }
            },
            // 连接成功的回调函数
            connectedToServer() {
                // eslint-disable-next-line no-console
                console.log('success')
                let fun = undefined
                fun = async () => {
                    let sendjs = {
                        'username': this.username,
                    }
                    try {
                        await this.axios.post(serverurl + '/api/live', JSON.stringify(sendjs))
                        // eslint-disable-next-line no-empty
                    } catch (e) {

                    }
                    this.timer = setTimeout(fun, 10e3)
                }
                fun()
                // this.resize()

            },

            //连接vnc的函数
            clipboardFromServer(msg) {
                // eslint-disable-next-line no-console
                console.log(msg)
                let message = msg.detail.text

                function handler(event) {
                    event.clipboardData.setData('text/plain', message);
                    document.removeEventListener('copy', handler, true);
                    event.preventDefault();
                }

                document.addEventListener('copy', handler, true);
                document.execCommand('copy');
            },
            pasteToServer() {

                this.rfb.clipboardPasteFrom(this.clipText)
                this.clipText = ''
            },

            connectVnc() {
                let url = `ws://${serverip}:${this.port}/websockify`
                // eslint-disable-next-line no-console
                // console.log(url)
                let rfb = new RFB(document.getElementById('screen'), url, {
                    // 向vnc 传递的一些参数，比如说虚拟机的开机密码等
                    credentials: {}
                });
                rfb.addEventListener('connect', this.connectedToServer);
                rfb.addEventListener('disconnect', this.disconnectedFromServer);
                rfb.addEventListener('clipboard', this.clipboardFromServer)
                rfb.scaleViewport = true;  //scaleViewport指示是否应在本地扩展远程会话以使其适合其容器。禁用时，如果远程会话小于其容器，则它将居中，或者根据clipViewport它是否更大来处理。默认情况下禁用。
                rfb.resizeSession = true; //是一个boolean指示是否每当容器改变尺寸应被发送到调整远程会话的请求。默认情况下禁用
                this.rfb = rfb;

            }
        },
        mounted: function () {
            this.username = this.$store.state.username
            if (!this.username) {
                this.$router.push({path: '/'})
            }
            window.onresize = () => {
                if (this.connected) {
                    // this.resize()
                }
            }

            this.addDocker()
        },
        destroyed() {
            window.onresize = null;
        },
        beforeDestroy() {
            clearTimeout(this.timer)
        }
    }
</script>
<style>
    html, body {
        height: 100%;
    }

    .el-header {
        background-color: #B3C0D1;
        color: #333;
        text-align: center;
        line-height: 40px;
    }

    .el-container {
        height: 100%;

    }

    .el-main {
        text-align: center;
        padding: 0px;
        height: 100%;
    }

    .el-button {
        margin-bottom: 20px;
    }

</style>