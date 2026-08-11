# Plotting functions
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.lines as mlines
import matplotlib.cm as cm
from matplotlib.ticker import MaxNLocator
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.colors import ListedColormap
import os 
from pathlib import Path

def save_plot_to_folder(fig, folder_path, filename='plot.jpeg'):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)  # Create the folder if it doesn't exist
    
    full_path = os.path.join(folder_path, filename)
    fig.tight_layout()
    fig.savefig(full_path, dpi=600, bbox_inches='tight')
    print(f"Plot saved to: {full_path}")

def hex_to_RGB(hex_str):
    
    """ #FFFFFF -> [255,255,255]"""
    
    return [int(hex_str[i:i+2], 16) for i in range(1,6,2)]

def get_color_gradient(n, c1= None, c2 = None):
    #Add automated if no colours given
    assert n > 1
    c1_rgb = np.array(hex_to_RGB(c1))/255
    c2_rgb = np.array(hex_to_RGB(c2))/255
    mix_pcts = [x/(n-1) for x in range(n)]
    rgb_colors = [((1-mix)*c1_rgb + (mix*c2_rgb)) for mix in mix_pcts]
    return ["#" + "".join([format(int(round(val*255)), "02x") for val in item]) for item in rgb_colors]

def plot_gaussian(x, y, x_fit, 
                  x_left = None, x_right = None, 
                  save_path = None, color = None,
                  measurement = '', scale = '', 
                  savename = ''):

    # Add if statements if no spread given.  
    if scale == 'V': 
        x = [round(i*1000,4) if not np.isnan(i) else np.nan for i in x]
        x_fit = [round(i*1000,4) if not np.isnan(i) else np.nan for i in x_fit]
        x_left = [round(i*1000,4) if not np.isnan(i) else np.nan for i in x_left]
        x_right = [round(i*1000,4) if not np.isnan(i) else np.nan for i in x_right]
    elif scale == "mV": 
        x = x
        x_fit = x_fit
        x_left =x_left
        x_right = x_right
    else: 
        print("Please correct scale input to either V or mV")

    if color: 
        color = color
    else: 
        color = 'red'

    # All plotting parameters: 
    dpi_setting = 600
    figsize_x, figsize_y = (2227/dpi_setting), (1498/dpi)
    fig, ax = plt.subplots(1, 1, sharey=True, figsize=(figsize_x, figsize_y))

    ax.margins (0.5,0.5) 
    tick_length = 6
    legend_font = 12
    base_font_size = 12
    scatter_size = 6
    line_width = 1.5
    ax = plt.gca()

    # Tick editing
    ax.tick_params(direction='in', axis = 'both', length=tick_length, labelsize = base_font_size)
    ax.xaxis.set_major_locator(MaxNLocator(nbins=5))  # Max 5 ticks on x-axis
    ax.yaxis.set_major_locator(MaxNLocator(nbins=5))  # Max 5 ticks on y-axis
    ax.autoscale(enable=None, axis="x", tight=True)
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(line_width)

    ax.set_ylim(0,500)
    ax.set_xlim(-y*3,*150)
    plt.xlabel("Time (s)")
    plt.ylabel(f"{measurement}({scale})")

    # main plotting: 
    plt.plot(y,x_fit,'-', label = 'Average SPV', color=color, linewidth=line_width)
    plt.plot(y, x_left, color='#6F6F6F', linewidth=0.0001)
    plt.plot(y, x_right, color='#6F6F6F', linewidth=0.0001)

    # Shaded regions for spread 
    if x_left: 
        plt.fill_between(x, x_left, x_right, color='#6F6F6F',
                 alpha=0.3)
    else: 
        print("No spread given. Plotting standard line plot.")


    if save_path: 
        fig=plt.gcf()
        plt.tight_layout()
        save_plot_to_folder(fig, save_path,filename=f"{savename}.jpeg")
        
    plt.show()
        
def waterfall_gaussian(x, y, x_fit, 
                       save_path = None, 
                       c1 = None, c2 = None, 
                       scale = '', measurement = ''): 
    # Add if statements for save path as normal
    # Add automation if no colours are given
    if scale == 'V': 
            x = [round(i*1000,4) if not np.isnan(i) else np.nan for i in x]
            x_fit = [round(i*1000,4) if not np.isnan(i) else np.nan for i in x_fit]
    elif scale == "mV": 
        x=x
        x_fit = x_fit
    else: 
        print("Please correct scale input to either V or mV")

