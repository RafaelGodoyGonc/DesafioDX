#!/usr/bin/env python3
default_days = 30
import csv, json, re, os, shutil
import requests
from datetime import datetime
from itertools import islice

max_email = 'max.silva@camil.com.br'
new_max_email = ''

def change_file(old_value, new_value, path, archive):
    project_root_dir = os.getcwd()

    approval_edi_file = os.path.join(project_root_dir, 'force-app', 'main', 'default', path, archive)
    
    fin = open(approval_edi_file, "rt")
    data = fin.read()
    data = data.replace(old_value, new_value)
    fin.close()
    
    fin = open(approval_edi_file, "wt")
    fin.write(data)
    fin.close()

def create_scratch_script():
    change_file(max_email, new_max_email, 'approvalProcesses', 'ItemListaEDI__c.VerificarDescontoMaximo.approvalProcess-meta.xml')

    
def discart_scratch_script():
    change_file(new_max_email, max_email, 'approvalProcesses', 'ItemListaEDI__c.VerificarDescontoMaximo.approvalProcess-meta.xml')
      
email_regex_str = '[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'

print('\n\nCREATING SCRATCH ORG...\n\n')
print('################################################################')
print('################################################################\n\n')

org_name = input('Scratch org name: ')

os.system('sfdx force:org:create -a "{org_name}" -f "../camil-sf/config/project-scratch-def.json" -s -w 10 -d {days}'.format(org_name=org_name, days=default_days))

project_root_dir = os.getcwd()
settings_file_path = os.path.join(project_root_dir, 'scripts', 'settings.json')
root_csv_path = os.path.join(project_root_dir, 'csv')
root_csv_default_path = os.path.join(project_root_dir, 'scripts', 'csvDefault')
translation_file_path = os.path.join(root_csv_path, 'translation.json', )
root_json_path = os.path.join(project_root_dir, 'csv', 'converted-output')


print('\nImporting components...\n')

auth_data = json.loads(
    os.popen('sfdx force:org:display --json').read()
)['result']

new_max_email = auth_data['username']

create_scratch_script()

os.system('sfdx force:source:push -f')
    
discart_scratch_script() 

print('\n\nScratch org created successfully.\n')