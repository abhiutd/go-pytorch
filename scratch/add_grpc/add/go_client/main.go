/*
 *
 * Copyright 2015 gRPC authors.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 */

package main

import (
        "log"
        "time"

        "golang.org/x/net/context"
        "google.golang.org/grpc"
        pb "self/add/go"
)

const (
        address     = "localhost:50052"
        defaultName = "world"
)

func main() {
        // Set up a connection to the server.
        conn, err := grpc.Dial(address, grpc.WithInsecure())
        if err != nil {
                log.Fatalf("did not connect: %v", err)
        }
        defer conn.Close()
        c := pb.NewOperationClient(conn)

        // Contact the server and print out its response.
        //name := defaultName
        //if len(os.Args) > 1 {
        //        name = os.Args[1]
        //}
        //clientDeadline := time.Now().Add(time.Duration(*deadlineMs) * time.Millisecond)
        //var deadlineMs = flag.Int("deadline_ms", 200*1000, "Default deadline in milliseconds.")
        ctx, cancel := context.WithTimeout(context.Background(), 300*time.Second)
        defer cancel()
        var num_1, num_2 int32 = 10, 5
        r, err := c.Add(ctx, &pb.OpRequest{A: &num_1, B: &num_2})
        if err != nil {
                log.Fatalf("could not add: %v", err)
        }
        log.Printf("The sum is: %d", *r.C)
}
