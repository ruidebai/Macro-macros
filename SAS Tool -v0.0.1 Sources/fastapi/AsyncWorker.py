# 定义一个AsyncWorker，继承Thread，重写run方法，run方法中调用WorkerController的do_something方法
from concurrent.futures import ThreadPoolExecutor, wait, as_completed
from log_cfg import logger
from sas_data_utils import compare_sas_dataset


class AsyncWorker(object):
    ASYNC_WORKER_INFO = dict()
    futures_List = []
    res = []
    status_info = dict()
    done_num = 0
    err_num = 0
    cancel_num = 0

    # 1. 创建任务列表
    # 2. 创建状态字典
    # 3. 创建查询状态字典的函数
    def __init__(self, params, ticket_id):
        self.params = params
        self.ticket_id = ticket_id
        self.commit_work()

    def afterdone(self, fn):
        if fn.cancelled():
            AsyncWorker.cancel_num += 1
            AsyncWorker.status_info[self.ticket_id] = {'done': AsyncWorker.done_num,
                                                       'error': AsyncWorker.err_num,
                                                       'cancel': AsyncWorker.cancel_num}
            logger.debug('done {}:取消'.format(fn.arg))
        elif fn.done():
            AsyncWorker.done_num += 1
            AsyncWorker.status_info[self.ticket_id] = {'done': AsyncWorker.done_num,
                                                       'error': AsyncWorker.err_num,
                                                       'cancel': AsyncWorker.cancel_num}
            error = fn.exception()
        if error:
            AsyncWorker.err_num += 1
            AsyncWorker.status_info[self.ticket_id] = {'done': AsyncWorker.done_num,
                                                       'error': AsyncWorker.err_num,
                                                       'cancel': AsyncWorker.cancel_num}
            logger.debug('done {} : 错误返回 : {}'.format(fn.arg, error))
        else:
            AsyncWorker.res.append(fn.result())
            logger.debug('done {} : 正常返回 '.format(fn.arg))

    def commit_work(self):
        executor = ThreadPoolExecutor(max_workers=10)
        AsyncWorker.futures_List = []
        AsyncWorker.res = []
        AsyncWorker.err_num = 0
        AsyncWorker.done_num = 0
        AsyncWorker.cancel_num = 0
        for item in self.params.selectedDataset:
            future = executor.submit(compare_sas_dataset, self.params.basePath + "\\" + item.base,
                                     self.params.cmpPath + "\\" + item.cmp)
            AsyncWorker.futures_List.append(future)
            AsyncWorker.status_info[item.base] = future.done()
            future.arg = item.base + "compare with " + item.cmp
            future.add_done_callback(self.afterdone)
