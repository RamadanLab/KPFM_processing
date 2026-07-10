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

# --- Gaussian fitting---
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

def estimate_guess_from_data(x:np.array, y:np.array, prominence=0.1, distance=10):
    y_smooth = gaussian_filter1d(y, sigma=2)
    peaks, properties = find_peaks(y_smooth, prominence=prominence, distance=distance)
    # Sort peaks by height (amplitude) and limit to top 2
    if len(peaks) > 2:
        sorted_indices = np.argsort(properties['prominences'])[::-1][:2]
        peaks = peaks[sorted_indices]

    guess = []
    for i in peaks:
        amp = y[i]
        cen = x[i]
        wid = 0.001 # Adjust based on data
        guess += [amp, cen, wid]
    
    return guess, len(peaks)

#Averaging and errors: 
def averaging_for_mean(dataSet:np.array):
    measurements = dataSet.shape[1]
    error = np.std(dataSet,axis=1)/np.sqrt(measurements)
    mean = np.mean(dataSet,axis=1)
    return mean,error

def calcAverage(valDict:dict,kind:str)->dict:
    y_peaks_adjusted = []
    GB_peaks_adjusted = []
    GI_peaks_adjusted = []

    for i in valDict.values():
        y_peaks_adjusted.append(i["y_peaks_adjusted"])
        GB_peaks_adjusted.append(i["GB_peaks_adjusted"])
        GI_peaks_adjusted.append(i["GI_peaks_adjusted"])


    #Averaging and finding errors for difference: 
    y_peaks_all, y_peaks_error = averaging_for_mean(np.asarray(y_peaks_adjusted))
    avgGB, avgGB_error = averaging_for_mean(np.asarray(GB_peaks_adjusted))
    avgGI, avgGI_error = averaging_for_mean(np.asarray(GI_peaks_adjusted))

    resultDict={}
    resultDict[f"{kind}"]={"y_peaks_all":y_peaks_all,"y_peaks_error":y_peaks_error,"avgGB":avgGB,"avgGB_error":avgGB_error,"avgGI":avgGI,"avgGI_error":avgGI_error}
    return resultDict