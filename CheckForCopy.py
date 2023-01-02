while True:
    import whisper
    import time
    import librosa
    import soundfile as sf
    import re
    import os

    # model = whisper.load_model("tiny.en")
    # model = whisper.load_model("base.en")  
    model = whisper.load_model("small.en") # load the small model
    # model = whisper.load_model("medium.en")
    # model = whisper.load_model("large")

    folders =  ["WhisperVideo/", "WhisperVideo/ProcessedVideo/", "WhisperVideo/TextFiles/", "WhisperVideo/AudioFiles/"]
    for folder in folders:
      path = "C:/Users/aljen/" + folder
      if not os.path.exists(path): # Create the folder if it does not exist
        os.mkdir(path)
    
    import openai
    from time import time, sleep
    import textwrap
    import re
    import os
    
    # Get a list of all items in the WhisperVideo folder
    video_folders = [item for item in os.listdir(r"C:\Users\aljen\My Drive\WhisperVideo") if os.path.isdir(os.path.join("C:/Users/aljen/My Drive/WhisperVideo", item))]

# Loop through the video folders and process all the video files inside them
    for video_folder in video_folders:
        folder_path = os.path.join("C:/Users/aljen/My Drive/WhisperVideo", video_folder)
        video_files = [item for item in os.listdir(folder_path) if item.endswith((".mp4", ".mov", ".avi", ".mkv"))]

    # Loop through the video files and transcribe them
        for video_file in video_files:
        # Extract the audio and transcribe the audio file using Whisper, as before
        

        # Skip the file if it is not a video format
            if not video_file.endswith((".mp4", ".mov", ".avi", ".mkv")):
                continue

        # Extract the audio from the video file using librosa
            video_path = os.path.join(folder_path, video_file)
            audio_path = os.path.join(folder_path, video_file[:-4] + ".wav") # Replace the video extension with .wav

            y, sr = librosa.load(video_path, sr=16000) # Load the audio with 16 kHz sampling rate
            sf.write(audio_path, y, sr) # Save the audio as a wav file

        # Transcribe the audio file using Whisper
            result = model.transcribe(audio_path)
            text = result["text"].strip()
            text = text.replace(". ", ".\n\n")

  # Save the transcription as a text file in Google Docs
            text_folder = folder_path
            text_file = video_file[:-4] + ".txt" # Replace the video extension with .txt
            text_path = os.path.join(text_folder, text_file)
            with open(text_path, "w") as f:
                f.write(text)

  # Move the video file to the ProcessedVideo folder
            os.remove(video_path)
            os.remove(audio_path)


  # Print a message to indicate the progress
            print(f"Processed {video_file} and saved the transcription as {text_file}")


            import openai
    
            def open_file(filepath):
                with open(filepath, 'r', encoding='utf-8') as infile:
                    return infile.read()

            api_key = open_file(r'C:\Users\aljen\RecursiveSummarizer\openaiapikey.txt')
            if api_key:
                openai.api_key = api_key
                print("Successfully opened API key file")
            else:
                print("Error: API key file could not be opened")


            def save_file(content, filepath):
                with open(filepath, 'w', encoding='utf-8') as outfile:
                    outfile.write(content)


            def gpt3_completion(prompt, engine='text-davinci-002', temp=0.6, top_p=1.0, tokens=2000, freq_pen=0.25, pres_pen=0.0, stop=['<<END>>']):
                    max_retry = 5
                    retry = 0
                    while True:
                        try:
                            response = openai.Completion.create(
                                engine=engine,
                                prompt=prompt,
                                temperature=temp,
                                max_tokens=tokens,
                                top_p=top_p,
                                frequency_penalty=freq_pen,
                                presence_penalty=pres_pen,
                                stop=stop)
                            text = response['choices'][0]['text'].strip()
                            text = re.sub('\s+', ' ', text)
                            filename = '%s_gpt3.txt' % time()
            # Load the transcription from the file
                            with open('C:/Users/aljen/My Drive/RecursiveSummarizer/gpt3_logs/%s' % filename, 'w') as outfile:
                                outfile.write('PROMPT:\n\n' + prompt + '\n\n==========\n\nRESPONSE:\n\n' + text)
                            return text
                        except Exception as oops:
                            retry += 1
                            if retry >= max_retry:
                                return "GPT3 error: %s" % oops
                            print('Error communicating with OpenAI:', oops)
                            sleep(1)


            if __name__ == '__main__':
                alltext = open_file(text_path)
                chunks = textwrap.wrap(alltext, 2000)
                result = list()
                count = 0
                for chunk in chunks:
                    count = count + 1
                    prompt = open_file(r'C:\Users\aljen\My Drive\RecursiveSummarizer\prompt.txt').replace('<<SUMMARY>>', chunk)
                    prompt = prompt.encode(encoding='ASCII', errors='ignore').decode()
                    summary = gpt3_completion(prompt)
                    print('\n\n\n', count, 'of', len(chunks), ' - ', summary)
                    result.append(summary)
                save_file('\n\n'.join(result), folder_path + "/" + text_file[:-4] + "_Summarized" + ".txt")