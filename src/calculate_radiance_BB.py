# Test script to calculate the total radiance of a blackbody given a vector of temperatures (e.g. a calibration run)

import scipy.constants as const
import scipy.integrate as integrate
import math
import numpy
import matplotlib.pyplot as plt

plancks_constant = const.h # 6.62607015e-34 [Joules*Seconds] 
speed_of_light_constant = const.c # 299792458.0 [Meters/Second]
boltzmann_constant = const.k # 1.380649e-23 [Joules/Kelvin]

wavelengths = numpy.linspace(8,14,6000) # Microns
wavelength = wavelengths*0.000001 # Microns --> Meters
temperature = 20 + 273.15 # Kelvin
spectral_radiance = []

numerator = (2.0*plancks_constant*speed_of_light_constant*speed_of_light_constant)

for i in range(len(wavelength)):
    
    denominator = (wavelength[i]*wavelength[i]*wavelength[i]*wavelength[i]*wavelength[i]*1000000.0)
    exponent = plancks_constant*speed_of_light_constant/(wavelength[i] * boltzmann_constant * temperature)

    spectral_radiance.append(numerator/denominator * 1/(math.exp(exponent)-1)) # [W/m^2/sr/micron]

radiance = integrate.trapezoid(spectral_radiance,wavelengths)
print(F"Total radiance of the blackbody {radiance}")
plt.plot(spectral_radiance)
plt.show()