import request from '@/utils/request'

export function fetchDataList(data) {
  return request({
    url: '/dataset/list',
    method: 'post',
    data
  })
}

export function getbatchCMPResult(data) {
  return request({
    url: '/dataset/cmpResult',
    method: 'post',
    data
  })
}

export function getbatchCMPResult_parallel(data) {
  return request({
    url: '/dataset/cmpResult',
    method: 'post',
    data
  })
}

export function getbatchCMP_status(data) {
  return request({
    url: '/check-status',
    method: 'post',
    data
  })
}

export function getSingle_CMP_Detials(data) {
  return request({
    url: '/dataset/details',
    method: 'post',
    data
  })
}
