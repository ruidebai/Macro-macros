
const state = {
  logresult: [],
  logwithIssue: [],
  logSummary: [],
  issueDetials: [],
  resNum: 0
}

const mutations = {
  LOG_RES_PUSH(state, resList) {
    state.logresult = resList
  },
  RES_NUM_UPDATE(state, num) {
    state.resNum = num
  },
  LOG_ERR_PUSH(state, resList) {
    state.logwithIssue = resList.filter(function(item) {
      return item.result > 0
    })
  },
  LOG_ANA_SUMMARY(state) {
    state.logSummary = [{
      item: '总共扫描了多少个日志文件',
      detail: state.resNum
    },
    {
      item: '不存在问题的文件个数',
      detail: state.resNum - state.logwithIssue.length
    },
    {
      item: '存在问题的日志文件个数',
      detail: state.logwithIssue.length
    }
    ]
  },
  ISSUE_DETAILS(state, resList) {
    state.issueDetials = []
    const temp = resList.filter(function(item) {
      return item.result > 0
    })
    for (var i = 0; i < temp.length; i++) {
      for (var j = 0; j < temp[i].result; j++) {
        state.issueDetials.push({
          logName: temp[i].name,
          errIndex: Object.keys(temp[i].errors)[j],
          errName: temp[i].errors[Object.keys(temp[i].errors)[j]],
          fullpath: temp[i].fullpath
        })
      }
    }
  }
}

const actions = {
  logresPush({ commit }, resList) {
    commit('LOG_RES_PUSH', resList)
  },
  resnumUpdate({ commit }, num) {
    commit('RES_NUM_UPDATE', num)
  },
  logerrPush({ commit }, resList) {
    commit('LOG_ERR_PUSH', resList)
  },
  loganasummary({ commit }) {
    commit('LOG_ANA_SUMMARY')
  },
  issuedetials({ commit }, resList) {
    commit('ISSUE_DETAILS', resList)
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}
