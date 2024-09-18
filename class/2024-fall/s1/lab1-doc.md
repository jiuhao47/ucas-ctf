# Lab1
## apt源

google bing 

Ubuntu 22.04 apt 换源

Linux

Ubuntu 22.04(24.04)

Arch 

Debian

CentOS

```bash
root
sudo

cp /etc/apt/sources.list /etc/apt/sources.list.bak 

/etc/apt/sources.list

sudo apt update

sudo apt install ...
```
## 目录与文件
```bash
mkdir
cd 
pwd
ls
touch
cp
mv
rm
cat
less
hexdump/xxd
```

### 更多参数

```bash
# ls
ls -al
# -l 显示详细信息
ls -l
# -a 显示所有文件
ls -a

# cp
# -r 递归复制
cp -r ...
# -i 覆盖前询问
cp -i ...
# -f 强制覆盖
cp -f ...

# mv
# -i 覆盖前询问
mv -i ...
# -f 强制覆盖
mv -f ...

# rm
# -r 递归删除
rm -r ...
# -f 强制删除
rm -f ...
# -i 删除前询问
rm -i ...

```

### 随堂测试1
尝试创建目录lab1和lab1.bak，其均拥有如下的目录结构
```
.
├── bin
├── doc
│   └── lab1-doc.md
├── misc
└── src
    ├── fib.py
    └── hello.c
```

## 用户与权限
```bash
# 用户
whoami
# 用户与组
id
# 模拟root登陆
sudo -i
# 更改文件、文件夹权限
chmod
# 更改文件、文件夹所有者
chown
# 更改文件、文件夹所属组
chgrp
```

### 随堂测试2
查看上一个任务创建的目录的权限，并尝试对lab1.bak更改权限（000 ... 700），观察不同权限下

```
ls lab1.bak
cd lab1.bak
touch ./lab1.bak/test.txt
```

上述命令的执行情况，思考原因。

然后将lab1.bak文件夹重命名为lab1.abandon，删除lab1.abandon文件夹

## shell
```bash
sh
bash
# zsh
```

## 重定向与管道
```bash
# 重定向
# > 覆盖
echo "hello" > hello.txt
# >> 追加
echo "world" >> hello.txt
# < 输入
cat < hello.txt
# | 管道
ls | grep "hello"
cat | less
```

## 编辑
```bash
# vim
vim
# normal
:q
:q!
:w <file_name>
i
v
# insert
# Esc 退出
# visual

# nano
nano
# Ctrl + O save
# Ctrl + X exit
# Ctrl + G help
```

## 编译与运行

### 解释型语言
```bash
#!/bin/bash
echo "hello world"
```
```python
#!/usr/bin/python3
print("hello world")
```

指定解释器后，需要给文件执行权限
```bash
chmod +x hello.sh
chmod +x hello.py
./hello.sh
./hello.py
```
### 编译型语言
```c
#include <stdio.h>
int main() {
    printf("hello world\n");
    return 0;
}
```

编译型语言需要编译后运行
```bash
gcc hello.c -o <output_file path>
```

### 随堂测试3

完成上述三个程序的编写，保存在lab1的src目录下，分别命名为hello.sh, hello.py, hello.c，然后编译运行hello.c，二进制可执行文件命名为hello，存放在lab1的bin目录下。


