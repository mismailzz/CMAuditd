import os
#openfile = open("copy_ausearch.txt", "r")
openfile = open("ausearch.txt", "r")
read_file = openfile.readlines()
newfile = open("refined.txt", "a+")
for i in range(len(read_file)):
	temp_list = read_file[i].split(' ')
	temp = ''
	#print(temp_list)
	
	for j in range(len(temp_list)):
		if ((('items' in temp_list[j])) or (('exit' in temp_list[j])) or (('a0' in temp_list[j])) or (('a1' in temp_list[j]))or (('a2' in temp_list[j]))or (('a3' in temp_list[j]))or (('auid' in temp_list[j]))or (('euid' in temp_list[j]))or (('suid' in temp_list[j]))or (('fsuid' in temp_list[j]))or (('egid' in temp_list[j]))or (('sgid' in temp_list[j]))or (('fsgid' in temp_list[j]))or (('tty' in temp_list[j]))or (('ses' in temp_list[j]))or (('subj' in temp_list[j]))or (('list=exit' in temp_list[j]))or (('res' in temp_list[j])) or (('item' in temp_list[j])) or (('inode' in temp_list[j]))or (('dev' in temp_list[j]))or (('rdev' in temp_list[j]))or (('cap_fp' in temp_list[j]))or (('cap_fi' in temp_list[j]))or (('cap_fe' in temp_list[j]))or (('cap_fver' in temp_list[j])) or (('cap_frootid' in temp_list[j]))) == False:
			temp = temp + " " + temp_list[j] 
			print(temp)

	newfile.write(temp)
	#newfile.write('\n')

openfile.close()
newfile.close()

os.system("> finalrefined.txt") # to remove the previous content

newfile = open("refined.txt", "r")
readfile = newfile.readlines()
refinedfile = open("finalrefined.txt", "a+") #it will be deleted in caller function because its result needed there
for i in range(len(readfile)):
	#print(readfile[i])
	temp_list = readfile[i].split(' ')
	print(temp_list)
	temp = ''
	for j in range(len(temp_list)):
		if ((j == 2) or ( j == 3)) == False:
			temp = temp + " " + temp_list[j]
	refinedfile.write(temp)
	 
	#temp_list = (str(readfile)).split(':')
	#print(temp_list)
	#temp = temp_list[0].split(' ')
	#sentence = temp[0] + " : " + temp_list[1]
	#refinedfile.write(sentence)
newfile.close()
refinedfile.close()
os.system('rm ausearch.txt') #delete as its work complete
os.system('rm refined.txt')

