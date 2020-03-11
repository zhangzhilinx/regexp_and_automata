# regexp_and_automata
Compilation Principles Course Design: Implement a simple regex and automaton





## 特性

### 常规特性
* 正规表达式 -> NFA
    * 支持的符号：+ ? * | ()
* NFA -> DFA
* 最小化DFA
    - 实现了清除无效状态：通过染色算法与BFS
    - 实现了等价状态简化
* 经过大多数测试已无问题，部分测试位于单元测试文件中

### GUI方面
* Qt5可视化图形界面
* 客制化GraphView，便于可视化查看自动机状态
    - 自动缩放到较为合适的图像大小





## 细节

解析文法：

```
regex'   = regex $
regex    = term [|] regex
		 | term
term     = factor term
		 | factor
factor   = unit [*]
		 | unit [+]
		 | unit [?]
		 | unit
unit     = ( regex )
		 | char
```

但该文法实现中存在一个已知缺陷：无法解析空串和空括号对





## 测试

测试用例：

```
(a|b)+
(0+1)*
(a+|b)cd
	-> abcd aabcd cd bcd aacdf abcdg
(b+(a(b*)))
1(0|1)*010
(a|b)*abb
	-> sabbaabbxabb
((ab|a)(b(c?)d|c))(d*)
	-> cabbabbcddddabbcdddddabbdabbcd / abbcddddabbcdddddabbdabbcd
(a|b)*(ab|ba)
a b & a | b c ? d & & c | & d * &
a b & a | b c ? d & & c | & d * &
```





## 缺陷

* 正则表达式*（子集实现）*
  * 目前尚不支持.符号
  * 目前尚不支持转义
  * 目前尚不支持解析空串与空括号对

