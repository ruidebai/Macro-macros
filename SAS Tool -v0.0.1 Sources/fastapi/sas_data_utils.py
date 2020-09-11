import hashlib
import os
import pandas as pd
from datacompy import Compare
from log_cfg import logger


class MyCompare(Compare):

    @logger.catch
    def report_to_json(self):
        """
        将对比后的结果用json的格式返回
        :return: json formated compare dataset
        """
        setSMRY = [{"DataSet": [self.df1_name, self.df2_name]}, {"Variables": [self.df1.shape[1], self.df2.shape[1]]},
                   {"Observations": [self.df1.shape[0], self.df2.shape[0]]}]  # 数据集汇总
        varSMRY = [{"coexisted": len(self.intersect_columns())},
                   {"varNumDiff": [self.df1_unq_columns(), self.df2_unq_columns()]}]  # 变量汇总
        obsSMRY = [{"matchedObs": str(self.intersect_rows.shape[0])}, {"fullmatchedObs": str(self.count_matching_rows())},
                   {"partunmatchedObs": str(self.intersect_rows.shape[0] - self.count_matching_rows())}]  # 观测汇总
        return {'setSMRY': setSMRY, 'varSMRY': varSMRY, 'obsSMRY': obsSMRY}

    def detail_json(self, column, sample_count=5):
        """Returns a sample sub-dataframe which contains the identifying
                columns, and df1 and df2 versions of the column.
                Parameters
                ----------
                column : str
                    The raw column name (i.e. without ``_df1`` appended)
                sample_count : int, optional
                    The number of sample records to return.  Defaults to 10.
                Returns
                -------
                Pandas.DataFrame
                    A sample of the intersection dataframe, containing only the
                    "pertinent" columns, for rows that don't match on the provided
                    column.
                """
        row_cnt = self.intersect_rows.shape[0]
        col_match = self.intersect_rows[column + "_match"]
        match_cnt = col_match.sum()
        sample_count = min(sample_count, row_cnt - match_cnt)
        sample = self.intersect_rows[~col_match].head(sample_count)
        return_cols = self.join_columns + [column + "_df1", column + "_df2"]
        to_return = sample[return_cols]
        return to_return


@logger.catch
def get_file_list(path, extension_name):
    """
    获取对应路径下所有符合extension_name后缀的文件名，并返回格式化数据
    :param path: 文件路径名
    :param extension_name:  文件拓展名 例如.sas、 .log 、.sas7bdat
    :return: {'data':[],'pathname':''}
    """
    file_names = []
    for root, dirs, files in os.walk(path):
        dirs[:] = []  # 忽略当前目录下的子目录
        for file in files:
            if file.endswith(extension_name):
                file_names.append(file)
    return {"fileNames": file_names, "path": path}


@logger.catch
def get_base_cmp(basepath, cmppath):
    """

    :param cmppath: base file path
    :param basepath: compare file path
    :return: {'base':basepath，'compare':compare path, 'coexisted': [],'onyInbase':[],'onlyInCmp':[]}
    """
    basedata = get_file_list(basepath, ".sas7bdat")
    cmpdata = get_file_list(cmppath, ".sas7bdat")
    return {"base": basedata['path'],
            "compare": cmpdata['path'],
            # 'coexisted': list(set(basedata['fileNames']).intersection(set(cmpdata['fileNames']))),
            "coexisted": fuzz_match(basedata['fileNames'], cmpdata['fileNames']),
            "onlyInBase": fuzz_set_diff(basedata['fileNames'], cmpdata['fileNames']),
            "onlyInCmp": fuzz_set_diff(cmpdata['fileNames'], basedata['fileNames'])}


@logger.catch
def fuzz_match(set1,set2):
    """
    数据集模糊匹配,带有 QC_前缀的和没带的都能匹配上
    :param set1:base filename lists
    :param set2:cmp filename lists
    :return: list(set(basedata['fileNames']).intersection(set(cmpdata['fileNames']))) 但是能匹配QC/qc前缀
    """
    coexisted = []
    base = [x for x in set1 if x in set2 or "qc_"+str(x) in set2 or "QC_"+str(x) in set2]
    cmp = [x for x in set2 if x in set1 or str(x).replace("qc_",'') in set1 or str(x).replace("QC_", '') in set1]
    #  对两个列表进行排序
    base.sort(key=lambda x: x)
    cmp.sort(key=lambda x: str(x).replace("QC_", '').replace("qc_",''))
    for k, v in zip(base,cmp):
        coexisted.append({"base": k, "cmp": v})
    return coexisted


@logger.catch
def fuzz_set_diff(set1, set2):
    """

    :param set1:
    :param set2:
    :return:
    """
    set2_no_prefix = [str(x).replace("QC_", '').replace("qc_",'') for x in set2]
    return [x for x in set1 if str(x).replace("QC_", '').replace("qc_",'') not in set2_no_prefix]


