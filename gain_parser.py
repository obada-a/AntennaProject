import os

inout_file = open("/home/alex/Dropbox/deFEKO/gain",'r')
data = []

while True:
    line = inout_file.readline()
    if not line:
        break
    data.append(line)
inout_file.close()

angoli = []
guadagni = []
index = 0
separator = "   "
i = 0
for item in data:
    def one(item):
        return item.split("    ")[1]
    def two(item):
        return item.split("    ")[0].split("   ")[-1]
    func_dict = { 0 : one, 1 : two }
    angoli.append(func_dict[i](item))
    guadagni.append(item.split("    ")[-2].split(separator)[index])
    if angoli[-1] == "9.50":
        i = 1
    if guadagni[-1] == "0.00":
        index = -2
        guadagni[-1] = item.split("    ")[-2].split(separator)[index]
    elif guadagni[-1] == "-9.8534":
        separator =" "
        index = -4
file_angoli = open("/home/alex/Dropbox/deFEKO/gain_angoli.txt",'w')
file_guadagni = open("/home/alex/Dropbox/deFEKO/gainTotal.txt",'w')
for item in angoli:
    file_angoli.write(item+"\n")
for item in guadagni:
    file_guadagni.write(item+"\n")
file_angoli.close()
file_guadagni.close()
