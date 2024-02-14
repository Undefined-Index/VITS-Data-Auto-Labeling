# VITS-Data-Auto-Labeling
A script that uses FunASR for Bert-VITS2 and GPT-SoVITS vocal data labeling
使用FunASR对Bert-VITS2和GPT-SoVITS声音数据自动打标

### Main feature|主要特性
-Use FunASR for speech recognition.
-Remove segments from the audio file that remain silent for longer than 2 seconds, only keep the part where someone is speaking. 

-使用FunASR进行语音识别
-从音频文件中删除无人声时间超过2秒的片段，只保留有人说话的部分去除空白间断。


### Installation|安装

    pip install -r requirements.txt
    python main.py

FFmpeg is required
需要安装FFmpeg
