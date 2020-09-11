<template>
  <div class="app-container">
    <el-container class="filter-container">
      <el-header>
        <el-input v-model="listQuery.filePath" placeholder="Log File path" :disabled="editableInput" style="width: 300px;" @keyup.enter.native="handleSearch" @input="change($event) " />
        <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click.native="handleSearch" style="margin-left:5px;">
          Search
        </el-button>
        <el-button v-waves class="filter-item" type="primary" icon="el-icon-check" @click.native="handleSubmit">
          Submit
        </el-button>
      </el-header>
      <el-main>
        <el-table v-loading="listLoading"
                  :data="list"
                  element-loading-text="Loading"
                  :row-style="{height:0+'px'}"
                  :cell-style="{padding:0+'px'}"
                  :row-key="getRowKeys"
                  border
                  fit
                  highlight-current-row
                  @selection-change="handleSelectionChange"
                  ref="multiTable"
    >
      <el-table-column type="selection" :reserve-selection="true" width="40" align="center" />
      <el-table-column label="Log File Name">
        <template slot-scope="scope">
          {{ scope.row.name }}
        </template>
      </el-table-column>
      <el-table-column align="center" prop="created_at" label="Modified Time" width="300">
        <template slot-scope="scope">
          <i class="el-icon-time" />
          <span>{{ scope.row.modified_time }}</span>
        </template>
      </el-table-column>
    </el-table>
    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="fetchData" />
      </el-main>
    </el-container>      

  </div>
</template>
<script>
import { fetchList, getAnaResult } from '@/api/log'
import waves from '@/directive/waves'
import { Message } from 'element-ui'
import { validPath } from '@/utils/validate.js'
import Pagination from '@/components/Pagination'
import store from '@/store'
export default {
  components: { Pagination },
  directives: { waves },
  store: store,
  data() {
    return {
      list: null,
      listLoading: true,
      filePath: '',
      total: 0,
      listQuery: {
        page: 1,
        limit: 20,
        filePath: undefined
      },
      logSubmit: {
        path: undefined,
        selectedLog: undefined
      },
      editableInput: false,
      multipleSelection: []
    }
  },
  created() {
    if (this.filePath === '') {
      this.listLoading = true
    } else {
      this.fetchData()
    }
  },
  methods: {
    fetchData() {
      this.listLoading = true
      fetchList(this.listQuery).then(response => {
        this.list = response.data.items
        this.total = response.data.total
        this.listLoading = false

        // Just to simulate the time of the request
        setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000)
      })
    },
    getRowKeys(row) {
      return row.name
    },
    handleSearch() {
      // console.log(this.listQuery.filePath)
      if (!validPath(this.listQuery.filePath)) {
        Message({
          message: this.filePath + '不是一个合法的路径，请检查',
          type: 'error',
          duration: 2 * 1000
        })
        this.editableInput = false
        this.listQuery.filePath = ''
      } else {
        this.$notify({
          title: 'Success',
          message: '路径正确，正在请求数据。。。',
          type: 'success',
          duration: 2000
        })
        //  clear selections
        this.$refs.multiTable.clearSelection() // 清除选中的数据
        // console.log('current selections:' + this.multipleSelection)
        this.editableInput = true
        this.fetchData()
      }
    },
    handleSubmit() {
      if (this.multipleSelection.length === 0) {
        Message({
          message: '请至少选择一个日志文件进行分析',
          type: 'warning',
          duration: 3 * 1000
        })
      } else {
        this.$notify({
          title: 'Info',
          message: '你总共选择了 ' + this.multipleSelection.length + ' 个日志',
          type: 'info',
          duration: 500
        })
        this.logSubmit.path = this.listQuery.filePath
        this.logSubmit.selectedLog = this.multipleSelection
        // console.log(this.logSubmit.selectedLog)
        this.editableInput = false
        getAnaResult(this.logSubmit).then(response => {
          // console.log('got analyzed data from server')
          // console.log(response)
          if (response.code === 20000) {
            this.$notify({
              title: 'Success',
              type: 'success',
              message: '成功获取到分析结果',
              duration: 500
            })
            this.$store.dispatch('logAna/resnumUpdate', response.data.total)
            this.$store.dispatch('logAna/logresPush', response.data.contents)
            this.$store.dispatch('logAna/logerrPush', response.data.contents)
            this.$store.dispatch('logAna/loganasummary')
            this.$store.dispatch('logAna/issuedetials', response.data.contents)
            // 提示执行了多少个任务
            const errs = response.data.contents.filter(function(item) {
              return item.result > 0
            })
            let errNums = 0
            // 计算总共存在多少个异常
            errs.forEach((item) => {
              errNums += item.result
            })
            const infMSG = errNums > 0
              ? '共分析了 ' + this.multipleSelection.length + '个日志文件，\n 存在 ' + errNums + '个异常， 请点击<strong>扫描结果</strong>查看细节'
              : '不存在异常'
            this.$notify({
              title: 'Success',
              type: 'success',
              message: infMSG,
              dangerouslyUseHTMLString: true,
              offset: 200,
              duration: 5000
            })
          }
        })
      }
    },
    handleSelectionChange(val) {
      this.multipleSelection = val
    },
    change(e) {
      this.$forceUpdate()
    }
  }
}
</script>

