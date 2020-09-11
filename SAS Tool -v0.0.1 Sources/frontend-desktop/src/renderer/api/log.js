import request from '@/utils/request'

export function fetchList(data) {
  return request({
    url: '/log/list',
    method: 'post',
    data
  })
}

export function getAnaResult(data) {
  return request({
    url: '/log/analysis',
    method: 'post',
    data
  })
}

export function getLogblock(data) {
  return request({
    url: '/log/block',
    method: 'post',
    data
  })
}
