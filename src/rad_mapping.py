import numpy as np
import LWIRimagetool as lit
import matplotlib.pyplot as plt


### BLACKBODY CALCULATIONS ###
n_steps = 13


band_radiances = np.zeros(n_steps)
temperatures = 283.15 + np.arange(n_steps) * 5.0 # 5 and 283 are hardcoded, need to adjust [K]
bb = lit.Blackbody()

rsr_filename = "/home/cjw9009/Desktop/Senior_Project/FLIRSIRAS_CalData/flir_boson_with_13mm_45fov.txt"

txt_content = np.loadtxt(rsr_filename, skiprows=1, delimiter=',')
wavelengths = txt_content[:, 0]
response = txt_content[:, 1]

for i, temp in enumerate(temperatures):
    bb.absolute_temperature = temp # [K]
    band_radiances[i] = bb.band_radiance(wavelengths, response)

cal_array = np.load("/home/cjw9009/Desktop/Senior_Project/20251202_1400_fullimage_bbrun_refactored_calarray.npy")
print(f"{cal_array}")
images = np.load("/home/cjw9009/Desktop/Senior_Project/src/20251202_1400_Cal_Work/20251202_1400_fullimage_bbrun.npy")


corrected_images = np.empty(images.shape)

for c in range(images.shape[1]):
            for r in range(images.shape[0]):
                corrected_images[r,c,:] = images[r,c,:]*cal_array[r,c,0] + cal_array[r,c,1]


fig, axs = plt.subplots(3, 5, figsize=(16, 9), constrained_layout=True)

error_1 = abs((corrected_images-band_radiances[0])/(band_radiances[0])*100)
im_1 = axs[0,0].imshow(error_1[:,:,100],vmin=0, vmax=2)
axs[0,0].set_title(f"BB Temp {temperatures[0]-273.15}BB Rad {band_radiances[0]:.2f}")
fig.colorbar(im_1, ax=axs[0,0], label="Rad Percent Difference")

error_2 = abs((corrected_images-band_radiances[1])/(band_radiances[1])*100)
im_2 = axs[0,1].imshow(error_2[:,:,260],vmin=0, vmax=2)
axs[0,1].set_title(f"BB Temp {temperatures[1]-273.15}   BB Rad {band_radiances[1]:.2f}")
fig.colorbar(im_2, ax=axs[0,1], label="Rad Percent Difference")

error_2 = abs((corrected_images-band_radiances[2])/(band_radiances[2])*100)
im_2 = axs[0,2].imshow(error_2[:,:,420],vmin=0, vmax=2)
axs[0,2].set_title(f"BB Temp {temperatures[2]-273.15}   BB Rad {band_radiances[2]:.2f}")
fig.colorbar(im_2, ax=axs[0,2], label="Rad Percent Difference")

error_2 = abs((corrected_images-band_radiances[3])/(band_radiances[3])*100)
im_2 = axs[0,3].imshow(error_2[:,:,580],vmin=0, vmax=2)
axs[0,3].set_title(f"BB Temp {temperatures[3]-273.15}   BB Rad {band_radiances[3]:.2f}")
fig.colorbar(im_2, ax=axs[0,3], label="Rad Percent Difference")

error_2 = abs((corrected_images-band_radiances[4])/(band_radiances[4])*100)
im_2 = axs[0,4].imshow(error_2[:,:,740],vmin=0, vmax=2)
axs[0,4].set_title(f"BB Temp {temperatures[4]-273.15}   BB Rad {band_radiances[4]:.2f}")
fig.colorbar(im_2, ax=axs[0,4], label="Rad Percent Difference")

error_2 = abs((corrected_images-band_radiances[5])/(band_radiances[5])*100)
im_2 = axs[1,0].imshow(error_2[:,:,900],vmin=0, vmax=2)
axs[1,0].set_title(f"BB Temp {temperatures[5]-273.15}   BB Rad {band_radiances[5]:.2f}")
fig.colorbar(im_2, ax=axs[1,0], label="Rad Percent Difference")

error_2 = abs((corrected_images-band_radiances[6])/(band_radiances[6])*100)
im_2 = axs[1,1].imshow(error_2[:,:,1060],vmin=0, vmax=2)
axs[1,1].set_title(f"BB Temp {temperatures[6]-273.15}   BB Rad {band_radiances[6]:.2f}")
fig.colorbar(im_2, ax=axs[1,1], label="Rad Percent Difference")

error_2 = abs((corrected_images-band_radiances[7])/(band_radiances[7])*100)
im_2 = axs[1,2].imshow(error_2[:,:,1220],vmin=0, vmax=2)
axs[1,2].set_title(f"BB Temp {temperatures[7]-273.15}   BB Rad {band_radiances[7]:.2f}")
fig.colorbar(im_2, ax=axs[1,2], label="Rad Percent Difference")

error_2 = abs((corrected_images-band_radiances[8])/(band_radiances[8])*100)
im_2 = axs[1,3].imshow(error_2[:,:,1380],vmin=0, vmax=2)
axs[1,3].set_title(f"BB Temp {temperatures[8]-273.15}   BB Rad {band_radiances[8]:.2f}")
fig.colorbar(im_2, ax=axs[1,3], label="Rad Percent Difference")

error_2 = abs((corrected_images-band_radiances[9])/(band_radiances[9])*100)
im_2 = axs[1,4].imshow(error_2[:,:,1540],vmin=0, vmax=2)
axs[1,4].set_title(f"BB Temp {temperatures[9]-273.15}   BB Rad {band_radiances[9]:.2f}")
fig.colorbar(im_2, ax=axs[1,4], label="Rad Percent Difference")

error_2 = abs((corrected_images-band_radiances[10])/(band_radiances[10])*100)
im_2 = axs[2,0].imshow(error_2[:,:,1700],vmin=0, vmax=2)
axs[2,0].set_title(f"BB Temp {temperatures[10]-273.15}   BB Rad {band_radiances[10]:.2f}")
fig.colorbar(im_2, ax=axs[2,0], label="Rad Percent Difference")

error_2 = abs((corrected_images-band_radiances[11])/(band_radiances[11])*100)
im_2 = axs[2,1].imshow(error_2[:,:,1860],vmin=0, vmax=2)
axs[2,1].set_title(f"BB Temp {temperatures[11]-273.15}   BB Rad {band_radiances[11]:.2f}")
fig.colorbar(im_2, ax=axs[2,1], label="Rad Percent Difference")

error_2 = abs((corrected_images-band_radiances[12])/(band_radiances[12])*100)
im_2 = axs[2,2].imshow(error_2[:,:,2020],vmin=0, vmax=2)
axs[2,2].set_title(f"BB Temp {temperatures[12]-273.15}   BB Rad {band_radiances[12]:.2f}")
fig.colorbar(im_2, ax=axs[2,2], label="Rad Percent Difference")

axs.flat[13].axis("off")
axs.flat[14].axis("off")

plt.show()
