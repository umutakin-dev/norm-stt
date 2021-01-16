#REQUIREMENTS
# ffmpeg
##

import vosk
import os
import sys
import getopt
import subprocess
import json
from vosk import Model, KaldiRecognizer, SetLogLevel

def main():

    argv = sys.argv[1:] 
    model_path = "./model"
    filename = ""
    
    try:
        
        opts, _ = getopt.getopt(argv, "f:m:",  
                                    ["file_name =", 
                                    "model_path ="]) 

        #print(opts)
        #print(args)
        
    except: 
        print("Error with arguments") 
        return

    for opt, arg in opts: 
            if opt in ['-f', '--file_name']: 
                filename = arg 
            elif opt in ['-m', '--model_path']: 
                model_path = arg 
        
    print( "FILE: ", filename, " MODEL: ",model_path)



    if not os.path.exists(model_path):
        print ("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
        return

    SetLogLevel(-1)
    sample_rate=16000
    model = Model(model_path)
    rec = KaldiRecognizer(model, sample_rate)


    process = subprocess.Popen(['ffmpeg', '-loglevel', 'quiet', '-i',
                                filename,
                                '-ar', str(sample_rate) , '-ac', '1', '-f', 's16le', '-'],
                                stdout=subprocess.PIPE)

    result = ""
    while True:
        data = process.stdout.read(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            data = json.loads(rec.Result())
            result += data['text']

    #print(result) 
    data = json.loads(rec.FinalResult())
    result += data['text']
    print("\n")
    print(result)

if __name__ == '__main__':
    main()