# 这个文件是用来测试一些不确定的代码的

a = {"a": 1, "b": 2}
b = a
del a["a"]
print(a)
print(b)