<template>
  <div class='app-container' >
    <transition name="my">
      <div v-show="resNum === 0">
        <i class="el-icon-loading" style="margin:0 15px 0 15px" /> 没有SAS日志分析任务被执行，未获取到分析结果 
      </div>
    </transition>
    <div class="main" v-show="resNum>0">
      <div class="summary-container"  align="center">
        <el-alert :closable="false" style="width:200px;display:inline-block;vertical-align: middle;margin-bottom:30px;" title="日志分析汇总信息" type="success" />
        <el-table
      :data="logSummary"
      :row-style="{height:5+'px'}"
      :cell-style="{padding:5+'px'}"
      :show-header="false"
      style="width: 55%"
      border
      border-radius:4px
      highlight-current-row
    >
        <el-table-column  min-width="15%" align="center" >
          <template slot-scope="scope">
              {{ scope.row.item }}
          </template>
        </el-table-column>
        <el-table-column align="center" prop="created_at"  min-width="40%">
          <template slot-scope="scope">
              <span>{{ scope.row.detail }}</span>
          </template>
        </el-table-column>
        </el-table>
      </div>
      <el-alert :closable="false" center style="width:100%;margin-top:10px;margin-bottom:10px;" title="PART II" type="success" /> 
      <div class="detail-container" align="center">
        <el-table
      :data="issueDetials"
      :row-style="{height:5+'px'}"
      :cell-style="{padding:5+'px'}"
      border
       style="width: 100%"
      border-radius:4px
      highlight-current-row
    >
        <el-table-column   min-width="20%" label="日志名称" align="left" >
          <template slot-scope="scope">
             {{ scope.row.logName }} 
          </template>
        </el-table-column>
        <el-table-column align="left"  label="错误名称" >
          <template slot-scope="scope">
              {{ scope.row.errName }}
          </template>
        </el-table-column>
        <el-table-column
          fixed="right"
          label="操作"
          width="100">
          <template slot-scope="scope">
            <el-button @click="handleViewClick(scope.row)" type="info" >查看</el-button>
          </template>
        </el-table-column>
        </el-table>
      </div>
      <el-alert :closable="false" center style="width:100%;margin-top:10px;margin-bottom:10px;" title="End of report" type="success" />       
      <el-dialog title="日志详情" :visible.sync="dialogFormVisible">
        <p v-for="(item, index) in  errcontent" :key= 'index' v-html="item" :visible="dialogFormVisible">{{ item  }}</p>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">
          Cancel
        </el-button>
      </div>
    </el-dialog>
    </div>
  </div>
</template>

<style>
       进入前和结束后的状态
    .my-enter,.my-leave-to{
        opacity: 0;
        transform: translateX(80px);
    }
    进入和离开的动画时间段
    .my-enter-active,.my-leave-active{
        
        transition: all 0.5S ease
    }
</style>

<script>
import store from '@/store'
import { mapGetters } from 'vuex'
import { getLogblock } from '@/api/log'
export default {
  name: 'Logresult',
  store: store,
  data() {
    return {
      gotRes: false,
      logWithERR: undefined,
      logDetials: [],
      dialogFormVisible: false,
      temp: {
        errName: undefined,
        errIndex: undefined,
        fullpath: ''
      },
      errcontent: []
    }
  },
  computed: {
    ...mapGetters(['resNum', 'logSummary', 'logwithIssue', 'issueDetials'])
  },
  activated() {
    console.log('enter into log result display page, actived!')
    console.log(this.$store.getters.logresult)
  },
  methods: {
    handleViewClick(row) {
      console.log(row.fullpath)
      this.temp = Object.assign({}, row)
      console.log(this.temp)
      this.getErrDetails(this.temp.fullpath, this.temp.errIndex)
      this.dialogFormVisible = true
    },
    getErrDetails(path, errName) {
      console.log('method has been called \n ' + path + errName)
      const param = {
        fullpath: path,
        errIndex: errName
      }
      console.log(param)
      getLogblock(param).then(response => {
        //  response.data.logBlock
        // console.log(response.data.logBlock)
        this.errcontent = response.data.logBlock
        console.log(this.errcontent)
        setTimeout(() => {
        }, 2 * 1000)
      })
    }
  }
}
</script>
