// src/router/index.js
import {createRouter, createWebHistory} from 'vue-router';

import Login from '@/pages/Login.vue';
import Home from '@/pages/Home.vue';
import Center from "@/pages/Center.vue";
import RePass from "@/pages/RePass.vue";
import User from '@/pages/User.vue'
import DataBoard from "@/pages/DataBoard.vue";
import Log from "@/pages/Log.vue";
import Records from "@/pages/Records.vue";

const routes = [{
    path: '/',
    redirect: '/login'
},
    {
        path: '/login',
        name: 'Login',
        component: Login
    },
    {
        path: '/register',
        name: 'Register',
        component: () => import('@/pages/Register.vue')
    },
    {
        path: '/home',
        name: 'Home',
        component: Home,
        redirect: '/center',
        children: [
            {
                path: '/center',
                component: Center
            },
            {
                path: '/repass',
                component: RePass
            },
            {
                path: '/user',
                component: User
            },
            {
                path: '/dataBoard',
                component: DataBoard
            },
            {
                path: '/records',
                component: Records
            },
            {
                path: '/fileinfo',
                component: () => import('@/pages/FileInfo.vue')
            },
            {
                path: '/answer',
                component: () => import('@/pages/Answer.vue')
            },
            {
                path: '/log',
                component: Log
            }
        ]
    },
];

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes
});

export default router;