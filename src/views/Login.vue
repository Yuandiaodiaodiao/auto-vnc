<template>
    <el-card class="box-card">
        <div slot="header" class="clearfix">
            <span>登录</span>
        </div>
        <el-input v-model="username" placeholder="用户名" style="width: 200px"></el-input>
        <br/>
        <el-input v-model="password" placeholder="密码" show-password style="width: 200px;margin-top: 20px"></el-input>
        <br/>
        <el-button type="primary" style="margin-top: 20px" @click="login">登录</el-button>
        <br/>
        <div v-if="canlogin===false">登录失败 用户名或密码错误</div>
    </el-card>

</template>
<script>
    import {serverurl} from '../config.js'

    export default {
        name: 'login',
        data() {
            return {
                canlogin: true,
                username: '',
                password: '',
                tags: []
            }
        },
        methods: {
            login: async function () {
                let sendjs = {
                    'username': this.username,
                    'password': this.password
                }
                // eslint-disable-next-line no-console
                console.log(serverurl)
                let res = await this.axios.post(serverurl + '/api/login', JSON.stringify(sendjs))
                this.canlogin = res.data.isok || false
                if (this.canlogin) {
                    if (this.username === "admin") {
                        this.$router.push({path: 'add'})
                    } else {
                        this.$router.push({path: 'home'})
                    }
                    this.$store.commit('setUser', this.username)
                }

            }
        }
    }
</script>
<style>
    .text {
        font-size: 14px;
    }

    .item {
        margin-bottom: 18px;
    }

    .clearfix:before,
    .clearfix:after {
        display: table;
        content: "";
    }

    .clearfix:after {
        clear: both
    }

    .box-card {
        margin: auto;
        width: 480px;
    }
</style>
