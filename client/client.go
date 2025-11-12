package main

import (
	"encoding/json"
	"fmt"
	"time"

	zmq "github.com/pebbe/zmq4"
)

func nowISO() string {
	return time.Now().UTC().Format("2006-01-02T15:04:05Z")
}

func sendRequest(service string, data map[string]interface{}) (map[string]interface{}, error) {
	socket, err := zmq.NewSocket(zmq.REQ)
	if err != nil {
		return nil, err
	}
	defer socket.Close()

	// connect to the python server (docker-compose service name "server")
	if err := socket.Connect("tcp://server:5555"); err != nil {
		return nil, err
	}

	msg := map[string]interface{}{
		"service": service,
		"data":    data,
	}
	b, _ := json.Marshal(msg)
	if _, err := socket.SendBytes(b, 0); err != nil {
		return nil, err
	}

	replyBytes, err := socket.RecvBytes(0)
	if err != nil {
		return nil, err
	}

	var reply map[string]interface{}
	if err := json.Unmarshal(replyBytes, &reply); err != nil {
		return nil, err
	}
	return reply, nil
}

func main() {
	fmt.Println("💬 BBS Client (Go) starting...")

	// 1) login
	loginData := map[string]interface{}{"user": "client_go_user", "timestamp": nowISO()}
	if r, err := sendRequest("login", loginData); err == nil {
		fmt.Println("Login reply:", r)
	} else {
		fmt.Println("Login error:", err)
	}

	time.Sleep(300 * time.Millisecond)

	// 2) users
	if r, err := sendRequest("users", map[string]interface{}{"timestamp": nowISO()}); err == nil {
		fmt.Println("Users reply:", r)
	} else {
		fmt.Println("Users error:", err)
	}

	time.Sleep(300 * time.Millisecond)

	// 3) create channel
	if r, err := sendRequest("channel", map[string]interface{}{"channel": "geral", "timestamp": nowISO()}); err == nil {
		fmt.Println("Channel create reply:", r)
	} else {
		fmt.Println("Channel create error:", err)
	}

	time.Sleep(300 * time.Millisecond)

	// 4) list channels
	if r, err := sendRequest("channels", map[string]interface{}{"timestamp": nowISO()}); err == nil {
		fmt.Println("Channels reply:", r)
	} else {
		fmt.Println("Channels error:", err)
	}

	fmt.Println("Client finished.")
}
