# -*- coding: utf-8 -*-

from chat_gpt import *

# ask_questions output like this
# 根据联合国承认的主权国家数量，全世界目前有195个国家。但是这个数字不是固定的，因为有些地区存在争议，例如台湾、巴勒斯坦、西撒哈拉等，它们被某些国家承认为独立国家，但被其他国家视为是其他国家的一部分，因此这个数字可能会因政治、历史和其他因素而有所变化。 3
# 5个苹果的总重量为 5 x 300 = 1500 克。
# 2个梨的总重量为 2 x 400 = 800 克。
# 因此，5个苹果和2个梨的总重量为 1500 + 800 = 2300 克。 3
# 中国最大的城市是上海。 3

# 测试询问问题，无需多伦回复，每个问题，只要有答案即可
def ask_questions():
    chat = ChatGPT("my_test_union_id", False)  # 这里new的时候，提供一个union_id作为独立的账号识别码，请切换一个有特殊标识的字符串
    question_list = ["全世界一共多少个国家", "一个苹果有300克，一个梨400克，那么5个apple，2个pear，一共多少克", "中国最大的城市是哪里"]
    for q in question_list:
        if chat.send_question(q):
            answer, status = chat.get_result(True)
            print(answer, status)
        chat.reset_session()
    chat.close()


# ask_multi_questions output like this
# question: 美国的领土面积排名在第几位
# answer: 美国的领土面积排名第三，仅次于俄罗斯和加拿大。根据2021年世界银行数据，美国的领土面积为9,147,593平方千米。
# question: 巴西呢？
# answer: 巴西是世界上第五大国家，其领土面积为8,515,767平方千米。因此，巴西在领土面积排名中位居第五。
# question: 那么第12的是谁
# answer: 根据世界银行2021年的数据，领土面积排名第12的国家是阿根廷，其领土面积为2,780,400平方千米。

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


if __name__ == '__main__':
    # ask_questions()

    ask_multi_questions()

    print("all test done. quit now...")

