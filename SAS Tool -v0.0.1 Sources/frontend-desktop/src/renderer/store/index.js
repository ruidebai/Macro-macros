import Vue from 'vue'
import Vuex from 'vuex'
import app from './modules/app'
import user from './modules/user'
import getters from './getters'
import logAna from './modules/logAna'
import todolist from './modules/todolist'
import dataCompare from './modules/dataCompare'

Vue.use(Vuex)

const store = new Vuex.Store({
  modules: {
    app,
    user,
    logAna,
    todolist,
    dataCompare
  },
  getters
})

export default store
