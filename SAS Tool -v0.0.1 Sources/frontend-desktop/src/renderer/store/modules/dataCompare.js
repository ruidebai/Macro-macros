const state = {
  cmptasknum: 0,
  taskRunning: 0,
  taskDone: 0,
  taskTicket: '',
  cmptaskRes: [],
  dataCMPSummary: [],
  cmpRES_N1: [],
  cmpRES_0: [],
  cmpRES_1: [],
  cmpDiff_Detail: [],
  query_cache: {
    t_base: '',
    t_cmp: ''
  },
  sepcific_diff: []
}

const mutations = {
  CMP_TASK_NUM_UPDATE(state, num) {
    state.cmptasknum = num
  },
  TASK_RUNNING_UPDATE(state, num) {
    state.taskRunning = num
  },
  TASK_DONE_UPDATE(state, num) {
    state.taskDone = num
  },
  TASK_TICKET_UPDATE(state, ticket) {
    state.taskTicket = ticket
  },
  CMP_TASK_RESULT_PUSH(state, res) {
    state.cmptaskRes = res
  },
  CMP_RESULT_N1_PUSH(state, res) {
    state.cmpRES_N1 = []
    const temp = res.filter(function(item) {
      return item.flag === -1
    })
    console.log('CMP_RESULT_N1_PUSH  excuted', temp)
    state.cmpRES_N1 = temp
  },
  CMP_RESULT_0_PUSH(state, res) {
    state.cmpRES_0 = []
    const temp = res.filter(function(item) {
      return item.flag === 0
    })
    console.log('CMP_RESULT_0_PUSH  excuted', temp)
    state.cmpRES_0 = temp
  },
  CMP_RESULT_1_PUSH(state, res) {
    state.cmpRES_1 = []
    const temp = res.filter(function(item) {
      return item.flag === 1
    })
    console.log('CMP_RESULT_1_PUSH  excuted', temp)
    state.cmpRES_1 = temp
  },
  DATA_CMP_SUMMARY(state) {
    console.log('DATA_CMP_SUMMARY  excuted')
    state.dataCMPSummary = [{
      item: 'SAS数据集比对任务数',
      detail: state.cmptasknum
    },
    {
      item: 'SAS数据集无法比对任务数',
      detail: state.cmpRES_N1.length
    },
    {
      item: 'SAS数据集完全匹配任务数',
      detail: state.cmpRES_0.length
    },
    {
      item: 'SAS数据集存在不匹配任务数',
      detail: state.cmpRES_1.length
    }
    ]
  },
  DATA_CMP_DIFF_DETAIL(state, difList) {
    state.cmpDiff_Detail = difList
  },
  DATA_CMP_QUERY_CACHE(state, param) {
    state.query_cache.t_base = param.t_base
    state.query_cache.t_cmp = param.t_cmp
  },
  DATA_CMP_SPECIFIC_DIFF_PUSH(state, specDiff) {
    state.sepcific_diff = specDiff
  }

}

const actions = {
  cmptasknumUpdate({ commit }, num) {
    commit('CMP_TASK_NUM_UPDATE', num)
  },
  taskRunningUpdate({ commit }, num) {
    commit('TASK_RUNNING_UPDATE', num)
  },
  taskDoneUpdate({ commit }, num) {
    commit('TASK_DONE_UPDATE', num)
  },
  taskTicketUpdate({ commit }, ticket) {
    commit('TASK_TICKET_UPDATE', ticket)
  },
  cmpTaskResUpdate({ commit }, res) {
    console.log('CMP_TASK_RESULT_PUSH  excuted')
    commit('CMP_TASK_RESULT_PUSH', res)
  },
  cmpRES_N1PUSH({ commit }, res) {
    console.log('CMP_RESULT_N1_PUSH  excuted')
    commit('CMP_RESULT_N1_PUSH', res)
  },
  cmpRES_0PUSH({ commit }, res) {
    console.log('CMP_RESULT_0_PUSH  excuted')
    commit('CMP_RESULT_0_PUSH', res)
  },
  cmpRES_1PUSH({ commit }, res) {
    console.log('CMP_RESULT_1_PUSH  excuted')
    commit('CMP_RESULT_1_PUSH', res)
  },
  dataCMPSummary({ commit }) {
    commit('DATA_CMP_SUMMARY')
  },
  dataCMP_DIFF_DETAIL_PUSH({ commit }, difList) {
    commit('DATA_CMP_DIFF_DETAIL', difList)
  },
  dataCMP_QUERY_CACHE_UPDATE({ commit }, param) {
    console.log('DATA_CMP_QUERY_CACHE  excuted')
    commit('DATA_CMP_QUERY_CACHE', param)
  },
  dataCMPSpecificDiffPush({ commit }, specDiff) {
    commit('DATA_CMP_SPECIFIC_DIFF_PUSH', specDiff)
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}