@logger.catch
def pandas_read_sas(filename, encoding='windows-1252'):
    """
    数据集的读取，编码设置，以及异常捕获
    :param filename: sas 数据集的全路径
    :param encoding: 编码方式，默认为 windows-1252
    :return: 返回pandas Dataframe
    """
    try:
        data = pd.read_sas(filename,encoding=encoding)
    except FileNotFoundError:
        return {"fullpath": filename, "ERROR": 'Fatal Error,文件 '+filename+' 不存在请检查路径和文件名', "dataframe": None}
    except UnicodeDecodeError:
        return {"fullpath": filename, "ERROR": ' 解析文件 '+filename+' 时发生编码错误', "dataframe": None}
    except BaseException:
        return {"fullpath": filename, "ERROR": ' 未知错误,无法解析该日志', "dataframe": None}
    else:
        return {"fullpath": filename, "ERROR": None,"dataframe": data}


@logger.catch
def get_shotname_extension(fullpath):
    """
    从文件的全路径中捕获文件名和后缀
    :param fullpath: D:\\xx\\xx\\xx\\aa.c
    :return: (aa,c)
    """
    (filepath,tempfilename) = os.path.split(fullpath)
    (shotname,extension) = os.path.splitext(tempfilename)
    return (shotname, extension)


# @performance('ms')
@logger.catch
def compare_sas_dataset(basefile, cmpfile):
    """
    对比两个sas数据集，并且返回对比结果
    :param basefile: 输入为基准数据集的全路径
    :param cmpfile:  输入为对比数据集的全路径
    :return: 比较结果
    """
    base = pandas_read_sas("\\".join(basefile.split("\\")))
    cmp = pandas_read_sas("\\".join(cmpfile.split("\\")))
    # print('compare rotuine executed {} vs {}'.format(base['fullpath'], cmp['fullpath']))
    if base['dataframe'] is None or cmp['dataframe'] is None:
        # 如果两个数据集之中有一个是None， 那么也就不会继续比较两个数据集
        return {"flag": -1, "base": basefile, "cmp": cmpfile, "result": base['ERROR'] if base['dataframe'] is None else cmp['ERROR'] }
    else:
        # 如果两个数据集均为发生异常，就开始比对数据集，并返回比对结果
        df1_name = get_shotname_extension(basefile)[0]
        df2_name = get_shotname_extension(cmpfile)[0]
        compare_result = MyCompare(base['dataframe'], cmp['dataframe'], on_index=True, df1_name=df1_name, df2_name = df2_name)
        if compare_result.matches():
            # 如果两个数据集完全匹配上
            return {"flag": 0, "base": basefile, "cmp": cmpfile, "result": compare_result.report_to_json()}
        else: # 如果两个数据集存在unmatch issue
            return {"flag": 1, "base": basefile, "cmp": cmpfile, "result": compare_result.report_to_json()}


@logger.catch
def get_compare_details(bpath, cpath):
    """
    返回对比数据集的详细比较细节
    :param bpath: base dataset fullpath
    :param cpath: compare dataset fullpath
    :return: compare details
    """
    base = pandas_read_sas("\\".join(bpath.split("\\")))
    # logger.debug("\\".join(bpath.split("\\")))
    cmp = pandas_read_sas("\\".join(cpath.split("\\")))
    df1_name = get_shotname_extension(bpath)[0]
    df2_name = get_shotname_extension(cpath)[0]
    compare_result = MyCompare(base['dataframe'], cmp['dataframe'], on_index=True, df1_name=df1_name, df2_name=df2_name)
    # logger.debug(compare_result.column_stats)
    match_status = []
    match_sample = []
    any_mismatch = False
    compare_result.column_stats = sorted(compare_result.column_stats, key=lambda x: x["column"])
    for column in compare_result.column_stats:
        if not column["all_match"]:
            any_mismatch = True
            match_status.append(
                {
                "Column": column["column"],
                "UnEQ": str(column["unequal_cnt"]),
                "Max_Diff": str(column["max_diff"]),
                "Null_Diff": str(column["null_diff"])
                    }
                )
        if column["unequal_cnt"] > 0:
            match_sample.append(compare_result.detail_json(column["column"], sample_count=5))
    # logger.debug(match_status)
    data_dict = []
    for item in match_sample:
        data_dict.append({'index': str(-1), 'col1': str(item.columns[0]).replace('_df1', '_base'),
                          'col2': str(item.columns[1]).replace('_df2', '_cmp')})
        for index, row in item.iterrows():
            data_dict.append({'index': str(index), 'col1': str(row[0]), 'col2': str(row[1])})
    # match_status = sorted(match_status, key=lambda x: x["Column"])
    return match_status, data_dict

# print(get_compare_details("D:\\Projects\\SAS\\base\\addv.sas7bdat", "D:\\Projects\\SAS\compare\\addv.sas7bdat"))


def genearte_md5(str):
    # 创建md5对象
    hl = hashlib.md5()
    # Tips
    # 此处必须声明encode
    # 否则报错为：hl.update(str)    Unicode-objects must be encoded before hashing
    hl.update(str.encode(encoding='utf-8'))
    logger.debug('MD5加密前为 ：' + str)
    logger.debug('MD5加密后为 ：' + hl.hexdigest())
    return hl.hexdigest()