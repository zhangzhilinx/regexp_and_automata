# regexp_and_automata
Compilation Principles Course Design: Implement a simple regex and automaton


## 特性
### 常规特性
* 正规表达式 -> NFA
* NFA -> DFA
* 最小化DFA
    - 实现了清除无效状态：通过染色算法与BFS
    - 实现了等价状态简化
* 经过大多数测试已无问题，部分测试位于单元测试文件中

### GUI方面
* Qt5可视化图形界面
* 客制化GraphView，便于可视化查看自动机状态
    - 自动缩放到较为合适的图像大小
