# Functions for reading and saving AFM images: 
from AFMReader.ibw import load_ibw
from AFMReader.jpk import load_jpk
#from AFMReader.spm import load_spm
from AFMReader.gwy import load_gwy
import matplotlib as plt
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import traceback

# Use for loading image
def load_image(file_path, filetype = '', channel_name = ''): 
    if filetype == 'ibw': 
        image, pixel_to_nanometre_scaling_factor = load_ibw(file_path, 
                                                            channel_name)
        print(f"Success! {filetype} has loaded")
        return image, pixel_to_nanometre_scaling_factor
    elif filetype == "jpk": 
        image, pixel_to_nanometre_scaling_factor = load_jpk(file_path, 
                                                            channel_name)
        print(f"Success! {filetype} has loaded")
        return image, pixel_to_nanometre_scaling_factor
   # elif filetype == "spm": 
   #     image, pixel_to_nanometre_scaling_factor = load_spm(file_path, 
   #                                                         channel_name)
   #     print(f"Success! {filetype} has loaded")
   #     return image, pixel_to_nanometre_scaling_factor
    elif filetype =="gwy": 
        image, pixel_to_nanometre_scaling_factor = load_gwy(file_path, 
                                                            channel_name)
        print(f"Success! {filetype} has loaded")
        return image, pixel_to_nanometre_scaling_factor
    else: 
        print("Error, please retry.")
        return

# Use to debug and check images. Can copy and save separately to refine formatting. 
def show_image (image_data, scale, channel_name, cmap_label = ''): 

    # Scale adjustment 
    pixels_x, pixels_y = image_data.shape
    x_nm = pixels_x*scale
    y_nm = pixels_y *scale
    fig, ax = plt.subplots(figsize=(6,8))

    im = ax.imshow(
        image_data, 
        cmap = 'gray', 
        origin = 'lower', 
        extent = [0,x_nm, 0, y_nm]
       )
    
    plt.colorbar(im, ax = ax, label = cmap_label)
    plt.title(channel_name)
    plt.xlabel('nm')
    plt.ylabel('nm')

    # Display the plot
    plt.show()
    return fig

# Best to start with if overall image tilt. You can try this with no other processing first. 
def plane_level(image_array):
    # x + y coordinates for each pixel. 
    Y_coords, X_coords = np.indices(image_array.shape)
    
    # Flattening to 2D arrays
    X_flat = X_coords.flatten()
    Y_flat = Y_coords.flatten()
    Z_flat = image_array.flatten()
    
    # Matrix for plane equation
    A = np.c_[X_flat, Y_flat, np.ones_like(X_flat)]
    
    # Solving for best plane fit
    C, _, _, _ = np.linalg.lstsq(A, Z_flat, rcond=None)
    
    # Reconstructing background plane
    background_plane = (C[0] * X_coords) + (C[1] * Y_coords) + C[2]
    
    # Plane subtraction
    leveled_image = image_array - background_plane
    return leveled_image

# Best for low variation across image (i.e. just grains on level surface) 
def polynomial_level(image_array, polynomial_no):

    leveled_image = np.zeros_like(image_array)
    x_pixels = np.arange(image_array.shape[1])
    
    # Loop through each row
    for i, row in enumerate(image_array):
        # Fit n-degree polynomial (a straight line: y = mx + c)
        slope, intercept = np.polyfit(x_pixels, row, polynomial_no)
        
        # Trend for lines
        trend_line = slope * x_pixels + intercept
        
        # line by line subtraction
        leveled_image[i] = row - trend_line
        
    return leveled_image

# Best if you have higher features
def median_line_level(image_array):

    # Use if you have significantly high features.
    # Median calculation
    row_medians = np.median(image_array, axis=1, keepdims=True)
    
    # Row median subtraction
    leveled_image = image_array - row_medians
    return leveled_image

# For iterating through a full folder of data. 
# filetype input MUST be just ibw, gwy, jpk or spm. No other filetypes accepted. Will save files as .npy
def load_from_folder (folder_path, save_path, filetype = '', channel_type = ''):
    if folder_path: 
        sorted_files= sorted(list(Path(folder_path).glob(f"*.{filetype}"))) 
    for file_path in sorted_files:
        try: 
            image, scale = load_image(file_path, filetype, channel_type)

            # For saving
            if save_path: 
                name = Path(file_path).stem
                save_name = f"{save_path}/{name}.npy"
                np.save(save_name, image)
            else: 
                print("No save path, continuing without")

        except Exception as e: 
            # Error printing
            print(f"\n{'='*20} ERROR DETECTED!!!  {'='*20}")
            print(f"Unable to load: {file_path.name}")
            print(f"Error Type: {type(e).__name__}")
            print(f"Details: {e}\n")
            
            print("--- Full Error List ---")
            traceback.print_exc()  # Printing errors line by line
            print(f"{'='*56}\n")
            
            # Stopping code
            raise e
    return 

def npy_to_histogram (file_path, bins_method='auto'): 
    data = np.load(file_path)
    # Flattening into 1D 
    flat_data = data.flatten()
    flat_data = flat_data[np.isfinite(flat_data)]
    
    #Creating histogram: 
    density, bin_edges = np.histogram(flat_data, bins = bins_method, density = True)

    # Finding midpoints
    bin_midpoints = (bin_edges[:-1] + bin_edges[1:]) / 2

    # placing into a 2D array [Matching gwyddion output as closely as possible]
    output_data = np.column_stack((bin_midpoints, density))

    
    # Quick plotting to debug if needed
    #plt.plot(density, bin_midpoints)
    #plt.show()

    return output_data

def setup_directories(root_directory, raw_folder_name = 'raw_data'):
    """Sets up project directory structure.

    Parameters:
    -----------
    root_dir : str or Path
        The main directory containing the raw data folder.
    raw_folder_name : str
        The name of the folder containing raw data (default: 'f1').

    Returns:
    --------
    f1_path, f2_path, f3_path, f4_path : Path objects
        Paths to each respective directory.
    """
    # Clean and parse parent path
    base_path = Path(str(root_directory).strip("'\"").replace("\xa0", " "))

    # Path to the raw data folder (f1)
    f1_path = base_path / raw_folder_name

    # Check if raw data folder exists
    if not f1_path.exists():
        print(f"⚠️ Warning: Raw data directory not found at: {f1_path}")

    # Create target paths for f2, f3, f4
    f2_path = base_path / "npy_files"
    f3_path = base_path / "stats"
    f4_path = base_path / "plots"

    # Create the directories safely without throwing errors if they exist
    for folder in [f2_path, f3_path, f4_path]:
        folder.mkdir(parents=True, exist_ok=True)

    print("Directory structure ready:")
    print(f"  ├── Raw Data (raw): {f1_path}")
    print(f"  ├── npy outputs (npy_files)): {f2_path}")
    print(f"  ├── Individual statistics (stats): {f3_path}")
    print(f"  └── Temporal plots (plots): {f4_path}\n")

    return f1_path, f2_path, f3_path, f4_path