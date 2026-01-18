import numpy as np
import matplotlib.pyplot as plt

print("Loading in data...")
individual_pixel = np.load("/home/cjw9009/Desktop/Senior_Project/20250208_middle_pixel.npy")
print("Loaded data")

individual_pixel = individual_pixel / 256.0
# individual_pixel = np.flip(individual_pixel[0,0,:]) RJPEG LINE
print("plotting ...")
plt.plot(individual_pixel)
plt.savefig("plot_middle_20250208.png")
plt.show()
plt.cla()
chunk_size = 100 # 100 For DRS, 3 For RJPEG
means = np.mean(individual_pixel.reshape(-1, chunk_size), axis=1)
# plt.plot(means)
# plt.savefig("means_top_left_rjpeg.png")
# plt.cla()

derivative = np.gradient(means)
derivative_two = np.gradient(derivative)
plt.plot(derivative)
plt.savefig("derivative_middle_20250208.png")
plt.show()
plt.cla()
plt.plot(derivative_two)
plt.savefig("2nd_derivative_middle_20250208.png")
plt.show()
change_in_temp = [0]

for i in range(derivative.shape[0]):
    if abs(derivative[i]) >= 2*np.std(derivative):
        if change_in_temp is not None:
            change_in_temp.append(i)
        else:
            change_in_temp = []
            change_in_temp.append(i)

change_in_temp.append(derivative.shape[0])
# print(change_in_temp)
distinct_regions = 0
regions = [0]
for i in range(1,len(change_in_temp)-1,1):
    if change_in_temp[i+1] > (change_in_temp[i] + 50):
        regions.append(change_in_temp[i])
        distinct_regions = distinct_regions + 1
    if change_in_temp[i] > (change_in_temp[i-1] + 50):
        regions.append(change_in_temp[i])

regions.append(derivative.shape[0])

print(regions)

cumulative_dc = 0.0
regional_average = []
count = 0
#print(len(regions))
# Moving between regions of Interest
for i in range(1,len(regions),1):
    cumulative_dc = 0.0
    count = 0
    if regions[i-1] + 25 < regions[i]:
        # Summing all DC within the regions of interest
        for j in range(regions[i-1],regions[i],1):
            # Excluding values that do not have a moderately constant derivative
            if derivative[j] < np.std(derivative):
                # print(f"I have found an area to average, and the current block {j} of 100 has a small derivative")
                for b in range(j,(j+1),1):
                    cumulative_dc = cumulative_dc + individual_pixel[b]
                    count = count + 1
                    # print(cumulative_dc)
    if count != 0:
        regional_average.append(cumulative_dc/count)
        print(f"regional average for {regions[i-1]} to {regions[i]} is {cumulative_dc/count}")

print(np.std(derivative))

# # averaged_pixels = np.mean(individual_pixel[27700:49900])
# # print(f"Averaged pixels between large derivative jumps {averaged_pixels} vs. pixels at that count range {individual_pixel[49500:49900]}")

# # plt.hist(individual_pixel)
# # plt.savefig("hist_256.png")