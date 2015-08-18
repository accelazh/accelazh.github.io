---
layout: post
title: "Goroutine can Race"
tagline : "Goroutine can Race"
description: "Goroutine can Race"
category: "go"
tags: [go, concurrency, language]
---
{% include JB/setup %}

### When does Goroutine Switch?

First, I want to test whether goroutine can switch in busy cpu loop. Here's my program (I'm using go 1.4.2). The two sleep_print goroutines keep switching between print and sleep. On default [GOMAXPROCS](http://stackoverflow.com/questions/6235317/why-doesnt-the-go-statement-execute-in-parallel) should be 1 which means all my goroutines run on one core only.

```
// File name test.go
package main

import (
    "fmt"
    "time"
    "sync"
)

func take_cpu(d time.Duration) {
    start := time.Now()
    count := 0
    for time.Now().Sub(start) < d {
        for i := 0; i < 1000 * 1000; i++ {}
        count++
    }
}

func sleep_print(tag string, count int, wg *sync.WaitGroup) {
    defer wg.Done()
    for i := 0; i < count; i++ {
        fmt.Println(tag, ":", i)
        time.Sleep(1 * time.Second)
        // take_cpu(1 * time.Second)
    }
}

func main() {
    var wg sync.WaitGroup
    
    wg.Add(1)
    go sleep_print("SP1", 10, &wg)
    fmt.Println("Launched SP1")
    wg.Add(1)
    go sleep_print("SP2", 10, &wg)
    fmt.Println("Launched SP2")

    wg.Wait()
    fmt.Println("Done")
}
```

Running it gives below results. As expected, goroutines can switch. It maybe because I use time.Sleep.

```
$ go run test.go
Launched SP1
Launched SP2
SP1 : 0
SP1 : 0 .5
SP2 : 0
SP2 : 0 .5
SP1 : 1
SP1 : 1 .5
SP2 : 1
SP2 : 1 .5
SP1 : 2
SP1 : 2 .5
SP2 : 2
SP2 : 2 .5
SP1 : 3
SP1 : 3 .5
SP2 : 3
SP2 : 3 .5
SP1 : 4
SP1 : 4 .5
SP2 : 4
SP2 : 4 .5
SP1 : 5
SP1 : 5 .5
SP2 : 5
SP2 : 5 .5
SP1 : 6
SP1 : 6 .5
SP2 : 6
SP2 : 6 .5
SP1 : 7
SP1 : 7 .5
SP2 : 7
SP2 : 7 .5
SP1 : 8
SP1 : 8 .5
SP2 : 8
SP2 : 8 .5
SP1 : 9
SP1 : 9 .5
SP2 : 9
SP2 : 9 .5
Done
```

Now, I change the sleep to take_cpu. If goroutines were executed in single thread, there should have been no chance for them to switch.

```
func sleep_print(tag string, count int, wg *sync.WaitGroup) {
    defer wg.Done()
    for i := 0; i < count; i++ {
        fmt.Println(tag, ":", i)
        // time.Sleep(1 * time.Second)
        take_cpu(1 * time.Second)
    }
}
```

Running it shows below results. Meanwhile I can see process `test` by top, using 100% cpu. Weird, it looks like goroutine can switch even in busy cpu loop.

```
$ go run test.go
Launched SP1
Launched SP2
SP1 : 0
SP1 : 0 .5
SP2 : 0
SP2 : 0 .5
SP1 : 1
SP1 : 1 .5
SP2 : 1
SP2 : 1 .5
SP1 : 2
SP1 : 2 .5
SP2 : 2
SP2 : 2 .5
SP1 : 3
SP1 : 3 .5
SP2 : 3
SP2 : 3 .5
SP1 : 4
SP1 : 4 .5
SP2 : 4
SP2 : 4 .5
SP1 : 5
SP1 : 5 .5
SP2 : 5
SP2 : 5 .5
SP1 : 6
SP1 : 6 .5
SP2 : 6
SP2 : 6 .5
SP1 : 7
SP1 : 7 .5
SP2 : 7
SP2 : 7 .5
SP1 : 8
SP1 : 8 .5
SP2 : 8
SP2 : 8 .5
SP1 : 9
SP1 : 9 .5
SP2 : 9
SP2 : 9 .5
Done
```

Articles [\[1\]](http://blog.nindalf.com/how-goroutines-work/#howgoroutinesareexecuted)[\[2\]](https://news.ycombinator.com/item?id=7652005) indicate that, after Go 1.2, goroutine can switch when entering a function. Article [\[3\]](https://blog.mozilla.org/services/2014/03/12/sane-concurrency-with-go/) says "Go's scheduler makes no guarantees about when, exactly, context switching will occur". Official notes [here](http://tip.golang.org/doc/go1.2#preemption).

I change my sleep_print this way, to avoid function calls to take_cpu. However, I still have the function calls to fmt.Println.

```
func sleep_print(tag string, count int, wg *sync.WaitGroup) {
    defer wg.Done()
    for i := 0; i < count; i++ {
        fmt.Println(tag, ":", i)
        fmt.Println(tag, ":", i, ".5")
        // time.Sleep(1 * time.Second)
        // take_cpu(1 * time.Second)
        for i := 0; i < 1000 * 1000 * 1500; i++ {}  // Approximately 1 second to me
    }
}
```

The result is the same. Two goroutines keep switching to each other.

```
$ go run test.go
Launched SP1
Launched SP2
SP1 : 0
SP1 : 0 .5
SP2 : 0
SP2 : 0 .5
SP1 : 1
SP1 : 1 .5
SP2 : 1
SP2 : 1 .5
SP1 : 2
SP1 : 2 .5
SP2 : 2
SP2 : 2 .5
SP1 : 3
SP1 : 3 .5
SP2 : 3
SP2 : 3 .5
SP1 : 4
SP1 : 4 .5
SP2 : 4
SP2 : 4 .5
SP1 : 5
SP1 : 5 .5
SP2 : 5
SP2 : 5 .5
SP1 : 6
SP1 : 6 .5
SP2 : 6
SP2 : 6 .5
SP1 : 7
SP1 : 7 .5
SP2 : 7
SP2 : 7 .5
SP1 : 8
SP1 : 8 .5
SP2 : 8
SP2 : 8 .5
SP1 : 9
SP1 : 9 .5
SP2 : 9
SP2 : 9 .5
Done
```

So my conclusion is that, goroutine can switch anytime, even in single core condition (GOMAXPROCS == 1). Goroutines can race.

P.S. Just for curious. When I set GOMAXPROCS = 4 (my core num), my program runs much faster. At least 2 cores are utilized, cpu 200%. Two sleep_print goroutines keeps switching to each other.

P.S. About handling concurrent control in Go way, usually we use channels to [Share Memory By Communicating](https://blog.golang.org/share-memory-by-communicating). Some [Go concurrency patterns](https://blog.golang.org/advanced-go-concurrency-patterns). Go also provides sync tools such as mutex, lock or condition, see [here](http://golang.org/pkg/sync/). Go's concurrency design borrows from [Communicating Sequential Processes](http://cs.stackexchange.com/questions/19506/differences-between-the-actor-model-and-communicating-sequential-processes-csp), which has some differences from Actor Model.

P.S. To detect goroutine races, go provides [Race Detector](https://blog.golang.org/race-detector). It is handy.

### Goroutine Can Race

Here's my program to simulate the classic bank balance problem. Note that there are for loops in Bank.change, making goroutine eagerer to switch.

```
// File name test2.go
package main

import (
    "fmt"
    "time"
)

type Bank struct {
    balance int
}

func (bank *Bank) change (amount int) {
    read := bank.balance
    for i := 0; i < 100; i++ { time.Sleep(100 * time.Nanosecond) }    // Make it easier to trigger goroutine switch
    write := read + amount
    for i := 0; i < 100; i++ { time.Sleep(100 * time.Nanosecond) }
    bank.balance = write
}

func main() {
    N_ROUTINE := 1000
    N_ADD := 1000
    BEGINNING_BALANCE := 100

    bank := &Bank{100}

    done := make(chan bool)
    for i := 0; i < N_ROUTINE; i++ {
        go func () {
            for j := 0; j < N_ADD; j++ {
                bank.change(1)
            }
            done <- true
        }()
    }
    for i := 0; i < N_ROUTINE; i++ {
        <- done
    }

    fmt.Println("Bank:", bank,
        "(should be:", BEGINNING_BALANCE + N_ROUTINE * N_ADD, ")")
}
```

Run it gives below result. This is clear evidence that goroutine can race. Without proper concurrent control, it corrupts the shared data.

```
$ go run test2.go
Bank: &{1100} (should be: 1000100 )
```

Golang provides a very handy tool - [Race Detector](https://blog.golang.org/race-detector). Use it to verify my program

```
$ go run -race test2.go
==================
WARNING: DATA RACE
Write by goroutine 5:
  main.(*Bank).change()
      /root/workspace/play-go/test2.go:17 +0xbd
  main.func·001()
      /root/workspace/play-go/test2.go:31 +0x93

Previous read by goroutine 368:
  main.(*Bank).change()
      /root/workspace/play-go/test2.go:13 +0x36
  main.func·001()
      /root/workspace/play-go/test2.go:31 +0x93

Goroutine 5 (running) created at:
  main.main()
      /root/workspace/play-go/test2.go:34 +0x252

Goroutine 368 (running) created at:
  main.main()
      /root/workspace/play-go/test2.go:34 +0x252
==================
```


