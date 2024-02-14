from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
import json
import subprocess
import os
from tqdm import tqdm

folder_name = input('Please enter the name of the voice:')
while folder_name == '':
    folder_name = input('Please enter the name of the voice:')
resource = input('Please enter the WAV file path:')
while os.path.exists(resource) == False:
    print("File doesn't exist")
    resource = input('Please enter the WAV file path:')
file_name = os.path.basename(resource)
    
sampling_rate = input('Please enter the sampling rate(Leave blank to use the default value 44100):')
if sampling_rate == '':
    sampling_rate = '44100'
try:
    if int(sampling_rate) <= 0:
        sampling_rate = '44100'
except:
    sampling_rate = '44100'
    
os.makedirs('output/' + folder_name, exist_ok=True)

inference_pipeline = pipeline(
    task=Tasks.auto_speech_recognition,
    model='damo/speech_paraformer-large-vad-punc_asr_nat-zh-cn-16k-common-vocab8404-pytorch'
)

rec_result = inference_pipeline(audio_in=resource)

def cut_wav(input_file, output_file, start_time, end_time):
    command = [
        'ffmpeg',
        '-i', input_file,
        '-ss', str(start_time),
        '-to', str(end_time),
        '-ar', sampling_rate,
        '-ac', "1",
        output_file
    ]

    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

data = json.loads(json.dumps(rec_result))
sentences = data['sentences']



def print_sentences(sentences, count):
    for sentence in tqdm(sentences):
        ts_text = ""
        temp_list = sentence['ts_list']
        temp_text = ''.join(sentence['text']).replace(" ", "")
        cut = False
        if len(temp_list) != 0:
            start_time = temp_list[0][0] / 1000
            for i in range(len(temp_list)):
                if i < len(temp_list) - 1:
                    if temp_list[i + 1][0] - temp_list[i][1] > 2000:
                        ts_text += temp_text[i]
                        end_time = temp_list[i][1] / 1000
                        output_wav = os.getcwd() + "/output/" + folder_name + '/' + file_name + str(count) + ".wav"
                        f.write(output_wav + "|" + file_name + "|ZH|" + ts_text + "\n") 
                        cut_wav(resource, output_wav, start_time, end_time)
                        count+=1
                        start_time = temp_list[i + 1][0] / 1000
                        ts_text = ""
                        cut = True
                    else:
                        ts_text += temp_text[i]
                else:
                    ts_text += temp_text[i]
                    
                    
        if cut:
            end_time = sentence['end'] / 1000
            output_wav = os.getcwd() + "/output/" + folder_name + '/' + file_name + str(count) + ".wav"
            f.write(output_wav + "|" + file_name + "|ZH|" + ts_text + "\n") 
            cut_wav(resource, output_wav, start_time, end_time)
            count+=1
        else:
            start_time = temp_list[0][0] / 1000
            end_time = sentence['end'] / 1000
            output_wav = os.getcwd() + "/output/" + folder_name + '/' + file_name + str(count) + ".wav"
            f.write(output_wav + "|" + file_name + "|ZH|" + ts_text + "\n") 
            cut_wav(resource, output_wav, start_time, end_time)
            count+=1
        

with open(folder_name + '.list','a', encoding="utf-8") as f:
    print_sentences(sentences, 0)
    
print('Done')