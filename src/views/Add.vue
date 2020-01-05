<template>
    <div class="home">
        <el-container>
            <el-header>Header</el-header>
            <el-main>
                <el-input v-model="input" placeholder="用户名">用户名:</el-input>
                <el-button type="primary" @click="addDocker">add docker</el-button>
                <el-row>
                    <el-col span="4">
                        <el-tag style="margin-right: 10px">运行中的容器:</el-tag>
                    </el-col>
                    <el-col span="20">
                        <el-tag style="margin-right: 10px"
                                v-for="(tag,index) in tags"
                                :key="tag.name"
                                closable
                                @close="handleClose(tag,index)"
                                :type="tag.type">
                            {{tag.name+' port='+tag.port}}
                        </el-tag>
                    </el-col>
                </el-row>

            </el-main>
        </el-container>
        <!--    <img alt="Vue logo" src="../assets/logo.png">-->
        <!--    <HelloWorld msg="Welcome to Your Vue.js App"/>-->
    </div>
</template>

<script>
    // @ is an alias to /src
    import {serverurl} from '../config'
    export default {
        name: 'home',

        data() {
            return {
                input: '',
                tags: []
            }
        },
        methods: {
            addDocker: async function () {
                let username = this.input
                let sendjs = {
                    'username': username
                }
                let res = await this.axios.post(serverurl+'/api/add', JSON.stringify(sendjs))
                let link = res.data.link
                window.open(link, '_blank')
                let dockerNow = res.data.dockerStatus
                this.tags.length = 0
                for (let x in dockerNow) {
                    this.tags.push({
                        name: `${x}`,
                        port: `${dockerNow[x].port}`,
                    })
                }

            },
            handleClose:async function(tag,index){
                let username=tag.name
                let sendjs = {
                    'username': username
                }
                let res = await this.axios.post(serverurl+'/api/delete', JSON.stringify(sendjs))
                this.tags.splice(index, 1)
                return res.data.isok
            }
        },
        mounted: async function () {
            this.username = this.$store.state.username
            if(this.username!=='admin'){
                this.$router.push({path: '/'})
            }
            let res = await this.axios.get(serverurl+'/api/status')
            let dockerNow = res.data.dockerStatus
            this.tags.length = 0
            for (let x in dockerNow) {
                this.tags.push({
                    name: `${x}`,
                    port: `${dockerNow[x].port}`,
                })
            }
        }
    }
</script>
<style>
    .el-header {
        background-color: #B3C0D1;
        color: #333;
        text-align: center;
        line-height: 60px;
    }


    .el-main {
        background-color: #E9EEF3;
        color: #333;
        text-align: left;
        line-height: 40px;
    }

    body > .el-container {
        margin-bottom: 40px;
    }

</style>