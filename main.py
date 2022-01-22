import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from numpy import size
from scipy.fft import fft, fftfreq
import csv
from datetime import datetime
from os import getcwd
from re import split
from sklearn.utils.metaestimators import if_delegate_has_method

file="20220113-after-stim-3-ku"
filter_name = split(r"-", file)
print(filter_name[0])
extension=".wav"
#a
#Create read and write filenames
read_filename=file+extension
write_filename=file+"-bowel-part"+extension

#Read the audio file
audio_freq_sample, audio_in = wavfile.read(read_filename)
length_audio=len(audio_in)
audio_duration=int(length_audio/audio_freq_sample)
df=audio_freq_sample/length_audio
frequency_audio=np.linspace(-1*audio_freq_sample/2,audio_freq_sample/2,length_audio)
t=np.linspace(0,length_audio-1,length_audio-1)/audio_freq_sample
#[fund_freq,loc] = pitch(audio_in,audio_freq_sample);

#Plot the time domain signal
plt.figure(figsize=(10, 8))
time=np.linspace(audio_duration/length_audio,audio_duration,length_audio);
plt.xlabel("Time (s)")
plt.ylabel("Signal intensity (a.u.)")
plt.title("Audio Signal")
plt.plot(time,audio_in)
plt.axhline(y=100, color='r', linestyle='-')
plt.grid()

cpm=0
max_array=[]
max_index_array=[]
bowel_array=[]
bowel_array=np.array(bowel_array)

for i in range(1,length_audio,200):
    if np.amax(audio_in[i:i+199])>100 and np.amax(audio_in[i:i+199])!=audio_in[i+199]:
        cpm+=1
        max_index = np.argmax(audio_in[i:i+199])
        m = np.amax(audio_in[i:i+199])
        max_index = i+max_index;
        max_array.append(m)
        max_index_array.append(max_index)
        if max_index>29 and max_index<479931:
            bowel_array = np.concatenate((bowel_array, audio_in[max_index-30:max_index+70]))
            #audio_in[max_index-30:max_index+70]=0
    
#Plot the bowel sound signal
plt.figure(figsize=(10, 8))
bowel_duration=(audio_duration*len(bowel_array))/length_audio
time_bowel=np.linspace(audio_duration/length_audio,bowel_duration,len(bowel_array))
plt.xlabel("Time (s)")
plt.ylabel("Signal intensity (a.u.)")
plt.title("Audio Signal")
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
    
total_area = sum(abs(bowel_array))/100*0.003 #For conversion to the values obtained in MATLAB
avg_area = total_area/bowel_duration
print("%.2f" % bowel_duration)
print("%.2f" %total_area)    
    
plt.show()

header_switch=0
FILE_NAME = "data.csv"
if len(filter_name)<5:
    filter_name[4]="AVO"
    
#with open(FILE_NAME, 'r') as csvfile:
#    csvreader = csv.reader(csvfile)
#    for row in csvreader:
#        if len(row)<1:
#            header_switch=1
            
with open(FILE_NAME, "a", newline='') as csv_file:
    writer = csv.writer(csv_file, delimiter=",")
    if header_switch:
        writer.writerow(['Date', 'Number of Measurement', 'User', 'Condition' 'Bowel Duration (s)', 'Amplitude', 'Avg. Amplitude'])
    writer.writerow([filter_name[0], filter_name[3], filter_name[4], filter_name[1]+''+filter_name[2], str("%.2f" % bowel_duration), str("%.2f" % total_area), str("%.2f" % avg_area)])
    csv_file.close()  
    
    