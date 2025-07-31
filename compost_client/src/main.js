import {createApp} from 'vue'
import App from './App.vue'
//全局导入element-plus
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import router from './router/router.js'
import VueAmap from '@vuemap/vue-amap'


import VMdPreview from '@kangc/v-md-editor/lib/preview'
import '@kangc/v-md-editor/lib/style/preview.css'
import githubTheme from '@kangc/v-md-editor/lib/theme/github'
import hljs from 'highlight.js'

// 初始化配置
VMdPreview.use(githubTheme, {
    Hljs: hljs, // 必须传递 Hljs 实例
    extend(md) {
        // 可在此处添加自定义插件
    }
})

const app = createApp(App)
app.use(VMdPreview) // 全局注册组件
app.use(VueAmap, {
    key: '764939a666fd22eb232d8f7a2b4ff34f',
    securityJsCode: 'c9ec1f917a075524896e5c96f0a1cb2c',
    version: "2.0",
    plugin: ['AMap.Geocoder', 'AMap.PlaceSearch'],
})
app.use(ElementPlus).use(router).mount('#app')
