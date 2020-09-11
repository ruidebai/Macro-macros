import { fetchtodolist } from '@/api/todo'
const state = {
  todolist: []
}

const mutations = {
  INITIAL_LIST(state, list) {
    state.todolist = list
  }
}

const actions = {
  initiallist(context) {
    fetchtodolist().then(({ data }) => {
      console.log(data)
      context.commit('INITIAL_LIST', data)
    })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}

