import os
import numpy as np
import LWIRimagetool
import matplotlib.pyplot as plt



directory = ("/home/cjw9009/Desktop/Senior_Project/FLIRSIRAS_CalData/20251202_1400")
# Factory = LWIRimagetool.ImageDataFactory()
# image = Factory.create_from_file(directory,'envi')
first_image_path = None
# print(image.metadata)


# Loop through each image
for file in sorted(os.listdir(directory)):
    filename = os.fsdecode(file)
    if filename.endswith("_R.jpg"):
        file_path = os.path.join(os.fsdecode(directory), filename)
        print(f"Currently processing {filename} ...")
        if first_image_path is None:
            Factory = LWIRimagetool.ImageDataFactory()
            first_src = Factory.create_from_file(file_path,'rjpeg')
            image_stack = np.array(first_src.raw_counts)
            first_image_path = file_path
            print(first_src.raw_counts.shape)
        else:
            src = Factory.create_from_file(file_path,'rjpeg')
            image_stack = np.dstack((image_stack,src.raw_counts))

np.save("20251202_1400_fullimage_bbrun", image_stack)
print(f"Image stack size for calibration run{image_stack.shape}")

# plt.imshow(image.raw_counts[:,:,1999])
# pixel_vector = image.raw_counts[320,206,:].flatten()
# plt.plot(pixel_vector)
# print(f"{image.raw_counts[0,0,:]}")
# plt.colorbar()
# plt.show()

