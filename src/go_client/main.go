/*
 *
 * Copyright 2018 MLModelScope authors.
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
        pb "github.com/go-pytorch/src/go"
)

const (
        address     = "localhost:50052"
        defaultName = "dlframework"
)

func main() {

        // Set up a connection to the server
        conn, err := grpc.Dial(address, grpc.WithInsecure())
        if err != nil {
                log.Fatalf("did not connect: %v", err)
        }
        defer conn.Close()
        c := pb.NewDlframeworkClient(conn)
        ctx, cancel := context.WithTimeout(context.Background(), 300*time.Second)
        defer cancel()

        // Contact the server 
        // Send test image URL as part of the message
        var image_url string = "https://s3.amazonaws.com/outcome-blog/wp-content/uploads/2017/02/25192225/cat.jpg"
        r, err := c.Predict(ctx, &pb.DlRequest{Image: &image_url})
        if err != nil {
                log.Fatalf("could not add: %v", err)
        }
        log.Printf("Predicted: %s", *r.Prediction)
}
