# obtain current public ip, create a variables.tfvars file 
# with this ip as the user_ip (along with other static data). 
# Run terraform shell script to apply the instance

import os,subprocess

myip = subprocess.check_output(["dig","+short","myip.opendns.com","@resolver1.opendns.com"])

myip = myip.rstrip()
ssh_key_name = "WallOfSound"
subnet_list="subnet-1c02837a,subnet-1c02837a,subnet-5656f01e"
name = "data"
zone_name = "shadoutmapes.net"
region = "us-west-2"

file = open("variables.tfvars","w")
file.write("ssh_key_name = " + "\"" + ssh_key_name + "\"\n")
file.write("subnet_list = " + "\"" + subnet_list + "\"\n")
file.write("user_ip = " + "\"" + myip + "\"\n")
file.write("name = " + "\"" + name + "\"\n")
file.write("zone_name = " + "\"" + zone_name + "\"\n")
file.write("region = " + "\"" + region + "\"\n")
file.close()

print "Running terraform apply script..."

os.system('./apply_bastion.sh')
