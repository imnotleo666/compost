// src/utils/request.js
import axios from 'axios';
import qs from 'qs';

// 创建 axios 实例
const service = axios.create({
    baseURL: 'http://localhost/api/', // 基础请求地址，可根据环境变量配置
    timeout: 500000 // 请求超时时间
});

// 请求拦截器
service.interceptors.request.use(
    config => {
        // 在发送请求之前做些什么，例如添加请求头
        // 这里可以添加 token 等信息
        const users = localStorage.getItem('user');
        if (users && users.trim().length > 0) {
            //console.log(users)
            let user = JSON.parse(users)
            config.headers['Authorization'] = `${user.id}`;
        }
        for (let key in config.data) {
            if (config.data[key] instanceof Object) {
                delete config.data[key]
            }
        }
        // 如果是 post 请求且指定为 form 格式
        if (config.method === 'post' && config.headers['Content-Type'] === 'application/x-www-form-urlencoded') {
            config.data = qs.stringify(config.data);
        }
        return config;
    },
    error => {
        // 处理请求错误
        console.log(error); // 打印错误信息
        return Promise.reject(error);
    }
);

// 响应拦截器
service.interceptors.response.use(
    response => {
        const res = response.data;
        return res;
    },
    error => {
        // 处理响应错误
        console.log('err' + error); // 打印错误信息
        return Promise.reject(error);
    }
);

// 封装请求方法
const request = {
    get(url, params) {
        return service.get(url, {
            params
        });
    },
    post(url, data) {
        const config = {
            headers: {}
        };
        config.headers['Content-Type'] = 'application/x-www-form-urlencoded';

        return service.post(url, data, config);
    },
    put(url, data) {
        return service.put(url, data);
    },
    delete(url, params) {
        return service.delete(url, {
            params
        });
    }
};

export default request;