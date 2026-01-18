file_path = '/home/cjw9009/Desktop/Senior_Project/FLIRSIRAS_CalData/flir_boson_with_13mm_45fov.txt'
import numpy as np
import LWIRimagetool

### GENERATING BLACKBODY BAND RADIANCES ###
blackbody = LWIRimagetool.Blackbody()
txt_content = np.loadtxt(file_path,skiprows=1,delimiter=',')
wavelengths = np.linspace(8,14,10000)
# wavelengths = txt_content[:,0]
response = txt_content[:,1]
band_radiances = []
for i in range(13):
    temp = 283 + i*5.0 # Assumes that the blackbody run is moving by 5 degree steps -- may need to make this adjustable
    blackbody.absolute_temperature = temp
    band_radiances.append(blackbody.band_radiance(wavelengths))
    print(f"the radiance is {blackbody.band_radiance(wavelengths)} for temp {temp}")