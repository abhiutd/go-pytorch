package main

// #cgo linux CFLAGS: -I/usr/local/cuda/include
// #cgo linux LDFLAGS: -lcuda -lcudart -L/usr/local/cuda/lib64
// #include <cuda.h>
// #include <cuda_runtime.h>
// #include <cuda_profiler_api.h>
import "C"

import (
	"bufio"
  "os"
	"context"
	"path/filepath"

	"github.com/k0kubun/pp"

	"github.com/rai-project/config"
	"github.com/rai-project/dlframework/framework/options"
	"github.com/rai-project/downloadmanager"
	"github.com/go-pytorch/work"
	nvidiasmi "github.com/rai-project/nvidia-smi"
	"github.com/rai-project/tracer"
	_ "github.com/rai-project/tracer/all"
)

var (
	batchSize		 = 1
	model        = "alexnet"
	graph_url		 = "https://s3.amazonaws.com/store.carml.org/models/pytorch/alexnet.pt"
	features_url = "http://data.dmlc.ml/mxnet/models/imagenet/synset.txt"
)

func main() {
	defer tracer.Close()

	dir, _ := filepath.Abs(".")
	dir = filepath.Join(dir, model)
	graph := filepath.Join(dir, "alexnet.pt")
	features := filepath.Join(dir, "synset.txt")

	if _, err := os.Stat(graph); os.IsNotExist(err) {
    if _, err := downloadmanager.DownloadInto(graph_url, dir); err != nil {
      panic(err)
    }
  }
	if _, err := os.Stat(features); os.IsNotExist(err) {

    if _, err := downloadmanager.DownloadInto(features_url, dir); err != nil {
      panic(err)
    }
  }

	// INFO
	pp.Println("Model + Weights url - ", graph_url)
	pp.Println("Labels url - ", features_url)

	imgDir, _ := filepath.Abs("./_fixtures")
  imagePath := filepath.Join(imgDir, "cat.jpg")
	// INFO
	pp.Println("Input path - ", imagePath)

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

	err = predictor.Predict(ctx, imagePath)
	if err != nil {
		panic(err)
	}

	predictions := predictor.ReadPredictedFeatures(ctx)

  if true {
    var labels []string
    f, err := os.Open(features)
    if err != nil {
      panic(err)
    }
    defer f.Close()
    scanner := bufio.NewScanner(f)
    for scanner.Scan() {
      line := scanner.Text()
      labels = append(labels, line)
    }

    len := len(predictions) / batchSize
    for i := 0; i < 1; i++ {
      res := predictions[i*len : (i+1)*len]
      res.Sort()
      pp.Println(res[0].Probability)
      pp.Println(labels[res[0].Index])
    }
  } else {
    _ = predictions
  }

	// INFO
	pp.Println("End of prediction...")
}

func init() {
	config.Init(
		config.AppName("carml"),
		config.VerboseMode(true),
		config.DebugMode(true),
	)
}
