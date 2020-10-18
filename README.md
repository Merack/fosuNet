### fosuNet
a simple Python script for fosu network  

![2020_1006_1601970034.png](https://i.loli.net/2020/10/06/qglPIb8rzJD4Lpo.png)
### usage
```
pip install -r requirements.txt
python main.py
```
### download
(推荐) [https://gitee.com/Merack/fosuNet/releases](https://gitee.com/Merack/fosuNet/releases)  
 [https://github.com/Merack/fosuNet/releases](https://github.com/Merack/fosuNet/releases)  

### tips
1. 目前本脚本仅在仙溪校区校园网测试, 其他校区情况未知  
2. 你可以通过修改位于软件目录下的/config/config来更改登陆信息
3. 为没有安装Python环境的windows用户打包了一个可以直接运行的成品, 下载release页面下fosuNet.zip,解压后运行fosuNet.exe即可   
release页面(github): [https://github.com/Merack/fosuNet/releases](https://github.com/Merack/fosuNet/releases)  
release页面(gitee)(推荐): [https://gitee.com/Merack/fosuNet/releases](https://gitee.com/Merack/fosuNet/releases)
4. 如果你下载了我打包好的成品并解压, 可以找到 fosuNet.exe->右键->发送快捷方式到桌面 来快捷地找到并使用本程序

### 自行打包成exe文件
如果你不想使用release页面下我打包好的程序, 可以自行打包  
需要这注意的是,此项操作需要Python环境  
1. 安装pyinstaller
```
pip install pyinstaller
```
2. 生成spec文件
```
pyi-makespec -n fosuNet main.py
```
3. 修改spec文件将config添加进打包目录
使用编辑器打开目录下生成的`fosuNet.spec`, 修改字段  
```
datas=[],
```
为  
```
datas=[('config', 'config')],
```
4. 打包成exe
```
pyinstaller fosuNet.spec
```  
更多使用方法请参照pyinstaller的官方文档

### 致谢
测试人员: [小叶](https://github.com/yez78), 徐轩
