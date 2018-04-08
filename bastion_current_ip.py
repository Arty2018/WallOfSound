# obtain current public ip, create a variables.tfvars file 
# with this ip as user_ip (along with other vars obtained
# from command line input). 
# Run terraform shell script to apply the instance

import os,subprocess
import argparse



def main():

	parser = argparse.ArgumentParser(description="Pass Terraform variables for bastion")

	parser.add_argument('-k','--ssh_key_name', type=str)
	parser.add_argument('-s','--subnet_list', type=str)
	parser.add_argument('-n','--name',type=str)
	parser.add_argument('-z','--zone_name',type=str)
	parser.add_argument('-r','--region',type=str)
	parser.add_argument('--destroy',action='store_true',default=False)
	parser.add_argument('--plan_destroy',action='store_true',default=False)
	parser.add_argument('--plan_apply',action='store_true', default=False)
	parser.add_argument('--apply',action='store_true',default=False)

	args = parser.parse_args()

	if args.plan_destroy:
		os.system('./plan_destroy_bastion.sh')
		return

	if args.destroy:
		os.system('./destroy_bastion.sh')
		return

	if args.plan_apply | args.apply:
		myip=get_public_ip()
		# create or overwrite variables.tfvars with user input from command line parser

		file = open("variables.tfvars","w")
		file.write("ssh_key_name = " + "\"" + args.ssh_key_name + "\"\n")
		file.write("subnet_list = " + "\"" + args.subnet_list + "\"\n")
		file.write("user_ip = " + "\"" + myip + "\"\n")
		file.write("name = " + "\"" + args.name + "\"\n")
		file.write("zone_name = " + "\"" + args.zone_name + "\"\n")
		file.write("region = " + "\"" + args.region + "\"\n")
		file.close()

		if args.plan_apply:
			os.system('./plan_apply_bastion.sh')
			return

		if args.apply:
			os.system('./apply_bastion.sh')
			return


def get_public_ip(): #attempt to obtain public ip. tries 2 different websites
	try:
		myip = subprocess.check_output(["dig","+short","myip.opendns.com","@resolver1.opendns.com"])
	except:
		try:
			myip = subprocess.check_output(["curl", "-s","checkip.dyndns.org"])
			myip = myip.split(":",1)[-1]
			myip = myip.split("<",1)[0]
		except:  
			myip = raw_input('Error obtaining IP address. Please specify IP: ')
 	myip = myip.lstrip()
	myip = myip.rstrip()
	print ("Public IP obtained")
	return str(myip.decode("utf-8"))


	

if __name__ == "__main__":
	main()
