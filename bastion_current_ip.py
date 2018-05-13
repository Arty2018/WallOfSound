#!/usr/bin/env python
""" obtain current public ip, create a variables.tfvars file
with this ip as user_ip (along with other vars obtained
from command line input).
Run terraform shell script to apply the instance """

import os
import subprocess
import argparse



def main():
    """ Use argparse to read commands and take action accordingly """
    parser = argparse.ArgumentParser(description="Pass Terraform variables for bastion")

    parser.add_argument('-k', '--ssh_key_name', type=str, help="Name of local SSH key file")
    parser.add_argument('-s', '--subnet_list', type=str,
                        help="List of subnets to use, comma separated")
    parser.add_argument('-n', '--name', type=str, help="A Record for site")
    parser.add_argument('-z', '--zone_name', type=str, help="Domain Name")
    parser.add_argument('-r', '--region', type=str, help="AWS Region name")
    parser.add_argument('--destroy', action='store_true', default=False,
                        help="Destroy existing bastion")
    parser.add_argument('--plan_destroy', action='store_true', default=False,
                        help="Plan for destroy existing bastion")
    parser.add_argument('--plan_apply', action='store_true', default=False,
                        help="Plan for apply new bastion")
    parser.add_argument('--apply', action='store_true', default=False, help="Apply new bastion")

    args = parser.parse_args()

    if args.plan_destroy:
        os.system('./plan_destroy_bastion.sh')
        return

    if args.destroy:
        os.system('./destroy_bastion.sh')
        return

    if args.plan_apply or args.apply:
        if (args.ssh_key_name is None or args.subnet_list is None or
                args.name is None or args.zone_name is None or args.region is None):
            print "Aborted: must specify all parameters."
            return

        myip = get_public_ip()
        # create or overwrite variables.tfvars with user input from command line parser

        varfile = open("variables.tfvars", "w")
        varfile.write("ssh_key_name = " + "\"" + args.ssh_key_name + "\"\n")
        varfile.write("subnet_list = " + "\"" + args.subnet_list + "\"\n")
        varfile.write("user_ip = " + "\"" + myip + "\"\n")
        varfile.write("name = " + "\"" + args.name + "\"\n")
        varfile.write("zone_name = " + "\"" + args.zone_name + "\"\n")
        varfile.write("region = " + "\"" + args.region + "\"\n")
        varfile.close()

        if args.plan_apply:
            os.system('./plan_apply_bastion.sh')
            return

        if args.apply:
            os.system('./apply_bastion.sh')
            return


def get_public_ip():
    """ attempt to obtain public ip. tries 3 different sites """
    try:
        myip = subprocess.check_output(["curl", "ifconfig.io"])
    except subprocess.CalledProcessError as err:
        #except if timeout error or site not returning address
        print err.output
        try:
            myip = subprocess.check_output(["dig", "+short", "myip.opendns.com",
                                            "@10.255.255.1"])
        except subprocess.CalledProcessError as err:
            #except if timeout error or site not returning address
            print err.output
            try:
                myip = subprocess.check_output(["curl", "-s", "checkip.dyndns.org"])
                myip = myip.split(":", 1)[-1]
                myip = myip.split("<", 1)[0]
            except subprocess.CalledProcessError as err:
                #except if timeout error or site not returning address
                print err.output
                myip = raw_input('Error obtaining IP address. Please specify IP: ')
    myip = myip.lstrip()
    myip = myip.rstrip()
    print "Public IP obtained"
    return str(myip.decode("utf-8"))




if __name__ == "__main__":
    main()
