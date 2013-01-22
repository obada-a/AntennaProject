import antenna_package
import math
from pylab import*

n = 9
c = 3.0*10**8
r = 20.0
f0 = 5.8*10**9
lambda_0 = c/f0

file_gain = open("gain.txt",'r')
file_angles = open("angles.txt",'r')

gain = []
angles = []
while True:
    line = file_gain.readline()
    if not line:
        break
    gain.append(float(line))
file_gain.close()

while True:
    line = file_angles.readline()
    if not line:
        break
    angles.append(float(line))
file_angles.close()

for item in range(0,len(gain)):
    gain[item] = 10**(gain[item]/10)

#distances between array elements
distances = arange(lambda_0/2,lambda_0,0.01)
array_factor = zeros((len(distances),len(angles)))
array_factor_gain = zeros((len(distances),len(angles)))
system_gain = zeros((len(distances),len(angles)))
max_gain = zeros(len(distances))
beam_width = zeros(len(distances))

for item in range(0,len(distances)):
    synthesis_results =  antenna_package.chebySynthesisDistance(f0, r , angles, gain, n, distances[item])
    synthesis_results[0]
    array_factor[item] = synthesis_results[0]
    array_factor_gain[item] = synthesis_results[1]
    system_gain[item] = synthesis_results[2]
    max_gain[item] = synthesis_results[3]
    beam_width[item] = synthesis_results[4]
print(len(beam_width))
print(len(distances))
plot(distances,beam_width)
grid(True)
xlabel( "distance between pathces" )
ylabel(" beamwidth")
title(" Beamwidth variation for " + str(n) + " elements array antenna " )
show()




