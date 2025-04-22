#!/usr/bin/env python3

import os
import mk_play
from netmiko import ConnectHandler
import concurrent.futures as cf
import subprocess

site_yml_location = "/etc/ansible/site.yml"
tasks_yml_location = "/etc/ansible/roles/router/tasks/main.yml"

site_yml_content = """
---
- name: Configure Routers
  hosts: localhost
  gather_facts: no
  vars_files:
    - requirements.yml
  roles:
    - router
"""

tasks_yml_content = """
---
- name: Generate configuration file
  template: src=router.j2 dest=/etc/ansible/configs/{{item.hostname}}.txt
  with_items: "{{ devices }}"
"""



# this function sets up the ansible files needed in the /etc/ansible folder. will create a site.yml and then a main.yml in the tasks folder 
def mk_playbook_files():
    with open(site_yml_location, "w") as site_file:
        site_file.write(site_yml_content)
    print("Created site.yml")

    with open(tasks_yml_location, "w") as task_file:
        task_file.write(tasks_yml_content)
    print("Created main.yml in tasks folder")
    
    # runs the mk_play.py script that creates a yml file with the formatted info from requirements.csv
    mk_play.yaml_file_creator()



# runs the ansible playbook
def mk_play_run():
    print("Running ansible-playbook")
    run = subprocess.run(["ansible-playbook", "/etc/ansible/site.yml"], stdout=subprocess.PIPE, text=True)
    print(run.stdout)
    if run.returncode == 0:
        print("Playbook completed")



# basic function to use netmiko to configure a device
def Config(man_ip, config_file): 
    try:

        login = {
                "device_type": "cisco_ios",
                "host": f"{man_ip}",
                "username": f"team",
                "password": f"team",
                "secret": f"netman",
        }

        with ConnectHandler(**login) as net_connect:
            print(f"Logged in to {man_ip} as team")
            net_connect.enable()
            output = net_connect.send_config_from_file(config_file)
            print(f"{man_ip} configured")
    except KeyboardInterrupt:
        print("Exiting")


# uses the config function and concurrency to run the function for each router at the same time   
def bgp_config():
    config_ip_list = ["198.51.100.10", "198.51.100.20", "198.51.100.30", "198.51.100.40", "198.51.100.50", "198.51.100.60", "198.51.100.70", "198.51.100.80"]
    config_file_list = ["/etc/ansible/configs/R1.txt", "/etc/ansible/configs/R2.txt", "/etc/ansible/configs/R3.txt", "/etc/ansible/configs/R4.txt", "/etc/ansible/configs/R5.txt", "/etc/ansible/configs/R6.txt", "/etc/ansible/configs/R7.txt", "/etc/ansible/configs/R8.txt"]
    with cf.ThreadPoolExecutor(max_workers=4) as executor:
        futures = []
        for ip, config_file in zip(config_ip_list, config_file_list):
            futures.append(executor.submit(Config, man_ip=str(ip), config_file=config_file))


# main function 
def main():
    mk_playbook_files()
    mk_play_run()
    bgp_config()


if __name__ == "__main__":
    main()
