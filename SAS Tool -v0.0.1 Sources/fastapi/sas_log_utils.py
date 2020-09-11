import os
import time
from datetime import datetime
import pandas as pd
from log_cfg import logger


@logger.catch
def timeit(unit):
    """
    给函数计时的装饰器
    :param unit: 计时的单位
    :return: 打印调用函数所耗费的时间
    """
    def perf_decorator(f):
        def wrapper(*args,**kw):
            t1 = time.time()
            r = f(*args,**kw)
            t2 = time.time()
            if unit == 's':
                logger.debug(' %s() has been executed  in  %.2fs' %(f. __name__, (t2-t1)))
            elif unit == 'ms':
                logger.debug('%s() has been executed  in  %.2fms' %(f. __name__, (t2-t1)*1000))
            else:
                logger.debug('Error parameters')
            return r
        return wrapper
    return perf_decorator


@logger.catch
def get_modify_time(indir):
    data = []
    for root, dirs, files in os.walk(indir):
        dirs[:] = [] # 忽略当前目录下的子目录
        for file in files:
            if file.endswith(".log"):
                whole_file_name = os.path.join(root, file)
                modify_time = os.path.getmtime(whole_file_name)
                nice_show_time = datetime.fromtimestamp(modify_time)
                data.append({'name': file, 'modified_time': datetime.strftime(nice_show_time, '%Y-%m-%d %H:%M:%S'),
                             'filepath': indir})
    return data


@logger.catch
def read_log(path, name):
    try:
        fullpath = path + '\\' + name
        data = pd.read_table(fullpath, encoding='gb2312', header=None, delimiter="\n")
        data.columns = ['log']
    except FileNotFoundError:
        return {'name': name, 'fullpath': fullpath, 'result': -1, 'errors': 'Fatal Error,日志文件不存在请检查路径和文件名'}
    except UnicodeDecodeError:
        return {'name': name, 'fullpath': fullpath, 'result': -1,
                'errors': ' Encountered UnicodeDecodeError during log parse'}
    except BaseException:
        return {'name': name, 'fullpath': fullpath, 'result': -1,
                'errors': ' Failed to parse log file, check this log,无法解析该日志'}
    else:
        data['result'] = data.log.apply(process_line)
        if data[data.result == 1].log.size > 0:
            return {'name': name, 'fullpath': fullpath, 'result': data[data.result == 1].log.size,
                    'errors': data[data.result == 1].log.to_dict()}
        else:
            return {'name': name, 'fullpath': fullpath, 'result': 0, 'errors': 'no error exists'}


@logger.catch
def extract_log_block(path, index1):
    """
    :param path: 日志文件的全路径
    :param index: 错误信息的index
    :return: 错误日志信息的文本块
    """
    try:
        data = pd.read_table(path, encoding='gb2312', header=None, delimiter="\n")
        data.columns = ['log']
    except FileNotFoundError:
        return {'fullpath': path, 'errors': 'Fatal Error,日志文件不存在请检查路径和文件名', 'logBlock': None}
    except UnicodeDecodeError:
        return {'fullpath': path, 'errors': ' 解析日志文件时发生编码错误', 'logBlock': None}
    except BaseException:
        return {'fullpath': path, 'errors': ' 未知错误,无法解析该日志', 'logBlock': None}
    else:
        data['result'] = data.log.apply(process_line)
        data.loc[data.result == 1, ['log']] = wrap_html_tag(data.loc[data.result == 1, ['log']])
        block = object()
        index = int(index1)
        if index > 20:
            block = data[(data.index <= index + 20) & (data.index >= index - 20)].log.tolist()
        else:
            block = data[(data.index <= index + 40) & (data.index >= index)].log.tolist()
        return {'fullpath': path, 'errors': None, 'logBlock': block}


@logger.catch
def wrap_html_tag(line):
    """
    为粗无信息包裹上html标签
    :param line: 错误信息文本
    :return: 包裹上html标签的错误文本信息
    """
    return "<font color=red size=4>" + line + "</font>"


@logger.catch
def process_line(content):
    if (content.find("WARNING") > -1) or (content.find("ERROR") > -1) or (content.find("字符值已转换为数值") > -1) or (
            content.find("数值已转换为字符值") > -1) or (content.find("参数无效") > -1) or (
            content.find("缺失值的生成是对缺失值执行操作的结果") > -1) or (content.find("MERGE 语句有多个数据集带有重复的 BY 值") > -1) or (
            content.find("未初始化") > -1) or (content.find("not found or could not be loaded") > -1) or (
            content.find("uninitialized") > -1) or (content.find("Invalid") > -1) or (
            content.find("Division by zero") > -1) or (content.find("Missing values were generated") > -1) or (
            content.find("Numeric values have been converted to character values") > -1) or (
            content.find("Character values have been converted to numeric values") > -1) or (
            content.find("MERGE statement has more than one data set with repeats of BY values") > -1) or (
            content.find("At least one W.D format was too small for the number to be printed") > -1) or (
            content.find("Character format specified for the result of a numeric expression") > -1) or (
            content.find("Mathematical operations could not be performed at the following places") > -1) or (
            content.find("ERROR DETECTED IN ANNOTATE=") > -1) or (content.find("PROBLEM IN OBSERVATION") > -1) or (
            content.find("Reduction in size of titles") > -1) or (content.find("outside the axis range") > -1) or (
            content.find("The SAS System stopped processing this step because of insufficient disk space") > -1):
        return 1
    else:
        return 0

