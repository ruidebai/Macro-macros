<template>
    <el-table :data="cmpDiff_Detail"
        :row-style="{height:0+'px'}"
        :cell-style="{padding:0+'px'}"
    >
        <el-table-column property="Column" label="变量名" ></el-table-column>
        <el-table-column property="Max_Diff" label="最大差异" ></el-table-column>
        <el-table-column property="Null_Diff" label="无差异"></el-table-column>
        <el-table-column property="UnEQ" label="不等观测数"></el-table-column>
    </el-table>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  data() {
    return {
    }
  },
  computed: {
    ...mapGetters(['cmpDiff_Detail'])
  },
  methods: {
  }
}
</script>