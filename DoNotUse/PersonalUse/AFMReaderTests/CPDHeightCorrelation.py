# For looking at CPD/Height correlation
from imports_for_code import *
import AFMReaderFunctions as AFMRead
def normalise_npy(data): 
    normalised_data = data/np.max(data)
    return normalised_data


def height_cpd_comparison(height_data, cpd_data, height_scale, cpd_scale):
    # Checks input plots, uncomment if not needed. 
    print("Pre-processed data")
    print(f"Min height = {np.min(height_data)}, max height = {np.max(height_data)} ")
    print(f"Min cpd = {np.min(cpd_data)}, max cpd = {np.max(cpd_data)} ")
    fig1 = AFMRead.show_image(height_data, height_scale, channel_name="Height", cmap_color="magma", cmap_label = "Height (nm)")
    fig2 = AFMRead.show_image(cpd_data, cpd_scale, channel_name = "CPD", cmap_color='viridis', cmap_label= "CPD(mV)")

    height_norm = normalise_npy(height_data)

    cpd_norm = normalise_npy(cpd_data)
    print("normalised data")
    print(f"Min norm height = {np.min(height_norm)}, max norm height = {np.max(height_norm)} ")
    print(f"Min norm cpd = {np.min(cpd_norm)}, max norm cpd = {np.max(cpd_norm)} ")
    fig3 = AFMRead.show_image(height_norm, height_scale, channel_name="Height norm", cmap_color="magma", cmap_label = "Height (nm)")
    fig4 = AFMRead.show_image(cpd_norm, cpd_scale, channel_name = 'CPD', cmap_color='viridis', cmap_label = 'CPD norm (V)' )
    diff_data = height_norm - cpd_norm
    fig5 = AFMRead.show_image(diff_data, channel_name="Difference map", cmap_color = "bwr", cmap_label = "Norm. diff")
    
    correlation = np.corrcoef(height_data.flatten(), cpd_data.flatten())[0,1]

    print(f"Correlation coefficient is {correlation:.3f}")

    return diff_data, correlation


