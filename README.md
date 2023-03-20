# AI-Project 更新日志

### 3.20：

- 加入了测试用主程序

- 加入了文件读取功能和判断文件路径功能

### 3.21

- 加入了Expand Cells 的算法，已完成debug测试
- 就是将cell分别往六个方向扩散后得到的新gameBoard（都是dict[tuple, tuple]）储存在list中，然后返回list的一个function
- 加入了往某一个方向移动一格的逻辑
- 加入了移动方向和对应坐标增减的字典