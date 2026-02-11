import numpy as np
import LWIRImageTool
import os            

def prepare_pixel(arr : np.array, row: int, col: int):
    stack = arr.image_stack
    array_of_avg_coords = arr.find_ascensions(stack, 3, 0.001, [])

    individual_pixel = stack[row,col,:]
    chunk_size = int(individual_pixel.shape[0]*0.001)
    means = []
    for i in range(0,individual_pixel.shape[0], chunk_size):
        chunk = individual_pixel[i:i+chunk_size]
        means.append(chunk.mean())

    first_derivative = np.gradient(individual_pixel)
    second_derivative = np.gradient(first_derivative)

    stdev_first_deriv = np.std(first_derivative)
    stdev_second_deriv = np.std(second_derivative)
    mean_first_deriv = np.mean(first_derivative)
    mean_second_deriv = np.mean(second_derivative)


    n_steps = len(array_of_avg_coords) // 2

    # Preallocate array size
    step_averages = np.zeros(n_steps)
    average_x_vals = np.zeros(n_steps)

    for step in range(n_steps):
        start = array_of_avg_coords[2 * step]
        end = array_of_avg_coords[2 * step + 1]

        # Compute mean over time for all pixels in the step window
        step_averages[step] = np.mean(individual_pixel[start:end])
        average_x_vals[step] = (end+start)//2


    ### Generating blackbody band radiances ###
    blackbody = LWIRImageTool.Blackbody()
    band_radiances = []

    txt_content = np.loadtxt("/home/cjw9009/Desktop/suas_data/FLIRSIRAS_CalData/flir_boson_with_13mm_45fov.txt", skiprows=1, delimiter=',')
    wavelengths = txt_content[:, 0]
    response = txt_content[:, 1]

    for i in range(step_averages.shape[0]):
        temp = 283 + i*5.0
        blackbody.absolute_temperature = temp
        band_radiances.append(blackbody.band_radiance(wavelengths, response))

    ### Applying Linear Regression to find gain and bias terms ###
    gain, bias = np.polyfit(step_averages,band_radiances,1)

    return [individual_pixel, means, first_derivative, second_derivative, average_x_vals, step_averages, band_radiances, gain, bias, row, col, chunk_size]