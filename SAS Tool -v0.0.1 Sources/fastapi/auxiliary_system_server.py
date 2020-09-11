import os
import time
import sys
print(sys.path)
sys.stdout.reconfigure(encoding='utf-8')
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from log_cfg import logger
#pip install -i http://mirrors.aliyun.com/pypi/simple/ uvicorn --trusted-host mirrors.aliyun.com
from AsyncWorker import AsyncWorker
from sas_data_utils import get_base_cmp, compare_sas_dataset, genearte_md5, get_compare_details
from api_data_model import DataSetListItem, DataSetCMPItem, CMP_ResultStatus, LogListItem, LogAnaItem, LogErrDetail, \
    CMP_Single_Detail
from sas_log_utils import get_modify_time, read_log, extract_log_block

logger.info('欢迎使用SAS辅助工具系统.....,按Ctrl+C终止系统')
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:9528/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.get("/")
# def index():
#     logger.debug("Welcome to the sas auxiliary system, work flow initial")
#     return 'Welcome to the sas auxiliary system'


@app.post('/user/login')
def login():
    return {"code": 20000, "data": {"token": "admin-token"}}


@app.get('/user/info')
def login_info():
    return {"code": 20000, "data": {"roles":["admin"], "introduction": "I am a super administrator", "avatar": "https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif", "name": "Super Admin"}}


@app.post('/log/list')
def get_log_list(log_list_item: LogListItem):
    """
    {"page":1,"limit":20,"filePath":"C:\\Users\\Lion\\Desktop\\log"}
    :return: {'code': 20000, 'data': {'total': total, 'items': pageList}}
    """
    logpath = log_list_item.filePath
    page = log_list_item.page
    limit = log_list_item.limit
    logger.debug('get log list request, log path:[{}] pageSize: [{}] pageNumber: [{}]'
                 .format(logpath,str(page), str(limit)))
    if os.path.isdir(logpath):
        datainfo = get_modify_time(logpath)
        logger.debug('got '+str(len(datainfo)) + ' log files in total' )
        total = len(datainfo)
        pageList = datainfo[int(limit)*(int(page)-1):int(limit) * int(page)]
        return {'code': 20000, 'data': {'total': total, 'items': pageList}}
    else:
        return {'code': 30001, 'root' : logpath}


@app.post('/dataset/list')
def get_sas_dataset_list(dslitem: DataSetListItem):
    """

    :param dslitem: vc
    :return:
    """
    logger.debug("get sas dataset List request, params: {} vs {}".format(dslitem.basePath,dslitem.cmpPath))
    basepath = r'\\'.join(dslitem.basePath.split('\\'))
    cmppath = r'\\'.join(dslitem.cmpPath.split('\\'))
    if os.path.exists(basepath) and os.path.exists(cmppath):
        data = get_base_cmp(basepath, cmppath)
        logger.debug("request complete successfully, coexisted: {} , onlyInBase: {}, onlyInCmp: {}"
                     .format(len(data['coexisted']), len(data['onlyInBase']), len(data['onlyInCmp'])))
        return {'code': 20000, 'data': data}
    else:
        logger.debug("dataset paths not exist,  {} vs {}".format(basepath, cmppath))
        return {'code': 30001}


@app.post('/log/analysis')
def get_log_analysis_result(*, log_ana_item: LogAnaItem):
    data = log_ana_item
    logger.debug("get log analysis request, at log path {} ".format(data.path))
    if os.path.isdir(data.path):
        results = []
        for item in data.selectedLog:
            results.append(read_log(item.filepath, item.name))
        return {'code': 20000, 'data': {'total': len(results), 'contents': results}}
    else:
        return {'code': 30001}


@app.post('/log/block')
def get_log_block(log_err_detail: LogErrDetail):
    """
    返回指定错误文本附近的日志块
    :return: log text around certain error
    """
    logger.debug("get log error detail block  request, at log path {} with error index {}"
                 .format(log_err_detail.fullpath, log_err_detail.errIndex))
    file_path = log_err_detail.fullpath
    error_index = log_err_detail.errIndex
    if os.path.isfile(file_path):
        data = extract_log_block(file_path, error_index)
        return {'code': 20000, 'data': data}
    else:
        return {'code': 30001}


@app.post('/dataset/cmpResult')
async def dataset_compare_result(*, ds_cmp_item: DataSetCMPItem):
    data = ds_cmp_item
    ticket_id = genearte_md5(str(int(round(time.time() * 1000))))
    logger.debug('开始多线程处理对比SAS数据集...')
    t1 = time.time()
    # 线程池提交任务
    # # 实例化一个AsyncWorker
    AsyncWorker(params=data, ticket_id=ticket_id)
    # 将ticket_id返回
    t2 = time.time()
    logger.debug('%s has been called and cost  %.2fs' % ('this multithread rotuine', (t2 - t1)))
    return {'code': 20000, "ticket_id": ticket_id, "totTask": len(data.selectedDataset)}


# 轮询任务
@app.post("/check-status")
async def check_status(param: CMP_ResultStatus):
    logger.debug("get Async Task by ID {}".format(param.ticket_id))
    ticket_id = param.ticket_id
    res = AsyncWorker.res
    status = AsyncWorker.status_info[ticket_id]
    return {'code': 20000, 'res': res, 'ticket_id': ticket_id,'status': status}


@app.post("/dataset/details")
async def get_single_detail(s_detail: CMP_Single_Detail):
    logger.debug("require single dataset compare result {} vs {}".format(s_detail.base, s_detail.cmp))
    #logger.debug(get_compare_details(s_detail.base, s_detail.cmp))
    sta, detail_dict = get_compare_details(s_detail.base, s_detail.cmp)
    # logger.debug(sta)
    return {'code': 20000, 'res': sta, 'details': detail_dict}


if __name__ == '__main__':
    # uvicorn.run('auxiliary_system_server:app', reload=True, host='127.0.0.1', port=8000, debug=True)
    uvicorn.run('auxiliary_system_server:app', host='127.0.0.1', port=8000)
