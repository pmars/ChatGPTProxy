package chat_gpt

import (
	"context"
	"encoding/json"
	"io/ioutil"
	"math/rand"
	"net/http"
	"strings"
	"time"
)

const saGPTHost = "https://chatgptproxy.xyz"

// ChatGPT 每一轮对话，都需要new一个新的
type ChatGPT struct {
	userFakeId string
	sessionId  string
	parentId   string
	stopHeart  bool
}

type ChatQuestionResp struct {
	Code     int    `json:"code"`
	CodeMsg  string `json:"code_msg"`
	TraceId  string `json:"trace_id"`
	RespData struct {
		ChatId string `json:"chat_id"`
	} `json:"resp_data"`
}

type ChatAnswerResp struct {
	Code     int    `json:"code"`
	CodeMsg  string `json:"code_msg"`
	TraceId  string `json:"trace_id"`
	RespData struct {
		Answer string `json:"answer"`
		Status int    `json:"status"`
	} `json:"resp_data"`
}

func NewChatGPT(userFakeId string) *ChatGPT {
	chat := &ChatGPT{
		userFakeId: userFakeId,
		sessionId:  randomString(16),
		parentId:   "0",
	}

	go chat.startHeart()

	return chat
}

func (c *ChatGPT) Close(ctx context.Context) {
	c.stopHeart = true
}

func (c *ChatGPT) SendQuestion(ctx context.Context, question string) error {
	apiPath := "/api/v1/chat/conversation"
	bodyData := map[string]interface{}{
		"data": map[string]string{
			"user_fake_id": c.userFakeId,
			"session_id":   c.sessionId,
			"parent_id":    c.parentId,
			"question":     question,
		},
	}
	dataByte, _ := json.Marshal(bodyData)
	reader := strings.NewReader(string(dataByte))
	resp, err := http.Post(saGPTHost+apiPath, "application/json", reader)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	respBody, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return err
	}

	qRespData := ChatQuestionResp{}
	if err := json.Unmarshal(respBody, &qRespData); err != nil {
		return err
	}

	c.parentId = qRespData.RespData.ChatId
	return nil
}

func (c *ChatGPT) GetAnswer(ctx context.Context, wait bool) (answer string, status int) {
	if !wait {
		return c.getAnswer(ctx)
	}
	for {
		answer, status = c.getAnswer(ctx)
		if status != 1 {
			return
		}
		time.Sleep(time.Second)
	}
}

func (c *ChatGPT) getAnswer(ctx context.Context) (answer string, status int) {
	apiPath := "/api/v1/chat/result"
	bodyData := map[string]interface{}{
		"data": map[string]string{
			"user_fake_id": c.userFakeId,
			"session_id":   c.sessionId,
			"chat_id":      c.parentId,
		},
	}
	dataByte, _ := json.Marshal(bodyData)
	reader := strings.NewReader(string(dataByte))
	resp, err := http.Post(saGPTHost+apiPath, "application/json", reader)
	if err != nil {
		return "", 4
	}
	defer resp.Body.Close()

	respBody, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return "", 4
	}

	respData := ChatAnswerResp{}
	if err := json.Unmarshal(respBody, &respData); err != nil {
		return "", 4
	}

	return respData.RespData.Answer, respData.RespData.Status
}

func (c *ChatGPT) startHeart() {
	for {
		if c.stopHeart {
			return
		}

		apiPath := "/api/v1/chat/heart"
		bodyData := map[string]interface{}{
			"data": map[string]string{
				"user_fake_id": c.userFakeId,
				"session_id":   c.sessionId,
			},
		}
		dataByte, _ := json.Marshal(bodyData)
		reader := strings.NewReader(string(dataByte))
		_, _ = http.Post(saGPTHost+apiPath, "application/json", reader)

		time.Sleep(time.Second * 10)
	}
}

func randomString(l int) string {
	bytes := []byte("ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678")

	result := make([]byte, l)
	r := rand.New(rand.NewSource(time.Now().UnixNano()))
	for i := 0; i < l; i++ {
		result[i] = bytes[r.Intn(len(bytes))]
	}
	return string(result)
}
