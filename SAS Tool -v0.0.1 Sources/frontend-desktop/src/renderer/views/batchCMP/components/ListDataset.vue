<template>
  <div class="app-container">
    <div class="filter-container">
      <div class="basePath">
        <el-input v-model="listQuery.basePath" placeholder="Base Dataset File Path" :disabled="editableInput" style="width: 500px;"  @input="change($event) " >
          <template slot="prepend" style="width: 150px;">Base数据集路径</template>
        </el-input>
        <el-input v-model="listQuery.cmpPath" placeholder="Compare Dataset File Path" :disabled="editableInput" style="width: 500px;" @keyup.enter.native="handleSearch" @input="change($event) ">
          <template slot="prepend" style="width: 150px;">Compare数据集路径</template>
        </el-input>
        <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" :disabled="ableBTN" style="margin-left: 15px;width: 100px;" @click.native="handleSearch">
          Search
        </el-button>
        <el-button v-waves class="filter-item" type="primary" icon="el-icon-check" :disabled="ableBTN" style="margin-left: 15px;width: 100px;" @click.native="handleParallel">
          {{ submit_btn_txt }}
        </el-button>
      </div>
    </div>
    <el-table
      v-loading="listLoading"
      :data="list"
      element-loading-text="Loading"
      :row-style="{height:5+'px'}"
      :cell-style="{padding:5+'px'}"
      :row-key="getRowKeys"
      border
      fit
      highlight-current-row
      style="width: 100%; margin-top: 15px;"
      @selection-change="handleSelectionChange"
    >
      <el-table-column type="selection" :reserve-selection="true" min-width="2%" align="center" />
      <el-table-column label="Base dataset name" min-width="44%">
        <template slot-scope="scope">
          {{ scope.row.base }}
        </template>
      </el-table-column>
      <el-table-column align="left" prop="created_at" label="Compare dataset name" min-width="44%">
        <template slot-scope="scope">
          <!-- <i class="el-icon-time" /> -->
          <span>{{ scope.row.cmp }}</span>
        </template>
      </el-table-column>
    </el-table>
    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="fetchData" style="margin-left: 15px;width: 150px;"/>
  </div>
</template>
<script>
import { fetchDataList, getbatchCMPResult_parallel, getbatchCMP_status } from '@/api/sasdataset'
import waves from '@/directive/waves'
import { Message } from 'element-ui'
import { validPath } from '@/utils/validate.js'
import Pagination from '@/components/Pagination'
import store from '@/store'
import { mapGetters } from 'vuex'
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
        basePath: undefined,
        cmpPath: undefined
      },
      datacmpSubmit: {
        basePath: undefined,
        cmpPath: undefined,
        selectedDataset: undefined
      },
      editableInput: false,
      multipleSelection: [],
      totTask: 0,
      status_done: 0,
      webSocket: null,
      wb_endpoint: '127.0.0.1:8000',
      wb_params: '',
      submit_btn_txt: 'Submit',
      ableBTN: false
    }
  },
  computed: {
    ...mapGetters(['cmptasknum', 'taskDone', 'taskTicket', 'cmptaskRes'])
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
      fetchDataList(this.listQuery).then(response => {
        console.log(response)
        this.listLoading = false
        this.list = response.data.coexisted
        this.total = response.data.coexisted.length
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
      if (!validPath(this.listQuery.basePath) && !validPath(this.listQuery.cmpPath)) {
        Message({
          message: this.basePath + ' or \n' + this.cmpPath + '不是一个合法的路径，请检查',
          type: 'error',
          duration: 2 * 1000
        })
        this.editableInput = false
        this.listQuery.basePath = ''
      } else {
        this.$notify({
          title: 'Success',
          message: '路径正确，正在请求数据。。。',
          type: 'success',
          duration: 2000
        })
        this.editableInput = true
        this.fetchData()
      }
    },
    getSecond(status_done) {
      const that = this
      if (parseInt(this.taskDone) + 1 > parseInt(this.cmptasknum)) {
        this.submit_btn_txt = 'Submit'
        this.ableBTN = false
        this.editableInput = false
        console.log('Compare Mission Completed!')
        this.$store.dispatch('dataCompare/cmpRES_N1PUSH', this.cmptaskRes)
        this.$store.dispatch('dataCompare/cmpRES_0PUSH', this.cmptaskRes)
        this.$store.dispatch('dataCompare/cmpRES_1PUSH', this.cmptaskRes)
        this.$store.dispatch('dataCompare/dataCMPSummary')
        Message({
          message: '数据集对比任务完成',
          type: 'success',
          duration: 2 * 1000
        })
      } else {
        this.ableBTN = true
        this.editableInput = true
        const tempA = parseInt(this.taskDone) < 10 ? '0' + this.taskDone : this.taskDone
        const tempB = parseInt(this.cmptasknum) < 10 ? '0' + this.cmptasknum : this.cmptasknum
        this.submit_btn_txt = tempA + ' / ' + tempB + ' '
        status_done++
        setTimeout(function() {
          that.handle_check_status()
          that.getSecond(status_done)
        }, 1500)
      }
    },
    handle_check_status() {
      getbatchCMP_status({ 'ticket_id': this.taskTicket }).then(response => {
        console.log('got check cmp status')
        console.log(response)
        if (response.code === 20000) {
          console.log(response.status)
          this.status_done = response.status.done
          this.$store.dispatch('dataCompare/taskDoneUpdate', response.status.done)
          this.$store.dispatch('dataCompare/cmpTaskResUpdate', response.res)
          console.log('Task has been done ' + this.taskTicket)
        }
      })
    },
    handleParallel() {
      if (this.multipleSelection.length === 0) {
        Message({
          message: '请至少选择一个数据集进行比对',
          type: 'warning',
          duration: 3 * 1000
        })
      } else {
        this.$notify({
          title: 'Info',
          message: '你总共选择了 ' + this.multipleSelection.length + ' 个数据集',
          type: 'info',
          duration: 500
        })
        this.datacmpSubmit.basePath = this.listQuery.basePath
        this.datacmpSubmit.cmpPath = this.listQuery.cmpPath
        this.datacmpSubmit.selectedDataset = this.multipleSelection
        this.editableInput = false
        getbatchCMPResult_parallel(this.datacmpSubmit).then(response => {
          console.log('got analyzed data from server')
          this.$store.dispatch('dataCompare/taskDoneUpdate', 0)
          console.log(response)
          if (response.code === 20000) {
            this.$notify({
              title: 'Success',
              type: 'success',
              message: '正在执行任务，合计' + response.totTask + '个任务',
              duration: 1500
            })
            this.$store.dispatch('dataCompare/taskTicketUpdate', response.ticket_id)
            this.$store.dispatch('dataCompare/cmptasknumUpdate', response.totTask)
            // 做一个递归调用
            const tempnum = parseInt(this.taskDone)
            console.log('调用递归函数，参数为：' + tempnum)
            this.getSecond(tempnum)
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

