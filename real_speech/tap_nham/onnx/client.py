


























import torch
import utils
import numpy as np
import tritonclient.grpc as grpcclient
from scipy.io.wavfile import write
import sys
sys.path.append('C:\\Users\\sodalab\\Desktop\\refactorcode\\refactor2\\text-to-speech\\')
from research.vits.vits_1.text import text_to_sequence
import commons_onnx


def get_text(text, hps):
    text_norm = text_to_sequence(text, hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = commons_onnx.intersperse(text_norm, 0)
    text_norm = torch.LongTensor(text_norm)
    
    return text_norm

client = grpcclient.InferenceServerClient(url="192.168.2.169:21001")

text = 'taj˧˨-liəw˨ˀ˩ʔ sɯə˧˩˨-doj˧˩˨ = bo˧˩˨-suŋ͡m˧˧ ve˧˨ not˦˥ ɑnˈtɑɫədʒi săw˧˧ xi˧˧ xaw˧˩˨-sat˦˥ cen˧˧ vuŋ͡m˧˨ zɯ˧ˀ˥-liəw˨ˀ˩ʔ mɤj˨˦ kuə˧˩˨ ˈhɑn da˧˧'
hps = utils.get_hparams_from_file("logs/nu_mienbac/config.json")
stn_tst = get_text(text, hps)

x_tst = stn_tst.unsqueeze(0)
x_tst_lengths = torch.LongTensor([stn_tst.size(0)])

x_tst = x_tst.numpy().astype(np.int64)
x_tst_lengths = x_tst_lengths.numpy().astype(np.int64)
x_tst_lengths = np.expand_dims(x_tst_lengths,axis=0)

input_tensors = [grpcclient.InferInput("x_tst", x_tst.shape, "INT64"),grpcclient.InferInput("x_tst_lengths", x_tst_lengths.shape, "INT64")]
input_tensors[0].set_data_from_numpy(x_tst)
input_tensors[1].set_data_from_numpy(x_tst_lengths)
results = client.infer(model_name="ensemble_model", inputs=input_tensors)
output_data = results.as_numpy("synthesized_audio").astype(np.float32)
print(f"output_data: {output_data}")
file_name = f'C:/Users/sodalab/Desktop/refactorcode/refactor2/text-to-speech/onnx_triton/vits/test_onnx3.wav'
write(file_name, hps.data.sampling_rate, output_data[0,0])
