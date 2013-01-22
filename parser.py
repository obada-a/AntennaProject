import os

input_file = open("dati.dat",'r')
out_angles = open("angles.txt",'w')
out_gain = open("gain.txt",'w')
gain = []
angles = []
while True:
    line = input_file.readline()
    if not line:
        break
    s = line.split("\t")
    angles.append(s[0])
    gain.append(s[1])
for item in range(0,len(gain)):
    out_angles.write(angles[item] + "\n" )
    out_gain.write(gain[item] + "\n" )

input_file.close()
out_angles.close()
out_gain.close()
