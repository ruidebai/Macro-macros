import request from '@/utils/request'

// 从后端请求的todolist数据
export function fetchtodolist(data) {
  return request({
    url: '/dosth',
    method: 'post',
    data
  })
}

