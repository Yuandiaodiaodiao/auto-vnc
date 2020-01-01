<template>
    <div class="home">
        <el-container>
            <el-header>Header</el-header>
            <el-main>
                <el-input v-model="input" placeholder="用户名">用户名:</el-input>
                <el-button type="primary" @click="addDocker">add docker</el-button>
                <el-row>
                    <el-col span="2">
                        <el-tag>运行中的容器:</el-tag>
                    </el-col>
                    <el-col span="22">
                        <el-tag
                                v-for="tag in tags"
                                :key="tag.name"
                                closable
                                :type="tag.type">
                            {{tag.name}}
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

    export default {
        name: 'home',

        data() {
            return {
                input: '',
                tags: [

                ]
            }
        },
        methods: {
            addDocker: async function () {
                let username = this.input
                let sendjs = {
                    'username': username
                }
                let res = await this.axios.post('http://ip.oops-sdu.cn:9006/api/add', JSON.stringify(sendjs))
                let link = res.data.link
                window.open(link, '_blank')
                let dockerNow = res.data.dockerStatus
                this.tags.length=0
                for (let x in dockerNow) {
                    this.tags.push({
                        name: `${x} port: ${dockerNow[x].port}`,
                    })
                }

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