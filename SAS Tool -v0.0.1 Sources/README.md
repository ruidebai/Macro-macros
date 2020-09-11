## 使用方法

### 启动后端

在pycharm的命令行安装所有的包

建议使用虚拟环境

```python
// 使用pip安装所有的依赖
pip install -r requirements.txt
// 如果某个依赖无法安装上去，可能是因为网络的问题， 此时建议使用手动安装 命令如下 手动安装uvicorn==0.11.8
// uvicorn==0.11.8 表示安装uvicorn这个模块的0.11.8 这个版本
pip install -i http://mirrors.aliyun.com/pypi/simple/ uvicorn==0.11.8 --trusted-host mirrors.aliyun.com
```



### 启动前端服务

使用vscode 打开项目，新建一个终端

```js
// 安装所有的依赖
npm  install
// 如果网络较差也可以先安装cnpm（npm在中国的镜像）
npm install -g cnpm --registry=https://registry.npm.taobao.org
// 然后执行
cnpm install 
// 启动服务
npm run dev
// 打包为exe
npm run-script build
```

