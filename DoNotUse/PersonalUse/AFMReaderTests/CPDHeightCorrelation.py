# For looking at CPD/Height correlation
from imports_for_code import *
import AFMReaderFunctions as AFMRead
def normalise_npy(data): 
    normalised_data = data/np.max(data)
    return normalised_data


def height_cpd_comparison(height_data, cpd_data):
    height_data = AFMRead.zero_data(AFMRead.median_line_level(AFMRead.plane_level(height_data)))
    height_norm = normalise_npy(height_data)
    cpd_norm = normalise_npy(cpd_data)
    diff_data = height_norm - cpd_norm

    correlation = np.corrcoef(height_data.flatten(), cpd_data.flatten())[0,1]

    print(f"Correlation coefficient is {correlation:.3f}")

    return diff_data, correlation


