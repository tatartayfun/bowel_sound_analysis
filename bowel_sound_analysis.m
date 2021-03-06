format long
close all;
clear all;

file="20220101-before-stim-4-ku";
extension=".wav";
read_filename=strcat(file,extension);
write_filename=strcat(file,"-bowel-part",extension)

%Read the audio file
[audio_in,audio_freq_sample] = audioread(read_filename);
%smooth_audio=(smooth(audio_in(:,1))+smooth(audio_in(:,2)))/2;
smooth_audio=(smooth(audio_in(:,1)));
length_audio=length(audio_in);
audio_duration=length_audio/audio_freq_sample;
df=audio_freq_sample/length_audio;
frequency_audio=-audio_freq_sample/2:df:audio_freq_sample/2-df;
t=(0:length_audio-1)/audio_freq_sample;
[fund_freq,loc] = pitch(audio_in,audio_freq_sample);

%Plot time domain signal
figure;
time=(audio_duration/length_audio:audio_duration/length_audio:audio_duration);
audio_in=audio_in(:,1);
plot(time,audio_in)
title('Audio Signal');
xlabel('Time (s)');
ylabel('Amplitude');
hold on
grid on
yline(0.003, 'r')

cpm=0;
max_array=[];
max_index_array=[];
bowel_array=[];
for i=1:200:length_audio
    if max(audio_in(i:i+199))>0.003 & max(audio_in(i:i+199))~=audio_in(i+199)
        cpm=cpm+1;
        [m,max_index]=max(audio_in(i:i+199));
        i
        max_index=i+max_index-1;
        %if (max_index-max_index_array(length(max_index_array))<400)&(max_array(length(max_array))/m>5)
        %    cpm=cpm-1;
        %end
        max_array=[max_array m];
        max_index_array=[max_index_array max_index];
        if max_index>29&&max_index<479931
            bowel_array=[bowel_array; audio_in(max_index-30:max_index+70)];
            audio_in(max_index-30:max_index+70)=0;
        end
    end
end

figure;
bowel_duration=(audio_duration*length(bowel_array))/length_audio;
time_bowel=(audio_duration/length_audio:audio_duration/length_audio:bowel_duration);
plot(time_bowel,bowel_array)
title('Extracted Bowel Signal');
xlabel('Time (s)');
ylabel('Amplitude');
xlim([0,bowel_duration])
hold on
grid on

%Plot Fourier transform of the signal
figure;
T=1/audio_freq_sample;
Y=fft(bowel_array);
length_bowel=length(bowel_array);
double_sided=abs(Y/length_bowel);
single_sided=double_sided(1:length_bowel/2+1);
single_sided(2:end-1)=2*single_sided(2:end-1);
f=audio_freq_sample*(0:(length_bowel/2))/length_bowel;
single_sided=smooth(single_sided);
plot(f,single_sided) 
title('Single-Sided Amplitude Spectrum of Bowel Sound')
xlabel('f(Hz)')
ylabel('|P1(f)|')
xlim([0,400])
hold on
grid on

%Find percentile frequencies
w=hanning(length_bowel, 'periodic');
[pxx,freq]=periodogram(bowel_array, w, length_bowel, audio_freq_sample, 'power');
percentile=0;
for i=1:length(pxx)
    percentile=percentile+pxx(i);
    if percentile>=0.25*sum(pxx)
        f25=freq(i);
        break;
    end
end
percentile=0;
for i=1:length(pxx)
    percentile=percentile+pxx(i);
    if percentile>=0.5*sum(pxx)
        f50=freq(i);
        break;
    end
end
percentile=0;
for i=1:length(pxx)
    percentile=percentile+pxx(i);
    if percentile>=0.75*sum(pxx)
        f75=freq(i);
        break;
    end
end
percentile=0;
for i=1:length(pxx)
    percentile=percentile+pxx(i);
    if percentile>=0.90*sum(pxx)
        f90=freq(i);
        break;
    end
end
%figure;
%plot(freq,pxx)
xlim([0,500])

time_bowel(end)
sum(abs(bowel_array))

audiowrite(write_filename,bowel_array,audio_freq_sample)
close all;