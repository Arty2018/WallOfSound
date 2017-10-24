# obtain current public ip, create a variables.tfvars file 
# with this ip as the user_ip (along with other vars prompted
# from user). 
# Run terraform shell script to apply the instance

import os,subprocess

def main():

	myip=get_public_ip()
	ssh_key_name,subnet_list,name,zone_name,region = get_variables()

	# create or overwrite variables.tfcars with user input from get_variables function

	file = open("variables.tfvars","w")
	file.write("ssh_key_name = " + "\"" + str(ssh_key_name) + "\"\n")
	file.write("subnet_list = " + "\"" + str(subnet_list) + "\"\n")
	file.write("user_ip = " + "\"" + myip + "\"\n")
	file.write("name = " + "\"" + str(name) + "\"\n")
	file.write("zone_name = " + "\"" + str(zone_name) + "\"\n")
	file.write("region = " + "\"" + str(region) + "\"\n")
	file.close()

	run_bastion_tf()

def get_public_ip():
	myip = subprocess.check_output(["dig","+short","myip.opendns.com","@resolver1.opendns.com"])
	myip = myip.rstrip()
	print ("Public IP obtained")
	return str(myip.decode("utf-8"))

def get_variables():
	ssh_key_name= input('Enter ssh key file name: ')
	subnet_list= input('Enter subnet list: ')
	name = input('Enter A record: ')
	zone_name = input('Enter domain name: ')
	region = input('Enter AWS region: ')

	return(ssh_key_name,subnet_list,name,zone_name,region)

def run_bastion_tf():
	print("\n")

	while True:
		action = input('Choose one of the followng: \n - plan_apply \n - plan_destroy \n - apply \n - destroy \n  (type "C" to cancel) \n')
		if action not in ['plan_apply','plan_destroy','apply','destroy','C']:
			continue
		else:
			break

	print ("\n")

	if action != "C":
		print ("Running terraform " + action + " script...")
	else:
		print ("Quit program")

	if action == "plan_apply":
		os.system('./plan_apply_bastion.sh')
	elif action == "plan_destroy":
		os.system('./plan_destroy_bastion.sh')
	elif action == "apply":
		os.system('./apply_bastion.sh')
	elif action == "destroy":
		os.system('./destroy_bastion.sh')
	elif action == "C":
		return()

	

if __name__ == "__main__":
	main()
