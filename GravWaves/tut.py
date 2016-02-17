import numpy as np 
from scipy import signal 
from scipy.interpolate import interp1d 
from scipy.signal import butter, filtfilt, iirdesign, zpk2tf, freqz 

import matplotlib.pyplot as plt 
import matplotlib.mlab as mlab
import h5py

import readligo as rl 

fn_H1 = 'H-H1_LOSC_4_V1-1126259446-32.hdf5' 
strain_H1, time_H1, chan_dict_H1 = rl.loaddata(fn_H1, 'H1')
fn_L1 = 'L-L1_LOSC_4_V1-1126259446-32.hdf5'
strain_L1, time_L1, chan_dict_L1 = rl.loaddata(fn_L1, 'L1')

fs = 4096 
time = time_H1
dt = time[1] - time[0]

NRtime, NR_H1 = np.genfromtxt('GW150914_4_NR_waveform.txt').transpose()

print('  time_H1: len, min, mean, max = ', len(time_H1), time_H1.min(), time_H1.mean(), time_H1.max())
print('strain_H1: len, min, mean, max = ', len(strain_H1), strain_H1.min(), strain_H1.mean(), strain_H1.max())
print('strain_L1: len, min, mean, max = ', len(strain_L1), strain_L1.min(), strain_L1.mean(), strain_L1.max())

# plot +- 5 seconds around the event
tevent = 1126259462.422 # mon sept 15 09:50:45 GMT 2015
deltat = 5. # seconds around the event
# index into the strain time series for this time interval
indxt = np.where((time_H1 >= tevent-deltat) & (time_H1 < tevent+deltat))

plt.figure()
plt.plot(time_H1[indxt] - tevent, strain_H1[indxt], 'r', label='H1 Strain')
plt.plot(time_L1[indxt] - tevent, strain_L1[indxt], 'g', label='L1 Strain')
plt.xlabel('time (s) since '+str(tevent))
plt.ylabel('strain')
plt.legend(loc='lower right')
plt.title('Advanced LIGO strain data near GW150914')
plt.savefig('GW150914_strain.png')


NFFT = 1*fs 
fmin = 10
fmax = 2000
Pxx_H1, freqs = mlab.psd(strain_H1, Fs=fs, NFFT=NFFT)
Pxx_L1, freqs = mlab.psd(strain_L1, Fs=fs, NFFT=NFFT)

psd_H1 = interp1d(freqs, Pxx_H1)
psd_L1 = interp1d(freqs, Pxx_L1)

plt.figure()
plt.loglog(freqs, np.sqrt(Pxx_H1),'r',label='H1 strain')
plt.loglog(freqs, np.sqrt(Pxx_L1),'g',label='L1 strain')
plt.axis([fmin, fmax, 1e-24, 1e-19])
plt.grid('on')
plt.ylabel('ASD (strain/rtHz)')
plt.xlabel('Freq (Hz)')
plt.legend(loc='upper center')
plt.title('Advanced LIGO strain data near GW150914')
plt.savefig('GW150914_ASDs.png')

def whiten(strain, interp_psd, dt):
	Nt = len(strain)
	freqs = np.fft.rfftfreq(Nt, dt)

	hf = np.fft.rfft(strain)
	white_hf = hf / (np.sqrt(inter_psd(freqs) / dt / 2.))
	white_ht = npp.fft.irfft(white_hf, n=Nt)
	return white_ht

strain_H1_whiten = whiten(strain_H1, psd_H1, dt)
strain_L1_whiten = whiten(strain_L1, psd_L1, dt)
NR_H1_whiten = whiten(NR_H1, psd_H1, dt)