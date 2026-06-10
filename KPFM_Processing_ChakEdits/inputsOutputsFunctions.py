import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.ticker import FormatStrFormatter
import os
import numpy as np

def loadtxtFile(file_path:str, rowsSkipped=3)->np.array:
    x_data,y_data = np.loadtxt(file_path,skiprows=rowsSkipped,encoding='utf-8',unpack=True)
    return x_data,y_data

def storeAnalysis(GB_peak_1:float,GB_fwhm_1:float,GB_min_1:float,GB_max_1:float,GI_peak_1:float,GI_fwhm_1:float,GI_min_1:float,GI_max_1:float,peak_diff_1:float,save_path:str,pixels:int,scaleFactor=1):
    # Save Analysis Output
    output_file = os.path.join(save_path, f'GrainBoundaries_analysis_output_{str(pixels*20)}_nm.txt')
    output_lines = [
            f"Analysis for {pixels*20} nm [in mV]:",
            f"Grain boundary peak = {GB_peak_1*scaleFactor}",
            f"Grain boundary fwhm = {GB_fwhm_1*scaleFactor}",
            f"Grain boundary min, max spread = {GB_min_1*scaleFactor}, {GB_max_1*scaleFactor}",
            f"Grain interior peak = {GI_peak_1*scaleFactor}",
            f"Grain interior fwhm = {GI_fwhm_1*scaleFactor}",
            f"Grain interior min, max spread = {GI_min_1*scaleFactor}, {GI_max_1*scaleFactor}",
            f"Diff of GB/GI = {peak_diff_1}",
        ]
    with open(output_file, 'w') as f:
        for line in output_lines:
            f.write(line + '\n')

def save_plot_to_folder(fig, folder_path:str, filename='plot.jpeg'):
    full_path = os.path.join(folder_path, filename)
    fig.tight_layout()
    fig.savefig(full_path, dpi=1000, bbox_inches='tight')
    plt.close(fig)
    #print(f"Plot saved to: {full_path}")

def generateFigures(GB_x_raw:list, GB_x_fit:list, GI_x_raw:list, GI_x_fit:list,GB_y_raw_1:np.array, GB_y_1:np.array, GI_y_raw_1:np.array, GI_y_1:np.array,GB_colour:str,GI_colour:str,save_path:str,datatype:str,pixels:int):
    fig, ax = plt.subplots(1, 1, sharey=True, figsize=(10,8))
    plt.rcParams.update({'font.size': 36}) # Use a slightly smaller font for general text
    
    ax.tick_params(direction='in', length=6)
    ax.tick_params(axis='both')#, labelsize=18)
    #ax.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax.margins(0.05, 0.05) # Reduced margins for a tighter plot
    ax.set_xlabel(f"{datatype} (mV)")#, fontsize=22)
    
    # Calculate limits from all fitted data for consistent scaling
    x_data_all = np.concatenate([GB_x_raw, GB_x_fit, GI_x_raw, GI_x_fit])
    y_data_all = np.concatenate([GB_y_raw_1, GB_y_1, GI_y_raw_1, GI_y_1])
    ax.set_xlim(np.min(x_data_all) - 10, np.max(x_data_all) + 10)
    ax.set_ylabel("Distribution (V$^{-1}$)")#, fontsize=22)
    ax.set_ylim(0, np.max(y_data_all)+5)
    # Limit number of ticks
    ax.xaxis.set_major_locator(MaxNLocator(nbins=5))
    ax.yaxis.set_major_locator(MaxNLocator(nbins=5)) 
    
    # Plotting
    plt.scatter(GB_x_raw, GB_y_raw_1, label=f"GB Data", color=GB_colour, s=30)
    plt.plot(GB_x_fit, GB_y_1, label=f"_nolegend_", color=GB_colour, linewidth=3)
    plt.scatter(GI_x_raw, GI_y_raw_1, label=f"GI Data", color=GI_colour, s=30, marker='s')
    plt.plot(GI_x_fit, GI_y_1, label=f"_nolegend_", color=GI_colour, linewidth=3, linestyle='--')
    
    plt.legend(loc='upper right', fontsize=24)
    
    # Save Plot
    # Assumes save_plot_to_folder is defined and handles the saving
    plot_filename = f'GrainBoundary_Interior_MultiGaussian_{pixels*20}_nm.jpeg'
    save_plot_to_folder(plt.gcf(), save_path, filename=plot_filename)

