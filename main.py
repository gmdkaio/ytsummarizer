import yt_dlp, whisper, os
from transformers import pipeline
import subprocess

def download_audio(youtube_url, output_path='audio'):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_path, 'audio.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ffmpeg_location': r'C:\ffmpeg\bin',  
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])
    return os.path.join(output_path, 'audio.mp3')  


def convert_to_wav_ffmpeg(input_file, output_file):
    try:
        command = [
            r'C:\ffmpeg\bin\ffmpeg.exe',
            '-i', input_file,
            output_file
        ]
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")

def transcribe_audio(wav_file):
    if not os.path.exists(wav_file):
        print(f"File not found: {wav_file}")
    model = whisper.load_model('base')
    result = model.transcribe(wav_file)
    return result['text']

def summarize_text(text):
    summarizer = pipeline('summarization')
    max_input_length = 1024
    max_output_length = 150

    def split_text(text, max_length):
        return [text[i:i+max_length] for i in range(0, len(text), max_length)]

    chunks = split_text(text, max_input_length)
    summaries = [summarizer(chunk, max_length=max_output_length, min_length=30, do_sample=False)[0]['summary_text'] for chunk in chunks]
    return ' '.join(summaries)

def main(youtube_url):
    audio_file = download_audio(youtube_url)
    wav_file = os.path.join('audio', 'audio.wav') 
    convert_to_wav_ffmpeg(audio_file, wav_file)  
    text = transcribe_audio(wav_file)
    summary = summarize_text(text)
    
    with open('output.txt', 'w', encoding='utf-8') as f:
        f.write("Summary:\n")
        f.write(summary)
    
    print("Transcript and summary have been saved to output.txt")
    print("Transcript:")
    print(text)
    print("\nSummary:")
    print(summary)

if __name__ == '__main__':
    youtube_url = input('Insert video URL: ')
    main(youtube_url)

