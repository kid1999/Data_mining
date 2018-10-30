import jieba
str = '小明特别喜欢读书，天天读书，除了读书就是吃饭睡觉。'
list = jieba.cut(str)
print("/".join(list))           #join方法 通过某个字符 把两个字符串连在一起