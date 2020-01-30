#!/usr/bin/python3
# CMAuditd.py Muhammad Ismail Zam Zam (Founder of Cybermizz)

from tkinter import *
from tkinter import ttk
import tkinter # for the main tkinter.Tk()
from tkinter.ttk import * # for style
import os #to execute the shell commands
import tkinter.scrolledtext as tkst # for scroll textbar
import subprocess # to make the output of command to the file
from tkinter import messagebox # to display the message box



#----global variable and make is static otherwise we get scope issue
#for static we need to define the class
class Test(object):
    i = 'Status: Sleep!' # global variable to record status of auditd
gauditd_status =  Test()

#--------------------------------------------------------------------

class CMAuditd:

    def __init__(self, window):

	#===========================================	
	#---Creating the Main Window with fixed size	
	window.title('CMAuditd-mismailzz')
	window.state('normal')
	window.geometry('1200x650-40+40')
	window.resizable(False, False) 
	#===========================================
	#---------Create frame for CMAuditd-Controls
	frame = ttk.LabelFrame(window, text="CMAuditd-Controls")
	frame.place(x = 5, y = 5, width=1150, height=50)

	style = Style() #style object because .config is'nt operable in python2.7
	style.configure('W.TButton', font = ('calibri', 10, 'normal'), width =15, height =2) 
	
	#Auditd Service Start Button
	auditd_start_button = ttk.Button(frame, text = "Start Auditd", command = self.start_auditd, style = 'W.TButton').grid(row = 0, column = 0, padx = 30)
	#Auditd Service Restart Button
	auditd_restart_button = ttk.Button(frame, text = "Restart Auditd", command = self.restart_auditd, style = 'W.TButton').grid(row = 0, column = 1, padx = 30)
	#Auditd Service Stop Button	
	auditd_stop_button = ttk.Button(frame, text = "Stop Auditd", command = self.stop_auditd, style = 'W.TButton').grid(row = 0, column = 2, padx = 30)

	#Adding label field of status - in this we change from label to entry because python2.7 cause problem of lable text change on click
	#self.status = ttk.Label(frame, text=gauditd_status,font = ('calibri', 10, 'italic') ).grid(column=5, row=0, padx=30)
	self.auditd_status = ttk.Entry(frame, text= "status" , width = 20)
	self.auditd_status.insert(END, gauditd_status.i)# gauditd_status.i is a static global variable
	self.auditd_status.grid(row = 0, column = 4, padx = 100)#its mean first you declare and last you decide the position otherwise it cause error
	#Auditd Service Status Button	
	status_button = ttk.Button(frame, text = "Status Auditd", command = self.status_auditd, style = 'W.TButton').grid(column=5, row=0, padx=30)
	#===========================================
	#-----------Auditd Log file path Entry Field
	loglabel = ttk.Label(window, text="Auditd Log file: ",font = ('calibri', 10, 'normal') )
	loglabel.place(x = 5, y = 60)
 	
	logfile = ttk.Entry(window, text="path", width = 30)
	logfile.insert(END, '/var/log/audit/auditd.log')
	logfile.state(['disabled']) #Hide for this time but can be extend for variable path
	logfile.place(x = 110, y = 60)	
	#===========================================
	#--Frame of valid Auditd rules (auditctl -l)
	
	frame2 = ttk.LabelFrame(window, text="RULES")
	frame2.place(x=5, y=90, width = 350, height=300)
	
	frame3 = tkinter.Frame(master = frame2) #bg = '#808000'
	frame3.pack(fill='both', expand='yes')
	self.ruleslist = tkst.ScrolledText(
	    master = frame3,
	    wrap   = tkinter.WORD,
	    width  = 20,
	    height = 10
	)
	# Don't use widget.place(), use pack or grid instead, since
	# They behave better on scaling the window -- and you don't
	# have to calculate it manually!
	self.ruleslist.pack(fill=tkinter.BOTH, expand=True) #padx=10, pady=10
	# Adding some text, to see if scroll is working as we expect it
	self.ruleslist.insert(tkinter.INSERT,"Hi Rules!")

	#rule button (to show rules) -->(it show your rules but with no check of valid - so it will be your original file)
	self.originalrule_button = ttk.Button(window, text = "All Rules", command = self.originalrule, style = 'W.TButton').place(x=80, y=395)

	#update rule button (to show rules) -->(it show only the valid rules)
	self.updaterule_button = ttk.Button(window, text = "Valid Rules", command = self.update_rule, style = 'W.TButton').place(x=223, y=395)
	#-----------------------------------------rule setbox completed
		
	#===========================================
	#ADD/DELETE RULES and Copy/Append rules
	
	frame4 = ttk.LabelFrame(window, text="MODIFY RULES FILE")
	frame4.place(x=5, y=425, width = 350, height=220)
	
	#---Entry field for rule
	self.auditdrule = ttk.Entry(frame4, text= "rule", width = 42)
	self.auditdrule.insert(END, 'Write Single Rule Here!')
	#auditdrule.state(['disabled'])
	self.auditdrule.place(x = 0, y = 0)	
	
	#---radiobutton selection and submit button setting
	self.rule_value = StringVar()
	ttk.Radiobutton(frame4, text = 'Add Rule', variable = self.rule_value, value = 'add').place(x=0, y=36)
	ttk.Radiobutton(frame4, text = 'Delete Rule', variable = self.rule_value, value = 'del').place(x=100, y=36)
	#print(rule_value.get()) # Note: value will be empty if no selection is made
	self.addDelete_rule_button = ttk.Button(frame4, text = "Submit", command = self.addDelete_rule, style = 'W.TButton').place(x=210, y=30)
	
	#---Entry field for copy and append new rules in file
	self.auditdrulefile = ttk.Entry(frame4, text="rulefile", width = 42)
	self.auditdrulefile.insert(END, 'Write New Rule File Path Here!')
	#auditdrule.state(['disabled'])
	self.auditdrulefile.place(x = 0, y = 85)	
	
	#---radiobutton selection and submit button setting
	self.rule_file = StringVar()
	ttk.Radiobutton(frame4, text = 'Copy Rule File in Existing auditd.rules file', variable = self.rule_file, value = 'cp').place(x=0, y=115)
	ttk.Radiobutton(frame4, text = 'Append New Rules in Existing auditd.rules file', variable = self.rule_file, value = 'app').place(x=0, y=145)
	#print(rule_value.get()) # Note: value will be empty if no selection is made
	
	rule_file_button = ttk.Button(frame4, text = "Submit", command = self.copyappend_auditd, style = 'W.TButton').place(x=210, y=168)
	#==================================================
	#---Check Rules Frame Start
	frame5 = ttk.LabelFrame(window, text="CHECK RULES VALIDITY")
	frame5.place(x=360, y=90, width = 252, height=375)
	
	frame6 = tkinter.Frame(master = frame5) #bg = '#808000'
	frame6.pack(fill='both', expand='yes')
	self.rulechecklist = tkst.ScrolledText(
	    master = frame6,
	    wrap   = tkinter.WORD,
	    width  = 20,
	    height = 10
	)
	# Don't use widget.place(), use pack or grid instead, since
	# They behave better on scaling the window -- and you don't
	# have to calculate it manually!
	self.rulechecklist.pack(fill=tkinter.BOTH, expand=True) #padx=10, pady=10
	# Adding some text, to see if scroll is working as we expect it
	self.rulechecklist.insert(tkinter.INSERT,"Wrong Rule No. will be displayed here")
	
	check_rule_button = ttk.Button(window, text = "Check", command = self.check_auditd_rule, style = 'W.TButton').place(x=480, y=470)
	#--------------------------------------------------

	self.wrongrule = ttk.Entry(window, text="wrongrule", width = 31) #to get the number of wrong rule and then see
	self.wrongrule.insert(END, 'Line No. of wrong rule!')
	self.wrongrule.place(x = 360, y = 510)	

	get_rule_button = ttk.Button(window, text = "Get", command = self.get_rule_auditd, style = 'W.TButton').place(x=480, y=540)
	
	
	self.wrongrule_path = ttk.Entry(window, text="wrongrulepath", width = 31) #to get the number of wrong rule and then see
	self.wrongrule_path.insert(END, 'Wrong Rule!')
	self.wrongrule_path.place(x = 360, y = 580)	

	#--------------------------------------------------
	#==================================================
	#----Output section of auditd logs based on keys value
	self.outputframe = ttk.LabelFrame(window, text="Auditd KEY VALUES")
	self.outputframe.place(x=620, y=90, width = 570, height=80)
	
	self.keyvalue = ()#tuple
	# the first is the decalartion of variable for textvariable field but 
	# and its value, should not be declared here because it can not update
	# in the dynmaic nature so we have to do the same after its button press
	self.key = tkinter.StringVar()
	self.cboCombo = ttk.Combobox(self.outputframe, values=self.keyvalue, textvariable=self.key, width=68).place(x=1, y=1)
	
	get_key_button = ttk.Button(self.outputframe, text = "Update Keys list", command = self.update_key_auditd, style = 'W.TButton').place(x=430, y=25)
	#==================================================	
	#----get the logs based on keys value (like ausearch -k <key>)
	logframe = ttk.LabelFrame(window, text="Auditd LOGS")
	logframe.place(x=620, y=180, width = 570, height=430)

	frame7 = tkinter.Frame(master = logframe) #bg = '#808000'
	frame7.pack(fill='both', expand='yes')
	self.outputlog = tkst.ScrolledText(
	    master = frame7,
	    #wrap   = tkinter.WORD, 
	    width  = 20,
	    height = 10
	)
	#ISMAIL disallow to wrap the text on the word
	# Don't use widget.place(6), use pack or grid instead, since
	# They behave better on scaling the window -- and you don't
	# have to calculate it manually!
	self.outputlog.pack(fill=tkinter.BOTH, expand=True) #padx=10, pady=10
	# Adding some text, to see if scroll is working as we expect it
	self.outputlog.insert(tkinter.INSERT,"Auditd Logs will be shown here!")
	
	get_log_button = ttk.Button(window, text = "Get Log", command = self.get_log_auditd, style = 'W.TButton').place(x=1057, y=610)
	save_log_button = ttk.Button(window, text = "Save", command = self.save_log_auditd, style = 'W.TButton').place(x=920, y=610)
	
    #=========================================================
    #----Implementing the events of buttons
    
    def start_auditd(self): #start the service auditd
        gauditd_status.i = 'Status: Started!'
	print(gauditd_status)
	os.system('service auditd start')
    
    def restart_auditd(self): #restart the service auditd
        gauditd_status.i = 'Status: Restarted!'
	os.system('service auditd restart')

    def stop_auditd(self): #stop the service auditd
        gauditd_status.i = 'Status: Stopped!'
	os.system('service auditd stop')

    def status_auditd(self):#status of the service auditd (relative to our tool)
	print(gauditd_status.i)
 	self.auditd_status.delete(0, 'end')
        self.auditd_status.insert(END, gauditd_status.i)
	#in the disable state we cannot change value
	#so we are not using disabled state

    def originalrule(self):
	file = open("allrules.txt", "w+")
	os.system("cat /etc/audit/audit.rules > allrules.txt")
	file.close()
        # Open a file: file
	file1 = open('allrules.txt',mode='r')
	 
	# read all lines at once
	all_of_it = file1.read()
	#print(all_of_it)
	self.ruleslist.delete('1.0', END)
	self.ruleslist.insert(tkinter.INSERT, all_of_it) 
	# close the file
	file1.close()
	os.system("rm allrules.txt")
	
    def update_rule(self):
	file = open("auditrule.txt", "w+")
	os.system('auditctl -l > auditrule.txt')
	file.close()
        # Open a file: file
	file1 = open('auditrule.txt',mode='r')
	 
	# read all lines at once
	all_of_it = file1.read()
	#print(all_of_it)
	self.ruleslist.delete('1.0', END)
	self.ruleslist.insert(tkinter.INSERT, all_of_it) 
	# close the file
	file1.close()

    def addDelete_rule(self): # add or delete rule from the rules file
	rule = self.auditdrule.get()
	if self.rule_value.get() != '':
		if self.rule_value.get() == 'add':
			#f=open("sample_rule.rules", "a+")
			#f.write(rule)
			#f.write("\n")
			#the above comment is a test case sample
			f=open("/etc/audit/rules.d/audit.rules" , "a")
			f.write("\n")
			f.write(rule)
			self.auditdrule.delete(0, 'end')
		if self.rule_value.get() == 'del':
			#with open('sample_rule.rules') as rulefile, open('new_sample_rule.rules', 'w+') as cleanfile:
			with open('/etc/audit/rules.d/audit.rules') as rulefile, open('new_sample_rule.rules', 'w+') as cleanfile:
			    for line in rulefile:
				clean = True
				if rule in line:
				    clean = False
				if clean == True:
				    cleanfile.write(line)
			self.auditdrule.delete(0, 'end')
			#os.system('cp new_sample_rule.rules sample_rule.rules')
			os.system('cp new_sample_rule.rules /etc/audit/rules.d/audit.rules')
			os.system('> new_sample_rule.rules')
	else:
		messagebox.showinfo("Title", "Note: Select Add or Delete Option!")

	
	#print(self.rule_value.get())
	#print(rule)

    def copyappend_auditd(self):
	
	file = self.auditdrulefile.get()
	#-----------------------------------			
	get_permission_command = "chmod -R o+rwx " + file
	os.system(get_permission_command)
	'''as we get the problem in copy file of permission issues, so i allow in above command'''
	get_permission_command = "chmod -R o+rwx /etc/audit/rules.d/audit.rules" 
	os.system(get_permission_command)
	'''we also give the permission where we want to copy'''
	#-----------------------------------
	if self.rule_file.get() != '':
		if self.rule_file.get() == 'cp':
					
			command = "sudo cp "+ rule_file +"/etc/audit/rules.d/audit.rules"
			os.system(command)
			self.auditdrulefile.delete(0, 'end')
		if self.rule_file.get() == 'app':
			f = open(file, "r")
			audit_rules = open("/etc/audit/rules.d/audit.rules", "a")
			fread = f.readlines()
			for i in range(len(fread)):
				audit_rules.write("\n")
				audit_rules.write(fread[i])
			audit_rules.close()
			f.close()				
			#command = file + " >> /etc/audit/rules.d/audit.rules"
			#os.system(command)
			self.auditdrulefile.delete(0, 'end')
	else:
		messagebox.showinfo("Title", "Note: Select Copy or Append Option!")

	
    def check_auditd_rule(self):
	f=open('ruleChecker.txt', 'w+')# +represent if not exit file then create
	f.close()
	self.rulechecklist.delete("1.0", "end")	
	os.system('augenrules --load 2>> ruleChecker.txt')
	f=open('ruleChecker.txt', 'r')
	fread = f.readlines()
	#print(len(fread)-1)
	if (len(fread)) > 0:
		for i in range(len(fread)): 
			if ('error in line' in fread[i]) == True:
				self.rulechecklist.insert(tkinter.INSERT, fread[i])
				break # if found then come out of loop
				#print('hi ismail')
	else:
		#print('hello')
		self.rulechecklist.insert(tkinter.INSERT, "All Rules are valid")
	os.system('> ruleChecker.txt')	
	

    def get_rule_auditd(self):
	wrong_rule_number = self.wrongrule.get()
	if wrong_rule_number.isdigit():
		f=open('wrongrule.txt', 'w+')# +represent if not exit file then create
		f.close()			
		#Example command for 13th wrong rule: >> sed -n '13p' /etc/audit/audit.rules
		make_command = 'sed -n \'' + wrong_rule_number + 'p\' /etc/audit/audit.rules > wrongrule.txt'
		os.system(make_command)
		f=open('wrongrule.txt', 'r')
		fread = f.readlines()
		self.wrongrule_path.delete(0, 'end')
		self.wrongrule_path.insert(END, fread[0])
		f.close()
		os.system('rm wrongrule.txt')		
		
	else:
		messagebox.showinfo("Title", "Note: Please enter a number (Avoid to write wrong number, it will permanently delete your rule).")

    def	update_key_auditd(self):
	#f=open("auditd.log", "r")
	f=open("/var/log/audit/auditd.log", "r")	
	fread = f.readlines()
	print(fread)
	key_list_store = []
	for i in range(len(fread)):
		if ('key=' in fread[i]) == True:
			temp = fread[i].split(' ')
			for j in range(len(temp)):
				if ('key' in temp[j]) == True: 
					get_key = temp[j]
					key_list_store.append(get_key.replace('\n','')) # For clean to remove \n from key values as added by file
	f.close()
	key_list_store = list(set(key_list_store)) # to make the unique	
	print(key_list_store)
	
	for i in range(len(key_list_store)):
		self.keyvalue = self.keyvalue + (key_list_store[i], )
	self.key = tkinter.StringVar()
	self.cboCombo = ttk.Combobox(self.outputframe, values=self.keyvalue, textvariable=self.key, width=68).place(x=1, y=1)
	


    def get_log_auditd(self):
	value = self.key.get() #if you get error (like argument value required -k) its mean you have to select the textvariable value
				#Which is define in the Combobox
	print(value)
	if isinstance(value, str) == True: #check if a string is selected
		f = open("ausearch.txt", "w+")
		f.close()
		key_value = value[5:len(value)-1]
		command = 'ausearch -k ' + key_value + ' --interpret > ausearch.txt'
		os.system(command)
		os.system("python clean_auditd.py") #passing ausearh.txt from filter
		f = open("finalrefined.txt", "r")# the resultant file and in filter we delete ausearch file
		#f = open("ausearch.txt", "r") 
		#f = open("finalrefined.txt", "r")		
		fread = f.readlines()
		temp_string = ""
		for i in range(len(fread)):
			temp_string = temp_string + fread[i] + "\n" 
		self.outputlog.delete("1.0", "end")
		self.outputlog.insert(tkinter.INSERT, temp_string)	
		f.close()
		#os.system('rm finalrefined.txt') # i need below, so i can't delete
		#messagebox.showinfo("Title", "")
	else:
		messagebox.showinfo("Title", "Note: Please select any key value!")

		
	
    def save_log_auditd(self):
	value = self.key.get()
	if (len(value) > 1) == True:
		key_value = value[5:len(value)-1]
		#store the detailed information comming from ausearch		
		dfilename = "d" + key_value + ".txt" #to create a file to save log
		f=open(dfilename, "w+")
		f.close()
		command = 'ausearch -k ' + key_value + ' --interpret > ' + dfilename
		os.system(command)
		#store the detailed information comming from ausearch
		cfilename = "c" + key_value + ".txt" #to create a file to save log
		command = 'cat finalrefined.txt > ' + cfilename
		f=open(cfilename, "w+")
		f.close()
		os.system(command)
		
		message = "Note: logs are saves in script folder (Detailed Log: " + dfilename  + " and  Comprehensive log: " + cfilename + ")" 	  	
		messagebox.showinfo("Title", message)
	else: 
		messagebox.showinfo("Title", "Please choose the key value")

            
def main():            
    
    root = tkinter.Tk()
    app =CMAuditd(root)
    root.mainloop()
    
if __name__ == "__main__": main()


