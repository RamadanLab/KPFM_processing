import numpy as np
from scipy.ndimage import gaussian_filter1d
from scipy.signal import find_peaks
from scipy.optimize import curve_fit

def gaussian(x, A, mu, sigma):
    return A * np.exp(-(x - mu)**2 / (2 * sigma**2))

# Function to model N Gaussians
def multi_gaussian(x, *params):
    n = len(params) // 3
    y = np.zeros_like(x)
    for i in range(n):
        amp = params[i * 3]
        cen = params[i * 3 + 1]
        wid = params[i * 3 + 2]
        y += amp * np.exp(-((x - cen) ** 2) / (2 * wid ** 2))
    return y

def multi_gaussian_folder(file_path, rows, name, save_path=None, measurement=''):
    results = []
    #print(f"\nProcessing file: {filename}") #Use if you want each individual file processed

    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
        data = np.loadtxt(f, skiprows=rows)

    x_data = data[:, 0]
    y_data = data[:, 1]
    # Estimate initial guess and peak count
    initial_guess, n_peaks = estimate_guess_from_data(x_data, y_data)
    # Uncomment if you want to use a specific number of points for fitting (or if there are few raw data points)
    #x_fit= np.linspace(np.min(x_data), np.max(x_data), 1000000)
    popt, pcov = curve_fit(multi_gaussian, x_data, y_data, p0=initial_guess, maxfev=1000000)
    y_fit=multi_gaussian(x_data,*popt)
    peak_index_max=np.argmax(y_fit)
    x_peak_centre=x_data[peak_index_max]
    perr=np.sqrt(np.diag(pcov))
    #For finding min and max *i.e. either side of the peaks. 
    # Extract Gaussian parameters
    gaussians = []
    for i in range(len(popt) // 3):
        amp = popt[i*3]
        cen = popt[i*3+1]
        wid = abs(popt[i*3+2])
        gaussians.append({'amp': amp, 'cen': cen, 'wid': wid})
    
    # Identify the highest peak
    highest = gaussians[np.argmax([g['amp'] for g in gaussians])]
    sigma=highest['wid']
    fwhm = 2.355 *sigma # to make mV
    x_left = highest['cen'] - fwhm / 2
    x_right = highest['cen'] + fwhm / 2
    
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
        
    print(statistics) 

    if save_path is not None:
        output_file = os.path.join(save_path, f'Statistics_{name}.txt')
        with open(output_file, 'w') as f: 
           f.write(statistics)
    else: 
        print("Cannot save statistics, continuing")
    params = [x_data, y_data, y_fit, statistics, perr]
    return x_data, y_data, y_fit, statistics, perr
    plt.show()
def fit_gaussian (x_data:np.array,y_data:np.array)->np.array:
    # Estimate initial guess and peak count (Assumes estimate_guess_from_data is defined) Multigaussian
    #initial_guess, n_peaks = estimate_guess_from_data(x_data, y_data)
    #popt, _ = curve_fit(multi_gaussian, x_data, y_data, p0=initial_guess, maxfev=100000000)
    #Estimate initial guess Single gaussian
    initial_guess = [max(y_data), np.mean(x_data), np.std(x_data)]
    popt, pcov = curve_fit(gaussian, x_data, y_data, p0=initial_guess, maxfev=100000000)

    x_fit= np.linspace(np.min(x_data), np.max(x_data), 1000000)
    #y_fit=multi_gaussian(x_fit,*popt)
    y_fit=gaussian(x_fit,*popt)
    peak_index_max=np.argmax(y_fit)
    peak_centre=x_fit[peak_index_max]
    
    # Extract Gaussian parameters
    gaussians = []
    for i in range(len(popt) // 3):
        amp = popt[i*3]
        cen = popt[i*3+1]
        wid = abs(popt[i*3+2])
        gaussians.append({'amp': amp, 'cen': cen, 'wid': wid})

    highest = gaussians[np.argmax([g['amp'] for g in gaussians])]
    fwhm = 2.355 * highest['wid']
    
    return x_data, y_data, x_fit, y_fit, peak_centre, fwhm


# Fitting exponentials 
def adjusted_exponential(t, A, tau, const):
    return A*(1-np.exp(-(t/tau)))+const

def d_adjusted_exponential(t, A, tau):
    return (A/tau)*np.exp(-t/tau)

def exponential_fitting (peaks, x_data, ): 
    print(peaks)
    print(x_data)