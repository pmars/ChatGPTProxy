
## 由来

最近ChatGPT大火，我也去体验了一下，的确逻辑性极强，而且，我在工作中，遇到的一些技术问题，都可以在上面得到满意的回复。

鉴于ChatGPT针对大陆和香港的确进行了IP封锁，各种代理也是五花八门，但都有一些技术上的瓶颈

或是 需要ti子，或是需要账号的，用起来都不是很方便

本着，**解决不了问题，就绕过问题** 的准则，我没有花费大量的时间去研究国外的代理，转而找了一下国内的。

测试发现，国内很多名义上是ChatGPT，结果对接的都是GPT-3或者GPT-3.5的模型。

## 各种代理对比

+ [https://chat.forchange.cn/](https://chat.forchange.cn/) 这个就是典型的ChatGPT的页面，但调用的是GPT-3的接口
+ [https://ai.xingacgn.com/chatgpt.html](https://ai.xingacgn.com/chatgpt.html) 这个也是一个杂牌的GPT，而且不能多伦对话
+ [https://chatgptproxy.xyz](https://chatgptproxy.xyz) 这个的回复，应该是chatGPT，做表格，逻辑题都是很正确

## 代理 [https://chatgptproxy.xyz](https://chatgptproxy.xyz)

该项目，就是hack的[https://chatgptproxy.xyz](https://chatgptproxy.xyz)的接口，方便大家调用

具体的分析过程，可以参见：[analysis.md](analysis.md)

## Python

##### 单论对话

```python
def ask_questions():
    chat = ChatGPT("my_test_fake_id", False)  # 这里new的时候，提供一个union_id作为独立的账号识别码，请切换一个有特殊标识的字符串
    question_list = ["全世界一共多少个国家", "一个苹果有300克，一个梨400克，那么5个apple，2个pear，一共多少克", "中国最大的城市是哪里"]
    for q in question_list:
        if chat.send_question(q):
            answer, status = chat.get_result(True)
            print(answer, status)
        chat.reset_session()
    chat.close()
```

###### 输出

```javascript
# 根据联合国承认的主权国家数量，全世界目前有195个国家。但是这个数字不是固定的，因为有些地区存在争议，例如台湾、巴勒斯坦、西撒哈拉等，它们被某些国家承认为独立国家，但被其他国家视为是其他国家的一部分，因此这个数字可能会因政治、历史和其他因素而有所变化。 3
# 5个苹果的总重量为 5 x 300 = 1500 克。
# 2个梨的总重量为 2 x 400 = 800 克。
# 因此，5个苹果和2个梨的总重量为 1500 + 800 = 2300 克。 3
# 中国最大的城市是上海。 3
```

##### 多伦对话联动

```python
# 询问连续性的问题，前后逻辑有关联
def ask_multi_questions():
    chat = ChatGPT("my_test_union_id", True)  # my_test_union_id 这个需要你们改一下，AI******* 即可
    question_list = ["美国的领土面积排名在第几位", "巴西呢？", "那么第12的是谁"]
    for q in question_list:
        print("question:", q)
        if chat.send_question(q):
            answer, status = chat.get_result(True)
            print("answer:", answer)
    chat.close()
```

###### 输出

```javascript
# question: 美国的领土面积排名在第几位
# answer: 美国的领土面积排名第三，仅次于俄罗斯和加拿大。根据2021年世界银行数据，美国的领土面积为9,147,593平方千米。
# question: 巴西呢？
# answer: 巴西是世界上第五大国家，其领土面积为8,515,767平方千米。因此，巴西在领土面积排名中位居第五。
# question: 那么第12的是谁
# answer: 根据世界银行2021年的数据，领土面积排名第12的国家是阿根廷，其领土面积为2,780,400平方千米。
```

## 支援

欢迎有什么好的建议和项目，直接提一下

## 声明

公开这种代理，是为了大家更好的在其中学习和高效率的工作，请勿进行非法活动，您应该对自己的行为负责，一切责任与无我关

侵权必删