def CPDPlot(darkData:np.array,illuminatedData:np.array,recoveryData:np.array,FINAL_PLOTS_SAVE_PATH:str,type:str):
    x_nm = [20, 40, 60, 80, 100]
    # 1. Unpassivated CPD Plot
    plt.rcParams.update({'font.size': 36})
    plt.figure(figsize=(10,8))
    ax = plt.gca()
    # ... (Plot formatting identical to original code, but reduced font size for cleaner fit)
    ax.tick_params(direction='in', length=6)
    ax.tick_params(axis='both')#, labelsize=18)
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    plt.xlabel("GB width (nm)")#, fontsize=20)
    plt.ylabel("GI - GB (mV)")#, fontsize=20)
    ax.xaxis.set_major_locator(MaxNLocator(nbins=5))
    ax.yaxis.set_major_locator(MaxNLocator(nbins=5))
    
    plt.scatter(x_nm, darkData, label='Dark', color='#6F6F6F', marker='s', s=50)
    plt.scatter(x_nm, illuminatedData, label='Illuminated', color='#8D1730', marker='o', s=50)
    plt.scatter(x_nm, recoveryData, label='Recovery', color='#003357', marker='^', s=50)
    plt.legend(loc='upper left', fontsize=24)
    plt.tight_layout()
    save_plot_to_folder(plt.gcf(), FINAL_PLOTS_SAVE_PATH, filename=f'FullScatternm_CPD_{type}.jpeg')

def SPVPlot(illuminatedData:np.array,recoveryData:np.array,FINAL_PLOTS_SAVE_PATH:str,type:str):
    x_nm = [20, 40, 60, 80, 100]
    plt.figure(figsize=(10,8))
    ax = plt.gca()
    # ... (Plot formatting)
    ax.tick_params(direction='in', length=6)
    ax.tick_params(axis='both')#, labelsize=18)
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    plt.xlabel("GB width (nm)")#, fontsize=20)
    plt.ylabel(" GI - GB (mV)")#, fontsize=20)
    ax.xaxis.set_major_locator(MaxNLocator(nbins=5))
    ax.yaxis.set_major_locator(MaxNLocator(nbins=5))
    
    plt.scatter(x_nm, illuminatedData, label='Illuminated', color='#8D1730', marker='o', s=50)
    plt.scatter(x_nm, recoveryData, label='Recovery', color='#003357', marker='^', s=50)
    plt.legend(fontsize=24)
    plt.tight_layout()
    save_plot_to_folder(plt.gcf(), FINAL_PLOTS_SAVE_PATH, filename=f'FullScatternm_SPV_{type}.jpeg')

def GIGBPlot(avgGB,avgGB_error,GB_color,avgGI,avgGI_error,GI_color,dictionaryKey:str,FINAL_PLOTS_SAVE_PATH:str):
    errorbar_capsize = 8
    e_linewidth = 1
    legend_font = 12 
    scatter_size = 18

    x_nm = [20, 40, 60, 80, 100]
    plt.figure(figsize=(10,8))
    ax = plt.gca()
    ax.tick_params(direction='in', length=6)
    ax.tick_params(axis='both')
    plt.xlabel("GB width (nm)")
    plt.ylabel(" CPD average (mV)")
    
    ax.margins(0.25, 0.25) # Reduced margins for a tighter plot  
    ax.xaxis.set_major_locator(MaxNLocator(nbins=5))
    ax.yaxis.set_major_locator(MaxNLocator(nbins=5))

    #plt.scatter(x_nm, UnpassGB, label='Unpassivated GB', color='#8D1730', marker='o', s=50)
    #plt.scatter(x_nm, UnpassGI, label='Unpassivated GI', color='#003357', marker='^', s=50)
    plt.errorbar(x_nm, avgGB,yerr= avgGB_error, capsize=errorbar_capsize, elinewidth=e_linewidth,
                  capthick =e_linewidth, label=f'{f"{dictionaryKey}"} GB', color=GB_color, marker='o', markersize=scatter_size, ls = '')
    plt.errorbar(x_nm, avgGI, yerr= avgGI_error, capsize=errorbar_capsize,elinewidth=e_linewidth,
                  capthick =e_linewidth,label=f'{f"{dictionaryKey}"} GI', color=GI_color, marker='^', markersize=scatter_size, ls = '')
    plt.legend(loc = 'best', fontsize=legend_font)
    plt.tight_layout()
    #save_plot_to_folder(plt.gcf(), FINAL_PLOTS_SAVE_PATH, filename='Separate_GB_GI_CPD_Unpassivated_witherror.jpeg')