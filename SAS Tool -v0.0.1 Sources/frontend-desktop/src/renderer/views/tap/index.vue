<template>
  <el-tabs v-model="activeName" @tab-click="handleClick">
    <el-tab-pane  name="first">
      <span slot="label">
             <i class="el-icon-search" style="margin:0 80px 0 80px">
                 <span style="padding-left: 8px">日志扫描</span>
             </i>
         </span>
      <keep-alive>
        <child1 />
      </keep-alive>
    </el-tab-pane>
    <el-tab-pane  name="second">
       <span slot="label">
             <i class="el-icon-info" style="margin:0 80px 0 80px">
                 <span style="padding-left: 8px">扫描结果 <el-badge :value="resNum" /></span>
             </i>
         </span>
      <keep-alive>
        <child2 />
      </keep-alive>
    </el-tab-pane>
  </el-tabs>
</template>
<script>
import TabPane from './components/TabPane'
import logresultDisplay from './components/logresultDisplay'
import { mapGetters } from 'vuex'
export default {
  name: 'Tab',
  components: {
    child1: TabPane,
    child2: logresultDisplay
  },
  data() {
    return {
      activeName: 'first',
      num: 0
    }
  },
  computed: {
    ...mapGetters(['resNum'])
  },
  methods: {
    handleClick(tab, event) {
      console.log('did this method been excuted?')
      console.log(tab, event)
    }

  }
}
</script>

<style scoped>
  .tab-container {
    margin: 10px;
  }
</style>
