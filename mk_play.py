#!/usr/bin/env python3

import csv
import yaml
from collections import defaultdict

csv_file = 'requirements.csv'
yaml_file = 'requirements.yml'

devices = defaultdict(lambda: {
    'interfaces': []
})

def yaml_file_creator(): 
    try:
        with open(csv_file) as file:
            reader = csv.DictReader(file, delimiter=',')
            for row in reader:
                hostname = row['hostname']
                if row['local_as'] != '':
                    devices[hostname]['local_as'] = int(row['local_as'])
                    devices[hostname]['neighbors'] = row['neighbors']
                    devices[hostname]['remote_as'] = row['remote_as']
                    devices[hostname]['source_int'] = row['source_int']
                    devices[hostname]['next_hop'] = row['next_hop']
                interface = {
                    'interface_type': row['interface_type'],
                    'interface_number': row['interface_number'],
                    'ip': row['ip'],
                    'mask': row['mask'],
                    'bgp_peer': row['bgp_peer'],
                    'advertise': row['advertise'],
                    'subnet': row['subnet'],
                    'border_router': row['border_router'],
                }
                devices[hostname]['interfaces'].append(interface)
        output_data = {
            'devices': []
        }
        for hostname, data in devices.items():
            device_entry = {
                'hostname': hostname,
                'local_as': data['local_as'],
                'neighbors': data['neighbors'],
                'remote_as': data['remote_as'],
                'source_int': data['source_int'],
                'next_hop': data['next_hop'],
                'interfaces': data['interfaces']
            }
            output_data['devices'].append(device_entry)
        with open(yaml_file, 'w') as file:
            yaml.dump(output_data, file, sort_keys=False)
            
        print("YAML file created")
    except Exception as e:
        print(f"Something went wrong creating inventory file: {e}")

# main function 
def main():
    yaml_file_creator()


if __name__ == "__main__":
    main()
