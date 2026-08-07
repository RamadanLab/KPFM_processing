import numpy as np
from scipy.optimize import curve_fit
from pathlib import Path
import os
# Exponential fitting for time series
# Fitting exponentials 
def adjusted_exponential(t, A, tau, const):
    return A*(1-np.exp(-(t/tau)))+const

def d_adjusted_exponential(t, A, tau):
    return (A/tau)*np.exp(-t/tau)

def exponential_fitting (peaks, time, save_path = None, measurement = '', peakscale = ''): 
    # Uncomment to check if plotting correct stuff
    #print(peaks)
    #print(time)

    if peakscale == 'V':
        adjusted_peaks = [round(x*1000,4) if not np.isnan(x) else np.nan for x in peaks]
    elif peakscale == 'mV': 
        adjusted_peaks = peaks
    else: 
        print("Error, set peakscale as either V or mV")
    A_initial = np.max(adjusted_peaks)#If data is positive then this should be max, if negative then it is min
    tau_initial= np.median(time) #Can also try max/2 or mean to see if this works
    const_initial=np.min(adjusted_peaks)
    print(f"Constant initial = {const_initial:.2f}")
    initial_guess = [A_initial,tau_initial, const_initial]  # Initial guess for A, tau, const
    params, covariance = curve_fit(adjusted_exponential,time, adjusted_peaks, p0=initial_guess, maxfev=1000000)
    cutoff = 0.01
    # Extract the parameters (A, tau, beta)
    A, tau, const = params


    if len(time) < 100: # if using a short time series where fitting won't look smooth. 
        x_fit= np.linspace(np.min(time), np.max(time), 1000000)
        y_fit = np.array([adjusted_exponential(np.array([x]), *params)[0] for x in x_fit])
        dy_fit = np.array([d_adjusted_exponential(np.array([x]), A, tau)[0] for x in x_fit])
        time_cst = x_fit[np.where(dy_fit < cutoff)[0][0]]
        fit_outputs = np.column_stack((peaks, time, x_fit, y_fit))
        if save_path: 
            # Saving all data 
            with open(save_path, 'w', encoding='utf-8') as f:
            # Header lines
                f.write(f"Time   Raw {measurement}  Fit time   Fitted {measurement}   \n")
                f.write(f"[(s)]     [({peakscale})]  [(s)] [({peakscale})]     \n")
                    
                # Write data rows (z, ρ)
                for t, y, y_f in zip(time, peaks, y_fit):
                    f.write(f"{t:<13.8g} {y:<13.8g} {y_f:<13.8g}\n")      
        else: 
            print(f'No save path given, printing details below: \n', 
                      f'Peaks, time, fitting\n',
                      f'{fit_outputs}')

    else: # For if there are 100 or more points
        y_fit = np.array([adjusted_exponential(np.array([x]), *params)[0] for x in time])
        dy_fit = np.array([d_adjusted_exponential(np.array([x]), A, tau)[0] for x in time])
        time_cst = time[np.where(dy_fit < cutoff)[0][0]]
        fit_outputs = np.column_stack((peaks, time, y_fit))
        if save_path: 
            # Saving all data 
            with open(save_path, 'w', encoding='utf-8') as f:
            # Header lines
                f.write(f"Time   Raw {measurement}  Fitted {measurement}   \n")
                f.write(f"[(s)]     [({peakscale})]   [({peakscale})]      \n")
            
                # Write data rows (z, ρ)
                for t, y, y_f in zip(time, peaks, y_fit):
                    f.write(f"{t:<13.8g} {y:<13.8g} {y_f:<13.8g}\n")

        else: 
            print(f'No save path given, printing details below: \n', 
                f'Peaks, time, fitting\n',
                f'{fit_outputs}')

    perr=np.sqrt(np.diag(covariance))
    SPV_sat_err = np.sqrt(perr[0]**2+perr[2]**2)

    fit_params = ("Fitted Parameters:\n", 
               f"A = {A:.2f}, error = {perr[0]}\n", 
               f"tau = {tau:.2f}, error = {perr[1]}\n", 
               f"C = {const:.2f}, error = {perr[2]}\n", 
               f"time constant = {time_cst:.2f}\n", 
               f"SPV_sat = {A+const}, error = {SPV_sat_err}"
    )

    if save_path is not None:
        output_file = os.path.join(save_path, f'Fitting_params_{measurement}.txt')
        with open(output_file, 'w') as f: 
           f.write(fit_params)
        print (f" Fitting params saved as Fitting_params_{measurement}.txt")
        print(fit_params)
    else: 
        print("Cannot save fitting parameters, printing below")
        print(fit_params)
    
    return fit_outputs # Outputting x, y, x_fit (if <100 points), y_fit. 