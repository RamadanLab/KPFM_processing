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
