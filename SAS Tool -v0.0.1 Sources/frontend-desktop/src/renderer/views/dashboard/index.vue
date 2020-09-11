<template>
  <div class="dashboard-container">
    <el-row :gutter="8">
      <el-col :xs="{span: 30}" :sm="{span: 20}" :md="{span: 20}" :lg="{span: 10}" :xl="{span:10}" style="margin-bottom:30px;">
        <todo-list />
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import TodoList from '@/components/TodoList'

export default {
  name: 'dashboard',
  components: {
    TodoList
  },
  computed: {
    ...mapGetters([
      'name'
    ])
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}
</style>
