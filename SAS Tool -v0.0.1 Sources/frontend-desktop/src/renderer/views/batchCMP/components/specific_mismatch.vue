<template>
    <el-table :data="sepcific_diff"
      :row-style="{padding:5+'px'}"
      :cell-style="{padding:5+'px'}"
      :show-header="false"
      width="100%"
    >
        <el-table-column  label="行号" min-width="10%" >        
          <template slot-scope="scope">
            <span v-if="scope.row.index=== '-1'"><el-tag effect="dark">观测</el-tag></span>
            <span v-else>{{ scope.row.index }} </span>           
          </template>
        </el-table-column>
        <el-table-column  label="BASE" min-width="45%">
          <template slot-scope="scope">
            <span v-if="scope.row.index=== '-1'" style="color: blue"><el-tag type="info" effect="dark">{{ scope.row.col1 }}</el-tag></span>
            <span v-else>{{ scope.row.col1 }} </span>           
          </template>
        </el-table-column>
        <el-table-column  label="CMPARE" min-width="45%">
          <template slot-scope="scope">
            <span v-if="scope.row.index=== '-1'" style="color: blue"><el-tag type="info" effect="dark">{{ scope.row.col2 }}</el-tag></span>
            <span v-else>{{ scope.row.col2 }} </span>           
          </template>
        </el-table-column>
    </el-table>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  computed: {
    ...mapGetters(['sepcific_diff'])
  },
  methods: {
  }
}
</script>