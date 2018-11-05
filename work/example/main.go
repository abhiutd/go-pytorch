package main

// #cgo linux CFLAGS: -I/usr/local/cuda/include
// #cgo linux LDFLAGS: -lcuda -lcudart -L/usr/local/cuda/lib64
// #include <cuda.h>
// #include <cuda_runtime.h>
// #include <cuda_profiler_api.h>
import "C"

import (
	"context"
	"path/filepath"

	"github.com/k0kubun/pp"

	"github.com/rai-project/config"
	"github.com/rai-project/dlframework/framework/options"
	"github.com/go-pytorch/work"
	nvidiasmi "github.com/rai-project/nvidia-smi"
	"github.com/rai-project/tracer"
	_ "github.com/rai-project/tracer/all"
)

var (
	model        = "resnet"
)


func main() {
	defer tracer.Close()

	dir, _ := filepath.Abs(".")
	dir = filepath.Join(dir, model)
	graph := filepath.Join(dir, "resnet_18.pt")
	batchSize := 1
	opts := options.New()

	device := options.CPU_DEVICE
	if nvidiasmi.HasGPU {
		pytorch.SetUseGPU()
		device = options.CUDA_DEVICE

	} else {
		pytorch.SetUseCPU()
	}

	ctx := context.Background()

	span, ctx := tracer.StartSpanFromContext(ctx, tracer.FULL_TRACE, "pytorch_batch")
	defer span.Finish()

	predictor, err := pytorch.New(
		ctx,
		options.WithOptions(opts),
		options.Device(device, 0),
		options.Graph([]byte(graph)),
		options.BatchSize(batchSize))
	if err != nil {
		panic(err)
	}
	defer predictor.Close()

	err = predictor.Predict(ctx)
	if err != nil {
		panic(err)
	}

	err = predictor.Predict(ctx)
	if err != nil {
		panic(err)
	}

	pp.Println("end of prediction...")
}

func init() {
	config.Init(
		config.AppName("carml"),
		config.VerboseMode(true),
		config.DebugMode(true),
	)
}
