package main

import (
	"ChatGPTProxy/go/chat_gpt"
	"context"
	"fmt"
	"time"
)

func main() {

	chat := chat_gpt.NewChatGPT("my_test_union_id")
	if err := chat.SendQuestion(context.Background(), "你好，可以给我推荐一本经济学的常识书么"); err == nil {
		for {
			answer, status := chat.GetAnswer(context.Background(), false)
			fmt.Println(status, answer)
			if status != 1 {
				break
			}
			time.Sleep(time.Second)
		}
	}
	chat.Close(context.Background())
}
