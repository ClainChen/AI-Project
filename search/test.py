# 这个文件是用来测试一些不确定的代码的

a = {"a": 1, "b": 2}
b = [("a", 1), ("a", 2), ("a", 3)]
b.sort(key= lambda x: x[1], reverse=True)
print(b)
