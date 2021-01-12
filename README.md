## QingCloud CLI
[toc]
> 通过青云iaas api实现创建主机(RunInstances)，获取主机(DescribeInstances)，销毁主机(TerminateInstances)的命令行接口。


### 环境
```
python2.7+

```


### 安装

```
git clone https://github.com/chseng213/QingCloudTest.git
cd QingCloudTest
pip install -r requirements.txt
pip install --editable .
```
**注意**
如果你的python是通过source code编译安装的   

请使用你安装路径下的python解释器进行对cli程序的编译和安装 
 
例如 python安装地址为:/usr/local/python37
```
/usr/local/python37/bin/pip install -r requirements.txt
/usr/local/python37/bin/pip install --editable .
```
**或者使用软链将你安装的python软链至/usr/bin/中**



### 命令行补全激活
#### For Bash:
```
eval "$(_QC_CLI_COMPLETE=source_bash qc-cli)"

```

#### For Zsh:
```
eval "$(_QC_CLI_COMPLETE=source_zsh  qc-cli)"

```

#### For Fish:
```
eval "$(_QC_CLI_COMPLETE=source_fish   qc-cli)"

```

### 使用
#### 编辑配置文件
程序配置文件默认为项目目录下config.py,必须包含三个参数`qy_access_key_id`,`qy_secret_access_key` 和`zone`  
内容如下
```
qy_access_key_id='YOUR-ACCESS-KEY'
qy_secret_access_key='YOUR-SECRET-ACCESS-KEY'
zone='sh1'  
```
或者使用 -f 指定配置文件
```
qc-cli -f /etc/qingcloud/config.ini
```

#### 创建主机(RunInstances)
>在command后输入  `--help` 可查看帮助 `qc-cli run-instances --help`  
必填参数有`image_id`,`login_mode`,程序中未包含但是api中可以传的参数请使用`-J`输入json格式字符串,api参数信息详细[API](<https://docs.qingcloud.com/product/api/>)  
*其中json参数会被简单的校验,当参数不是当前api的参数则会被过滤*

示例:
```
qc-cli run-instances 'centos56x64' 'passwd' -p qweW123142 -C 1 -M 1024 -J '{"invalid-key1":233,"invalid-key1":2,"os_disk_size":30}'
```

结果输出:
```
{"job_id":"j-p8q9cbk6wss","eips":null,"ret_code":0,"instances":["i-emhiicz8"],"volumes":null,"action":"RunInstancesResponse"}
```

#### 获取主机(DescribeInstances)
>在command后输入  `--help` 可查看帮助 `qc-cli describe-instances --help`  
所有参数均为非必填,默认最多返回20条主机信息  
需要指定多个image_id或者多种instance_type时可以多次传参

示例:
```
qc-cli describe-instances -m centos64x86a -m centos56x64
```

结果输出
```
{"action":"DescribeInstancesResponse","instance_set":[],"total_count":0,"ret_code":0}

```

#### 销毁主机(TerminateInstances)
> 在command后输入  `--help` 可查看帮助 `qc-cli terminate-instances --help`  
必须传入实例id,可指定多个实例id

示例:
```
qc-cli terminate-instances -i  i-9ktshcem
```

结果输出
```
{"action":"TerminateInstancesResponse","job_id":"j-nbsyspqu8rh","ret_code":0}
```