import numpy as np
from scipy.ndimage import gaussian_filter1d
from scipy.signal import find_peaks
from scipy.optimize import curve_fit
import os
import matplotlib.pyplot as plt
from pathlib import Path
import AFMReaderFunctions

def extract_and_save_params(popt, pcov, perr, file_path, save_path):

    # Extract Gaussian parameters
    gaussians = []
    for i in range(len(popt) // 3):
        amp = popt[i*3] # Amplitude
        cen = popt[i*3+1] # Mu (peak centre)
        wid = abs(popt[i*3+2]) # Sigma
        gaussians.append({'amp': amp, 'cen': cen, 'wid': wid})
    
    # Identify the highest peak
    highest = gaussians[np.argmax([g['amp'] for g in gaussians])]
    sigma=highest['wid']
    fwhm = 2.355 *sigma # to make mV
    x_left = highest['cen'] - fwhm / 2
    x_right = highest['cen'] + fwhm / 2
    fwhm_err = perr[2]*2.355

        # Store in lists for output

    # Optional: print for debugging
    # 3. Create the summary text for the plot
    statistics=(f"Peak: {highest['cen']*1000:.3f} mV\n"
                f"Error: {np.sqrt(pcov[1,1])*1000:.3f}mV\n"
              f"FWHM: {fwhm*1000:.2f} mV\n"
              f"Error: {np.sqrt(pcov[2,2])*2.355*1000:.3f}mV\n"
              f"FWHM Bounds: [{x_left*1000:.2f}, {x_right*1000:.2f}]mV\n"
              f"Sigma: {sigma*1000:.3f} mV\n"
              f"Error: {np.sqrt(pcov[2,2])*1000:.3f}mV\n")
    # print(statistics)

    if save_path is not None:
        name = Path(file_path).stem
        output_file = os.path.join(save_path, f'{name}_stats.txt')
        with open(output_file, 'w') as f: 
           f.write(statistics)
    else: 
        print("Cannot save statistics, continuing")
    #Final A, mu, sigma, FWHM: 
    vals = [highest['amp'],highest ['cen'], sigma]
    spread = [fwhm, fwhm_err, x_left, x_right]
    return vals, spread

def gaussian(x, A, mu, sigma): # This is redundant, multigaussian will fit a single if no other peaks are found
    return A * np.exp(-(x - mu)**2 / (2 * sigma**2))

# Function to model N Gaussians
def multi_gaussian(x, n_peaks, *params):
    n = len(params) // n_peaks
    y = np.zeros_like(x)
    for i in range(n):
        amp = params[i * 3]
        cen = params[i * 3 + 1]
        wid = params[i * 3 + 2]
        y += amp * np.exp(-((x - cen) ** 2) / (2 * wid ** 2))
    return y

def estimate_guess_from_data(x, y, n_peaks, prominence=0.1, distance=10):
    y_smooth = gaussian_filter1d(y, sigma=2)
    peaks, _ = find_peaks(y_smooth, prominence=prominence, distance=distance)
    
    # Sort peaks by height (amplitude) and limit to top 2
    if len(peaks) > n_peaks:
        #sorted_indices = np.argsort(properties['prominences'])[::-1][:2]
        sorted_indices = np.argsort(y_smooth[peaks])[::-1][:2]
        peaks = peaks[sorted_indices]

    guess = []
    for i in peaks:
        amp = y[i]
        cen = x[i]
        x_range = np.ptp(x)
        wid =x_range/50 # Adjust based on data
        guess += [amp, cen, wid]
    
    return guess, len(peaks)

def fitting_individual_file(file_path, rows, peak_guess, save_path=None):

    #print(f"\nProcessing file: {filename}") #Use if you want each individual file processed 
    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
        data = np.loadtxt(f, skiprows=rows)

    # Separating data:
    x_data = data[:, 0]
    y_data = data[:, 1]

    # Estimate initial guess and peak count based of personal peak number
    initial_guess, n_peaks = estimate_guess_from_data(x_data, y_data, peak_guess)

    # Find fitting parameters:
    popt, pcov = curve_fit(multi_gaussian, x_data, y_data, p0=initial_guess, maxfev=1000000)

    # Using x_fit if datapoints are low to improve fitting
    if len(x_data) < 2000: 
        x_fit= np.linspace(np.min(x_data), np.max(x_data), 10000)
        y_fit=multi_gaussian(x_fit, n_peaks, *popt)
    else: 
        y_fit=multi_gaussian(x_data, n_peaks, *popt)

    #Find errors for A, mu, sigma from pcov. 
    perr=np.sqrt(np.diag(pcov))
    
    #Extracting and saving params: 
    vals, spread = extract_and_save_params(popt, pcov, perr, file_path, save_path)

    params = [x_data, y_data, x_fit, y_fit, popt, pcov, perr]
    return params, vals, spread
    plt.show()


def fitting_folder (file_directory, im_time = None, peak_guess = None, save_path = None):
    gaussian_peaks= []
    time = []
    x_left = []
    x_right = []
    # Setting x_data for time series
    if image_time: 
        image_time = im_time
    else: 
        image_time = 1
    
    for filename in enumerate(files, desc="Processing files"):
            files=sorted([f for f in os.listdir(file_directory) if f.endswith('.txt')])
            file_path = os.path.join(file_directory, filename)
            npy_data = np.load(file_path)
            data = AFMReaderFunctions.npy_to_histogram(npy_data)
            #print(f"\nProcessing file: {filename}")
            # Separate data 
            x_data = data[:, 0]
            y_data = data[:, 1]

            # Estimate initial guess and peak count based of personal peak number
            initial_guess, n_peaks = estimate_guess_from_data(x_data, y_data, peak_guess)
            # Find fitting parameters:
            popt, pcov = curve_fit(multi_gaussian, x_data, y_data, p0=initial_guess, maxfev=1000000)
            
            # Using x_fit if datapoints are low to improve fitting
            if len(x_data) < 2000: 
                x_fit= np.linspace(np.min(x_data), np.max(x_data), 10000)
                y_fit=multi_gaussian(x_fit, n_peaks, *popt)
            else: 
                y_fit=multi_gaussian(x_data, n_peaks, *popt)
            
            #Find errors for A, mu, sigma from pcov. 
            perr=np.sqrt(np.diag(pcov))
                
            #Extracting and saving params: 
            vals, spread = extract_and_save_params(popt, pcov, perr, file_path, save_path)

            gaussian_peaks.append(vals[1])
            x_left.append(spread[2])
            x_right.append(spread[3])
            t += image_time
            time.append(t)
            print(f"Completed fitting for {filename}")

    return gaussian_peaks, time, x_left, x_right

