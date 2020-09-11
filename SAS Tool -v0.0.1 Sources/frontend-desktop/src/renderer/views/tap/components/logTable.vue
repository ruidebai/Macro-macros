<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input v-model="listQuery.filePath" placeholder="Log File path" :disabled="editableInput" style="width: 300px;" @keyup.enter.native="handleSearch" @input="change($event) " />
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click.native="handleSearch">
        Search
      </el-button>
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-s-promotion" @click.native="handleSubmit">
        Submit
      </el-button>
    </div>
    <el-table
      v-loading="listLoading"
      :data="list"
      element-loading-text="Loading"
      :row-style="{height:0+'px'}"
      :cell-style="{padding:0+'px'}"
      :row-key="getRowKeys"
      border
      fit
      highlight-current-row
      @selection-change="handleSelectionChange"
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
  </div>
</template>
<script>
import { fetchList, getAnaResult } from '@/api/log'
import waves from '@/directive/waves'
import { Message } from 'element-ui'
import { validPath } from '@/utils/validate.js'
import Pagination from '@/components/Pagination'
export default {
  components: { Pagination },
  directives: { waves },
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
      console.log(this.listQuery.filePath)
      if (!validPath(this.listQuery.filePath)) {
        Message({
          message: this.filePath + ' is  an illegal path,please check',
          type: 'error',
          duration: 2 * 1000
        })
        this.editableInput = false
        this.listQuery.filePath = ''
      } else {
        this.$notify({
          title: 'Success',
          message: 'valid path, requesting data',
          type: 'success',
          duration: 2000
        })
        this.editableInput = true
        this.fetchData()
      }
    },
    handleSubmit() {
      if (this.multipleSelection.length === 0) {
        Message({
          message: 'Select one at least',
          type: 'warning',
          duration: 3 * 1000
        })
      } else {
        this.$notify({
          title: 'Info',
          message: 'You\'ve chosen ' + this.multipleSelection.length + ' logs',
          type: 'info',
          duration: 500
        })
        this.logSubmit.path = this.listQuery.filePath
        this.logSubmit.selectedLog = this.multipleSelection
        // console.log(this.logSubmit.selectedLog)
        this.editableInput = false
        getAnaResult(this.logSubmit).then(response => {
          console.log(response)
          if (response.code === 20000) {
            this.$notify({
              title: 'Success',
              type: 'success',
              message: 'got response from server',
              duration: 500
            })
            this.$router.push({
              name: 'result', params: { data: response.data }})
            console.log(this.$route)
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

