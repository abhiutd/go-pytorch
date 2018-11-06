#define _GLIBCXX_USE_CXX11_ABI 0

#include <algorithm>
#include <iosfwd>
#include <memory>
#include <string>
#include <utility>
#include <vector>

#include <torch/torch.h>
#include <torch/script.h>

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>

#include "json.hpp"
#include "predictor.hpp"
#include "timer.h"
#include "timer.impl.hpp"

#if 0
#define DEBUG_STMT std ::cout << __func__ << "  " << __LINE__ << "\n";
#else
#define DEBUG_STMT
#endif

using namespace torch;
using std::string;
using json = nlohmann::json;
using namespace cv;

/* Pair (label, confidence) representing a prediction. */
using Prediction = std::pair<int, float>;

/*
	Predictor class takes in one module file (exported using torch JIT compiler)
	, batch size and device mode for inference
*/
class Predictor {
 public:
  Predictor(const string &model_file, int batch, torch::DeviceType mode);
  void Predict(string datapath);

  std::shared_ptr<torch::jit::script::Module> net_;
  int width_, height_, channels_;
  int batch_;
  int pred_len_;
  torch::DeviceType mode_{torch::kCPU};
  profile *prof_{nullptr};
  bool profile_enabled_{false};
  at::Tensor result_;
};

Predictor::Predictor(const string &model_file, int batch, torch::DeviceType mode) {
  /* Load the network. */
	// In pytorch, a loaded module in c++ is given 
	// type torch::jit::script::Module as it has been
	// ported from python/c++ via pytorch's JIT compiler
  net_ = torch::jit::load(model_file);
	assert(net_ != nullptr);

  mode_ = mode;

	// TODO should fetch width and height from model
	width_ = 224;
	height_ = 224;
	channels_ = 3;
  batch_ = batch;

  CHECK(channels_ == 3 || channels_ == 1)
      << "Input layer should have 1 or 3 channels.";


}

void Predictor::Predict(const string &datapath) {

	//result_ = nullptr;

	Mat image = imread(datapath);
	std::vector<int64_t> sizes = {1, 3, image.rows, image.cols};
	at::TensorOptions options(at::ScalarType::Byte);
	at::Tensor tensor_image = torch::from_blob(image.data, at::IntList(sizes), options);
	tensor_image = tensor_image.toType(at::kFloat);

	std::vector<torch::jit::IValue> inputs;
	inputs.emplace_back(tensor_image);

	// Execute the model and turn its output into a tensor.
	result_ = net_->forward(inputs).toTensor();

}

PredictorContext NewPytorch(char *model_file, int batch,
                          int mode) {
  try {
    const auto ctx = new Predictor(model_file, batch,
                                   (torch::DeviceType)mode);
    return (void *)ctx;
  } catch (const std::invalid_argument &ex) {
    LOG(ERROR) << "exception: " << ex.what();
    errno = EINVAL;
    return nullptr;
}

void SetModePytorch(int mode) {
	
}

void InitPytorch() {}

void PredictPytorch(PredictorContext pred, const string &datapath) {
  auto predictor = (Predictor *)pred;
  if (predictor == nullptr) {
    return;
  }
  predictor->Predict(datapath);
  return;
}

const float*GetPredictionsPytorch(PredictorContext pred) {
  auto predictor = (Predictor *)pred;
  if (predictor == nullptr) {
    return nullptr;
  }

	//TODO return float casted result
  return nullptr;
}

void DeletePytorch(PredictorContext pred) {
  auto predictor = (Predictor *)pred;
  if (predictor == nullptr) {
    return;
  }
  if (predictor->prof_) {
    predictor->prof_->reset();
    delete predictor->prof_;
    predictor->prof_ = nullptr;
  }
  delete predictor;
}

void StartProfilingPytorch(PredictorContext pred, const char *name,
                         const char *metadata) {

}

void EndProfilingPytorch(PredictorContext pred) {

}

void DisableProfilingPytorch(PredictorContext pred) {

}

char *ReadProfilePytorch(PredictorContext pred) {
  char* temp = NULL;
	return temp;
}

int GetWidthPytorch(PredictorContext pred) {
  auto predictor = (Predictor *)pred;
  if (predictor == nullptr) {
    return 0;
  }
  return predictor->width_;
}

int GetHeightPytorch(PredictorContext pred) {
  auto predictor = (Predictor *)pred;
  if (predictor == nullptr) {
    return 0;
  }
  return predictor->height_;
}

int GetChannelsPytorch(PredictorContext pred) {
  auto predictor = (Predictor *)pred;
  if (predictor == nullptr) {
    return 0;
  }
  return predictor->channels_;
}

int GetPredLenPytorch(PredictorContext pred) {
  auto predictor = (Predictor *)pred;
  if (predictor == nullptr) {
    return 0;
  }
  return predictor->pred_len_;
}

