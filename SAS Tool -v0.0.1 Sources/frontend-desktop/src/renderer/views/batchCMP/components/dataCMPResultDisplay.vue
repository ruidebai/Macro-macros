<template>
  <div class='app-container' >
    <div v-show="cmptasknum === 0" style="width:100%;margin-top:20px;"><i class="el-icon-loading" style="margin:0 15px 0 15px" /> 没有SAS数据集对比任务被执行，无法获取到任何对比结果 </div>
    <div class="main" v-show="cmptasknum > 0">
      <div class="summary-container"  align="center">
        <el-alert :closable="false" style="width:250px;display:inline-block;vertical-align: middle;margin-bottom:20px;" title="SAS数据集Compare汇总信息" type="success" />
        <el-table
      :data="dataCMPSummary"
      :row-style="{height:5+'px'}"
      :cell-style="{padding:5+'px'}"
      :show-header="false"
      style="width: 55%"
      border
      border-radius:4px
      highlight-current-row
    >
        <el-table-column  min-width="20%" align="left" >
          <template slot-scope="scope">
              {{ scope.row.item }}
          </template>
        </el-table-column>
        <el-table-column align="center" prop="created_at" min-width="20%">
            <template slot-scope="scope">
              <span>{{ scope.row.detail }}</span>
            </template>
        </el-table-column>
        </el-table>
      </div>
      <el-alert :closable="false" center style="width:100%;margin-top:10px;margin-bottom:10px;" title="PART II" type="success" /> 
      <div class="detail-container" align="center">
        <el-table
        :data="cmpRES_1"
      :row-style="{height:5+'px'}"
      :cell-style="{padding:5+'px'}"
      :header-cell-style="tableHeaderColor"
      border
       style="width: 100%"
      border-radius:4px
      highlight-current-row
    >
        <el-table-column   min-width="25%" label="比较任务名称" align="center" >
          <template slot-scope="scope">
            <el-popover trigger="hover" placement="bottom">
            <p>基准数据集路径:  {{ scope.row.base }} </p>
            <p>比较数据集路径:  {{ scope.row.cmp }} </p>
            <div slot="reference" >
              {{ scope.row.result.setSMRY[0]['DataSet'][0]}}  <i class="el-icon-star-on" style="margin:0 15px 0 15px" />
              {{ scope.row.result.setSMRY[0]['DataSet'][1]}}
            </div>
            </el-popover>
          </template>
        </el-table-column>
        <el-table-column align="center"    label="观测汇总" >
          <el-table-column align="center"  min-width="25%" label="进行对比的观测总数">
            <template slot-scope="scope">
              {{ scope.row.result.obsSMRY[0]['matchedObs'] }}
            </template>
          </el-table-column>
          <el-table-column align="center" min-width="25%" label="完全匹配的观测数">
            <template slot-scope="scope">
              {{ scope.row.result.obsSMRY[1]['fullmatchedObs'] }}
            </template>
          </el-table-column>
          <el-table-column align="center" min-width="25%" label="未匹配的观测数">
            <template slot-scope="scope">
              {{ scope.row.result.obsSMRY[2]['partunmatchedObs'] }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column align="center"  label="数据集汇总" >
          <el-table-column align="center" min-width="25%"  label="变量数对比" >
            <template slot-scope="scope">
              <el-popover trigger="hover" placement="bottom">
                <p>基准数据集:  {{ scope.row.result.setSMRY[1]['Variables'][0] }} 个变量 </p>
                <p>比较数据集:  {{ scope.row.result.setSMRY[1]['Variables'][1] }}  个变量</p>
              <div slot="reference" >
                {{ scope.row.result.setSMRY[1]['Variables'][0] }}<i class="el-icon-star-on" style="margin:0 15px 0 15px" /> {{ scope.row.result.setSMRY[1]['Variables'][1]}}
              </div>
              </el-popover>
            </template>
          </el-table-column>
         <el-table-column align="center"  min-width="25%" label="观测数对比" >
            <template slot-scope="scope">
              <el-popover trigger="hover" placement="bottom">
                <p>基准数据集:  {{ scope.row.result.setSMRY[2]['Observations'][0] }} 个观测 </p>
                <p>比较数据集:  {{ scope.row.result.setSMRY[2]['Observations'][1] }}  个观测</p>
              <div slot="reference" >
                {{ scope.row.result.setSMRY[2]['Observations'][0] }}<i class="el-icon-star-on" style="margin:0 15px 0 15px" /> {{ scope.row.result.setSMRY[2]['Observations'][1]}}
              </div>
              </el-popover>
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column align="center"  label="变量汇总" >
         <el-table-column align="center" min-width="25%"  label="同时存在的变量数" >
            <template slot-scope="scope">
              {{ scope.row.result.varSMRY[0]['coexisted'] }}
            </template>
          </el-table-column>
          <el-table-column align="center" min-width="25%"  label="变量差异" >
          <el-table-column align="center" min-width="30%"  label="仅在Base数据集中存在的变量" >
            <template slot-scope="scope">
              {{ scope.row.result.varSMRY[1]['varNumDiff'][0].join(',') }}
            </template>
          </el-table-column>
          <el-table-column align="center" min-width="30%"  label="仅在CMP数据集中存在的变量" >
            <template slot-scope="scope">
              {{ scope.row.result.varSMRY[1]['varNumDiff'][1].join(',') }}
            </template>
          </el-table-column>
          </el-table-column>
        </el-table-column>        
        <el-table-column
          align="center"
          label="操作"
          width="100">
          <template slot-scope="scope">
            <el-button @click="handleViewClick(scope.row)" type="info" >查看</el-button>
          </template>
        </el-table-column>
        </el-table>
      </div>
            <el-alert :closable="false" center style="width:100%;margin-top:10px;margin-bottom:10px;" title="End of report" type="success" />      
      <el-dialog  :visible.sync="dialogFormVisible" >
        <template v-slot:title>
            <h2 style="color:lightblue;width:100%;display:inline-block;vertical-align: middle;horizontal-align: middle;margin-bottom:30px;"> {{detail_title }}</h2>
        </template>
        <el-tabs v-model="activeName" @tab-click="handleClick"  style="margin:0 5px 0 5px" >
          <el-tab-pane  name="first">
            <span slot="label">
              <span style="padding-left: 8px">变量差异统计</span>
            </span>
            <keep-alive>
              <child1 />
            </keep-alive>
        </el-tab-pane>
        <el-tab-pane  name="second">
          <span slot="label">
            <span style="padding-left: 8px">变量差异详情 </span>
          </span>
          <keep-alive>
            <child2 />
          </keep-alive>
        </el-tab-pane>
      </el-tabs>
      <div slot="footer" class="dialog-footer" >
        <el-button @click="dialogFormVisible = false">
          Cancel
        </el-button>
      </div>
    </el-dialog>
    </div>
  </div>
</template>

<script>
import store from '@/store'
import { mapGetters } from 'vuex'
import { getSingle_CMP_Detials } from '@/api/sasdataset'
import diff_detail from './diff_detail'
import specific_mismatch from './specific_mismatch'
export default {
  name: 'Logresult',
  store: store,
  components: {
    child1: diff_detail,
    child2: specific_mismatch
  },
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
      errcontent: [],
      detail_title: '数据集对比结果详情',
      activeName: 'first'
    }
  },
  computed: {
    ...mapGetters(['cmptasknum', 'dataCMPSummary', 'cmpRES_1', 'cmpDiff_Detail', 'query_cache'])
  },
  activated() {
    console.log('enter into data compare result display page, actived!')
  },
  methods: {
    handleViewClick(row) {
      console.log(row.base + '----' + row.cmp)
      this.temp = Object.assign({}, row)
      console.log(this.temp)
      // 如果 相同的参数请求过一次，就缓存起来，下次请求相同参数就使用缓存，而不再去重复请求，减小消耗
      if ((this.query_cache.t_base === this.temp.base) && (this.query_cache.t_cmp === this.temp.cmp)) {
        console.log('exactly the same, read data from cache')
      } else {
        this.getErrDetails(this.temp.base, this.temp.cmp)
      }
      this.detail_title = this.temp.base + ' 与 ' + this.temp.cmp + '对比结果详情'
      this.dialogFormVisible = true
    },
    getErrDetails(bpath, cpath) {
      console.log('method has been called \n ' + bpath + cpath)
      const param = {
        base: bpath,
        cmp: cpath
      }
      console.log(param)
      this.$store.dispatch('dataCompare/dataCMP_QUERY_CACHE_UPDATE', { 't_base': param.base, 't_cmp': param.cmp })
      getSingle_CMP_Detials(param).then(response => {
        this.errcontent = response.res
        this.$store.dispatch('dataCompare/dataCMP_DIFF_DETAIL_PUSH', response.res)
        this.$store.dispatch('dataCompare/dataCMPSpecificDiffPush', response.details)
        setTimeout(() => {
        }, 2 * 1000)
      })
    },
    // 更改表头样式
    tableHeaderColor({ row, column, rowIndex, columnIndex }) {
      if (column.label === '变量汇总') {
        return 'background-color: lightblue;color: white;font-weight: 700;'
      } else if (column.label === '观测汇总') {
        return 'background-color: lightgreen;color: white;font-weight: 700;'
      } else if (column.label === '数据集汇总') {
        return 'background-color: lightred;color: black;font-weight: 700;'
      }
    },
    handleClick(tab, event) {
      console.log('did this method been excuted?')
      console.log(tab, event)
    }
  }
}
</script>
