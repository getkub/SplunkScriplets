package main

import (
	"fmt"
	"time"
)

func main() {
	fmt.Println("time", time.Now().Format("2006-01-02T15:04:05Z"))
	fmt.Println("time-5m", time.Now().Add(-5*time.Minute))
}
