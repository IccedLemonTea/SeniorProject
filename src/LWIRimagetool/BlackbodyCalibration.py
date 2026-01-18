### Blackbody Class ###
# Author : Cooper White (cjw9009@g.rit.edu)
# Date : 09/30/2025
# File : Blackbody.py


import LWIRimagetool

import os
import numpy as np

class BlackbodyCalibration(LWIRimagetool.CalibrationData):
    def __init__(self,directory,filetype):
        LWIRimagetool.CalibrationData.__init__(self)
        self.regional_average(directory,filetype)


    def regional_average(self,directory,filetype):
        """
        Calculates regional averages based on a blackbody run. 
        See details on how to perform a blackbody run in the README:
            directory(str): Directory containing images from blackbody run
        Returns:
        np.ndarray: Array containing the calibration coefficients for each pixel in the detector

        """

        directory = os.fsencode(directory)
        first_image_path = None
        print(directory)
        # Loop through each image
        for file in sorted(os.listdir(directory)):
            filename = os.fsdecode(file)
            file_path = os.path.join(os.fsdecode(directory), filename)
            if first_image_path is None:
                Factory = LWIRimagetool.ImageDataFactory()
                first_src = Factory.create_from_file(file_path,filetype)
                image_stack = np.array(first_src.raw_counts)
                first_image_path = file_path
            else:
                src = Factory.create_from_file(file_path,filetype)
                image_stack = np.dstack((image_stack,src.raw_counts))
        
        for col in range(image_stack.shape(0)):
            for row in range(image_stack.shape(1)):
                # Slicing one pixel out from the entire image, 
                # keep 3rd dim as it is the temporal element of the pixel
                pixel_vector = image_stack[row,col,:]

                # Average the pixel values along the temporal dim to reduce 
                # calculations 
                # (only necessary for DRS, may need to take another look for RJPEG)
                
                chunk_size = 100 # Should be dependent on total collection time and camera capture rate
                means = np.mean(pixel_vector.reshape(-1, chunk_size), axis=1)
                derivative = np.gradient(means)

                # Vector to hold all values of when the DC noticeably changes
                change_in_temp = [0]

                for i in range(derivative.shape[0]):
                    if derivative[i] >= max(derivative)/2.0: # /2.0 value may need to be adjusted (2 or 3 x stdev(derivative))
                        if change_in_temp is not None:
                            change_in_temp.append(i)
                        else:
                            change_in_temp = []
                            change_in_temp.append(i)

                # Adding end point of derivative vector
                change_in_temp.append(derivative.shape[0])

                # Vector to hold only derivative values that 
                # signal the beginning and end of the temperature change 
                # portion of the blackbody run
                regions = [0]
                for i in range(1,len(change_in_temp)-1,1):
                    if change_in_temp[i+1] > (change_in_temp[i] + 100): # 100 should be generalized, again based on capture rate and total time
                        regions.append(change_in_temp[i])
                        distinct_regions = distinct_regions + 1
                    if change_in_temp[i] > (change_in_temp[i-1] + 100):
                        regions.append(change_in_temp[i])
                regions.append(derivative.shape[0])

                cumulative_dc = 0
                regional_average = []
                count = 0
                # Moving between regions of interest to average
                for i in range(1,len(regions),1):
                    cumulative_dc = 0
                    count = 0
                    if regions[i-1] + 10 < regions[i]: # +10 ensures we don't average a temperature climb
                        # Summing all DC within the regions of interest
                        for j in range(regions[i-1],regions[i],1):
                            # Excluding values that do not have a moderately constant derivative
                            if derivative[j] < 2*np.std(derivative): # < 0.2 should be generalized
                                # print(f"I have found an area to average, and the current block {j} of 100 has a small derivative")
                                for b in range(j*chunk_size,(j+1)*chunk_size,1):
                                    cumulative_dc = cumulative_dc + pixel_vector[b]
                                    count = count + 1
                    if count != 0:
                        regional_average.append(cumulative_dc/count)
                
if __name__ == '__main__':
    import os
    import LWIRimagetool

    directory = "/home/cjw9009/Desktop/Senior_Project/FLIRSIRAS_CalData/20251110_1620"
    filetype = 'envi'
    
    Factory = LWIRimagetool.CalibrationDataFactory()
    Blackbody_Coefficients = Factory.create_from_file(directory, 'blackbody', 'rjpeg')
    

     