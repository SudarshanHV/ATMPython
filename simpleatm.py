import datetime
import ast
import re
details={}
password="admin"
path="File path of Atm.txt"
def readdetails():
	file=open(path,"r")
	for line in file:
		lister=line.split()
		#ast.literal__eval 
		details[lister[0]]=[int(lister[1]),int(lister[2]),lister[3],ast.literal_eval(lister[4]),int(lister[5])]#ast.literal_eval Converts string to list
	#print(details) Line for debugging 

def writedetails():
	file=open(path,"w")
	for key,value in details.items():
		#Troubleshootin EOF error using Regex
		var=re.sub(r"[\n\t\s]*", "", str(value[3]))# re.sub is used to trim spaces 
		string=key+' '+str(value[0])+' '+str(value[1])+' '+value[2]+' '+var+' '+str(value[4])+'\n'
		file.write(string)
	file.close()



def withdraw(accno):
	accno=str(accno)
	counter=0
	while counter<3:
		if(details[accno][4]==1):
			pin=int(input("Enter the PIN:"))
			if(pin==details[accno][0]):
				amt=int(input('Enter amount to withdraw:'))
				if(amt>int(details[accno][1])):
					print('You dont have that much frickin money!!!')
					terminal()
				details[accno][1]-=amt
				datestr=datetime.datetime.now().isoformat()
				transaction=f"Withdrawn..{amt}..from..{accno}..Date:{datestr}"
				details[accno][3].append(transaction)
				print('Collect your amount!!!\n\n')
				writedetails()		
			else:
				counter+=1
				print(f'Invalid pin: Tries remaining {3-counter}')
				if(counter==3):
					print("Account blocked.Contact admin to unblock:")
					details[accno][4]=0
					writedetails()
		else:
			print("Sorry. Account is Blocked!!! Contact Admin to unblock.")
			break
	terminal()

def deposit(accno):
	amt=int(input('Enter amount to deposit:'))
	details[accno][1]+=amt
	datestr=datetime.datetime.now().isoformat()
	transaction=f"Deposited..{amt}..to..{accno}..Date:{datestr}"
	details[accno][3].append(transaction)
	print('Successfully deposited amount!!!\n\n')
	writedetails()
	terminal()

def printreceipt(accno):
	accno=str(accno)
	for item in details[accno][3]:
		print(item)
	terminal()

def terminal():
	#print(details) Line for Debugging
	choice=int(input("1.Do a transaction:(User) OR\n2.Exit\n3.Enter new user/unblock(admin only):\nEnter your choice:"))
	if(choice==1):
		accno=input('Enter account number:\n')
		if(details[accno][4]==1):
			print('1.Withdraw\n2.Deposit\n3.Print Receipt')
			ch=int(input("Enter your choice:\n"))
			if(ch==1):
				withdraw(accno)
			elif ch==2:
				deposit(accno)
			elif ch==3:
				printreceipt(accno)
			else:
				print("Invalid choice")
		else:
			print("Account blocked. Contact admin to unblock!")
		terminal()
	elif choice==2:
		writedetails()
		exit()
	elif choice==3:
		newuser()
		exit()
	else:
		print("Invalid choice!!\n")
	terminal()

def newuser():
	pwd=input("Enter admin password:")
	if(pwd==password):
		print("1.Enter new user\n2.Unblock account\nEnter your choice:")
		ch=int(input())
		if(ch==1):
			accno=input("Enter new user account number:")
			pin=int(input("Enter pin:"))
			balance=int(input("Enter current account balance:"))
			name=input("Enter the name:")
			details[accno]=[pin,balance,name,[],1]
			writedetails()
		elif(ch==2):
			accno=input("Enter user account number:")
			details[accno][4]=1
			writedetails()
			print("Account unblocked!!")
		else:
			print("Invalid choice, Redirecting to admin login page:")
			newuser()
	else:
		print("Invalid password.Redirecting to main page.....")
	terminal()
readdetails()
terminal()







