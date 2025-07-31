import http from '../utils/http.js';

export default {
    repassword(params) {
        return http.post('user/repassword', params)
    },

    getRecordsList(params) {
        return http.post('/records/list', params)
    },
    createRecords(data) {
        return http.post('/records/add', data)
    },
    updateRecords(data) {
        return http.post('/records/update', data)
    },
    deleteRecords(id) {
        return http.post('/records/del', {id: id})
    },
    getLogList(params) {
        return http.post('/log/list', params)
    },
    createLog(data) {
        return http.post('/log/add', data)
    },
    updateLog(data) {
        return http.post('/log/update', data)
    },
    deleteLog(id) {
        return http.post('/log/del', {id: id})
    },
    getUserList(params) {
        return http.post('/user/list', params)
    },
    createUser(data) {
        return http.post('/user/add', data)
    },
    updateUser(data) {
        return http.post('/user/update', data)
    },
    deleteUser(id) {
        return http.post('/user/del', {id: id})
    },
    getAllData() {
        return http.post('/log/getAllData')
    },
    getFileinfoList(params) {
        return http.post('/fileinfo/list', params)
    },
    createFileinfo(data) {
        return http.post('/fileinfo/add', data)
    },
    updateFileinfo(data) {
        return http.post('/fileinfo/update', data)
    },
    deleteFileinfo(id) {
        return http.post('/fileinfo/del', {id: id})
    },
    getAnswer(data) {
        return http.post('/question/answer', data)
    },

    getRecordList(params) {
        return http.post('/record/list', params)
    },
    createRecord(data) {
        return http.post('/record/add', data)
    },
    updateRecord(data) {
        return http.post('/record/update', data)
    },
    deleteRecord(id) {
        return http.post('/record/del', {id: id})
    },
    getRecordById(id) {
        return http.post('/record/getById', {id: id})
    },
}