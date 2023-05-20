# 在本地运行版本2.3

## 安装python

1. 安装[anaconda]<https://www.anaconda.com/>配置python环境

2. 安装需要的包

   ```python
   pip install opencv-python	# opencv
   pip install tk						# tkinter
   pip install Pillow				# pillow
   pip install numpy					# numpy
   ```

## 在terminal中运行脚本

### 打开终端

- windows系统：右下角设置-> 输入terminal（终端）-> 打开
- MacOS：在程序坞中搜索terminal（终端）-> 打开

### 将路径设置到脚本所在位置

先回到根目录

```shell
cd
```

加载到解完压缩的文件夹（有python文件的位置）。右键选择“复制路径”得到文件夹 `xiaoyaoyou ver2_3` 内脚本所在位置。

```shell
cd "...(根据你的根目录决定)/xiaoyaoyou ver2_3"
```

### 运行目前版本

如果想查看803step：

```
python version_2_3_803.py
```

