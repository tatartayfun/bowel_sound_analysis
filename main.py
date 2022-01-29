#Token: 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

import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from numpy import size
from scipy.fft import fft, fftfreq
import csv
from datetime import datetime
from os import getcwd, listdir
from re import split
import glob
from sklearn.utils.metaestimators import if_delegate_has_method
import os.path

write_switch = 1

file_exists = os.path.isfile('data.csv')

#Check all the sound files in the current directory
dir_list = glob.glob("*.wav")

for file in dir_list:
    #Create read and write filenames
    read_filename=file
    filter_name = split(r"-", file[0:-4]) #To get rid of .wav extension
    #Read the audio file
    audio_freq_sample, audio_in = wavfile.read(read_filename)
    length_audio=len(audio_in)
    audio_duration=int(length_audio/audio_freq_sample)
    df=audio_freq_sample/length_audio
    frequency_audio=np.linspace(-1*audio_freq_sample/2,audio_freq_sample/2,length_audio)
    t=np.linspace(0,length_audio-1,length_audio-1)/audio_freq_sample
    #[fund_freq,loc] = pitch(audio_in,audio_freq_sample);
    
    '''
    #Plot the time domain signal
    plt.figure(figsize=(10, 8))
    time=np.linspace(audio_duration/length_audio,audio_duration,length_audio);
    plt.xlabel("Time (s)")
    plt.ylabel("Signal intensity (a.u.)")
    plt.title("Audio Signal")
    plt.plot(time,audio_in)
    plt.axhline(y=100, color='r', linestyle='-')
    plt.grid()
    '''
    
    cpm=0
    max_array=[]
    max_index_array=[]
    bowel_array=[]
    bowel_array=np.array(bowel_array)
    
    for i in range(1,length_audio,200):
        if np.amax(audio_in[i:i+198])>100 and np.amax(audio_in[i:i+198])!=audio_in[i+198]:
            cpm+=1
            max_index = np.argmax(audio_in[i:i+199])
            m = np.amax(audio_in[i:i+199])
            max_index = i+max_index;
            max_array.append(m)
            max_index_array.append(max_index)
            if max_index>29 and max_index<479931:
                bowel_array = np.concatenate((bowel_array, audio_in[max_index-30:max_index+70]))
                #audio_in[max_index-30:max_index+70]=0
    
    bowel_duration=(audio_duration*len(bowel_array))/length_audio

    '''    
    #Plot the bowel sound signal
    plt.figure(figsize=(10, 8))
    time_bowel=np.linspace(audio_duration/length_audio,bowel_duration,len(bowel_array))
    plt.xlabel("Time (s)")
    plt.ylabel("Signal intensity (a.u.)")
    plt.title("Bowel Sound Extracted")
    plt.plot(time_bowel,bowel_array)
    plt.grid()
    
    #Plot the FFT of the bowel signal
    plt.figure(figsize=(10, 8))
    # Number of sample points
    N = len(bowel_array)
    # sample spacing
    T = 1.0 / audio_freq_sample
    x = np.linspace(0.0, N*T, N, endpoint=False)
    bowel_fft = fft(bowel_array)
    xf = fftfreq(N, T)[:N//2]
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Intensity (a.u.)")
    plt.title("Single sided FFT of the bowel signal")
    plt.plot(xf, 2.0/N * np.abs(bowel_fft[0:N//2]))
    plt.grid()
    '''   
                
    total_area = sum(abs(bowel_array))/100*0.003 #For conversion to the values obtained in MATLAB
    avg_area = total_area/bowel_duration
    #print("%.2f" % bowel_duration)
    #print("%.2f" %total_area)    
    FILE_NAME = "data.csv"
    if len(filter_name)<5:
        filter_name.append("AVO")
        
    #with open(FILE_NAME, 'r') as csvfile:
    #    csvreader = csv.reader(csvfile)
    #    for row in csvreader:
    #        if len(row)<1:
    #            header_switch=1
    
    #Calculate a score for ordering in .csv file
    if filter_name[1]=='before':
        condition_multiplier=1
    elif filter_name[1]=='after':
        condition_multiplier=3
    else:
        condition_multiplier=2
        
    condition = int(filter_name[3])+10*condition_multiplier
    
    order_score = str(100*int(filter_name[0])+condition)
    
    if write_switch: 
        print(read_filename)           
        with open(FILE_NAME, "a", newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=" ")
            if not file_exists:
                writer.writerow(['Order', 'Date', 'NumberofMeasurement', 'User', 'Condition', 'BowelDuration(s)', 'Amplitude', 'Avg.Amplitude'])
                file_exists = os.path.isfile('data.csv')
            writer.writerow([order_score, filter_name[0], filter_name[3], filter_name[4], filter_name[1]+''+filter_name[2], str("%.2f" % bowel_duration).replace('.', ','), str("%.2f" % total_area).replace('.', ','), str("%.2f" % avg_area).replace('.', ',')])
            csv_file.close()  
        
#plt.show()
        