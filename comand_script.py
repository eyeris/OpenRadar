import numpy as np
import pyrealsense2 as rs
import matplotlib.pyplot as plt     
from datetime import datetime
from mmwave.dataloader import DCA1000

NUM_TX = 3
NUM_RX = 4
CHIRP_LOOPS = 128
NUM_ADC_SAMPLES = 149

# Data sampling configuration
c = 3e8 # Speed of light (m/s)
sample_rate = 3000 # Rate at which the radar samples from ADC (ksps - kilosamples per second)
freq_slope = 60.06 # Frequency slope of the chirp (MHz/us)
adc_samples = 149 # Number of samples from a single chirp

start_freq = 77.0 # Starting frequency of the chirp (GHz)
idle_time = 7 # Time before starting next chirp (us)
ramp_end_time = 58.57 # Time after sending each chirp (us)

# Range resolution
range_res = (c * sample_rate * 1e3) / (2 * freq_slope * 1e12 * NUM_ADC_SAMPLES)
print(f'Range Resolution: {range_res} [meters]')

# Maximum Range
max_range = (c * sample_rate * 1e3) / (2 * freq_slope * 1e12)
print(f'Maximum Range: {max_range} [meters]')

# Make sure your equation translates to the following
velocity_res = c / (2 * start_freq * 1e9 * (idle_time + ramp_end_time) * 1e-6 * CHIRP_LOOPS * NUM_TX)
print(f'Velocity Resolution: {velocity_res} [meters/second]')

ranges = np.arange(adc_samples) * range_res

dca = DCA1000()

def mmwave_data_collection():
    i = 0
    radar_list = []
    time_list = []
    while True:
        i = i + 1
        try:
            adc_data = dca.read(1)
            #frame3d = dca.organize(adc_data, CHIRP_LOOPS, NUM_RX*NUM_TX, NUM_ADC_SAMPLES)

            radar_list.append(adc_data)
            # range_plot = np.fft.fft(frame3d, axis=2)
            # range_bins = np.abs(range_plot).sum(1)
            # powers = 10*np.log10(np.abs(range_bins.T))

            # # #range_cube = mm.dsp.range_processing(frame3d)

            # clear_output(wait=True)
            # plt.plot(ranges, powers) 
            # plt.xlabel('Range in m')
            # plt.ylabel('Reflected Power')
            # plt.show()
            # plt.clf()
            # print("Success")

            # range_fft = np.fft.fft(frame3d, axis=2)
            # range_doppler = np.fft.fft(range_fft, axis=0)
            # range_doppler = np.fft.fftshift(range_doppler, axes=0)
            # range_doppler = np.log(np.abs(range_doppler)).sum(1)

            # plt.imshow(range_doppler.T)
            # plt.xlabel('Doppler Bins')
            # plt.ylabel('Range Bins')
            # plt.title('Analyzing the Range-Doppler Heatmap')
            # plt.show()
            # plt.clf()
            # print("Success")

            datetime_object = datetime.now()
            time_list.append(datetime_object)
            print(datetime.now(), "Done frame", i)
            # if i == 200:
            #     break;
        except:
            print("Timeout occured")
            arr_1 = np.asarray(radar_list)
            arr_2 = np.asarray(time_list)
            print(arr_1.shape)
            print("Saving")
            np.savez("radar_cam_100_frames.npz",arr_1,arr_2)
            break;

mmwave_data_collection()