def time_series_plot(x_fit, y, 
                     x_left = None, x_right = None, 
                     cutoff_line1 = None, cutoff_line2 = None, 
                     save_path = None, savename = None,
                     color = None,
                     measurement = None, scale = None): 

    '''if scale == 'V': 
        x_fit = [round(i*1000,4) if not np.isnan(i) else np.nan for i in x_fit]
        x_left = [round(i*1000,4) if not np.isnan(i) else np.nan for i in x_left]
        x_right = [round(i*1000,4) if not np.isnan(i) else np.nan for i in x_right]
    elif scale == 'mV': 
        x_fit = x_fit
        x_left = x_left
        x_right = x_right
    else: 
        print("Please correct scale input to either V or mV")'''

    if color: 
        color = color
    else: 
        color = 'red'

    # All plotting parameters: 
    dpi_setting = 600    
    tick_length = 6
    base_font_size = 12
    line_width = 1.5
    figsize_x, figsize_y = (2227/dpi_setting), (1498/dpi_setting)
    fig, ax = plt.subplots(1, 1, sharey=True, figsize=(figsize_x, figsize_y))

    ax.margins (0.5,0.5) 

    ax = plt.gca()

    # Tick editing
    ax.tick_params(direction='in', axis = 'both', length=tick_length, labelsize = base_font_size)
    ax.xaxis.set_major_locator(MaxNLocator(nbins=5))  # Max 5 ticks on x-axis
    ax.yaxis.set_major_locator(MaxNLocator(nbins=5))  # Max 5 ticks on y-axis
    ax.autoscale(enable=None, axis="x", tight=True)
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(line_width)

    #Dynamic bounds 
    xbound_top, xbound_bottom = (np.max(x_right)*1.1),(np.min(x_left)*0.9)
    ybound_left, ybound_right = np.min(y), np.max(y)
    ax.set_ylim(xbound_bottom, xbound_top)
    ax.set_xlim(ybound_left, ybound_right)

    # Axis labels
    plt.xlabel("Time (s)")
    plt.ylabel(f"{measurement}(mV)")

    # main plotting: 
    plt.plot(y,x_fit,'-', label = 'Average SPV', color=color, linewidth=line_width)
    plt.plot(y, x_left, color='#6F6F6F', linewidth=0.0001)
    plt.plot(y, x_right, color='#6F6F6F', linewidth=0.0001)

    # Shaded regions for spread 
    if x_left: 
        plt.fill_between(y, x_left, x_right, color='#6F6F6F',
                 alpha=0.3)
    else: 
        print("No spread given. Plotting standard line plot.")

     
    # Adding vlines for light off and light on indication. 
    if cutoff_line1: # Start cutoff line
        plt.vlines(x=y[cutoff_line1],
            ymin=xbound_bottom, 
            ymax = xbound_top,
            linestyle = '--',
            linewidth=1,
            color = 'black'
                )
    else: 
        print("No light off time given, assuming no vlines needed.")

    if cutoff_line2: # end cutoff line 
        plt.vlines(x=y[cutoff_line2],
                ymin=xbound_bottom, 
                ymax=xbound_top,
                linestyle = '--',
                linewidth=1,
                color = 'black'
                 )

    if save_path: 
        fig=plt.gcf()
        plt.tight_layout()
        save_plot_to_folder(fig, save_path,filename=f"{savename}.jpeg")
        plt.show()
        return
    else: 
        print("No save path given.")
        plt.show() 
        return
    
        

    
def stretched_exp_plot (x, y, x_fit, y_fit = None, 
                        save_path = None, 
                        color = None, 
                        measurement = '', scale = '',): 
        # need to add: 
    # If statement for the spread
    # Add standard if statement for save_path
    # Add error if no measurement.
    if scale == 'V': 
        x = [round(i*1000,4) if not np.isnan(i) else np.nan for i in x]
        x_fit = [round(i*1000,4) if not np.isnan(i) else np.nan for i in x_fit]
    elif scale == "mV": 
        x=x
        x_fit = x_fit
    else: 
        print("Please correct scale input to either V or mV")

def compare_gaussians(x1, y1, x_fit1, 
                    x2, y2, x_fit2,
                  save_path = None, 
                  measurement = '', scale = ''): 
    if scale == 'V': 
        x1 = [round(i*1000,4) if not np.isnan(i) else np.nan for i in x1]
        x_fit1 = [round(i*1000,4) if not np.isnan(i) else np.nan for i in x_fit1]
        x2 = [round(i*1000,4) if not np.isnan(i) else np.nan for i in x2]
        x_fit2 = [round(i*1000,4) if not np.isnan(i) else np.nan for i in x_fit2]
    elif scale == "mV": 
        x1=x1
        x_fit1 = x_fit1
        x2=x2
        x_fit2 = x_fit2
    else: 
        print("Please correct scale input to either V or mV")
