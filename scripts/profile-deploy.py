#!/usr/bin/env python3
import os
from xmljson import parker, Parker
from xml.etree.ElementTree import fromstring as parse_xml
from collections import defaultdict

def is_field_assignable(e): 
    is_valid = type(e) is not str and e['fullName'].endswith('__c')
    
    if 'required' in e:
        is_valid = is_valid and not e['required'] 

    if 'type' in e:
        is_valid = is_valid and not e['type'] == 'MasterDetail' 

    return is_valid

    # return type(e) is not str and ('type' in e and not e['type'] == 'MasterDetail')

def go_up(path, times=1): 
    result = path
    for _ in range(times): 
        result = os.path.dirname(result)
    return result

print('\nRUNNING AUTO-GENERATE FOR "ADMIN" PROFILE...\n\n')
print('################################################################')
print('################################################################\n\n')

profile_nodes = list()
tab_nodes = list()

#while not in root dir
while 'sfdx-project.json' not in os.listdir('.') :
    os.chdir('..')

project_root_dir = os.getcwd()

#joins with the OS default separator
object_directory = os.path.join( project_root_dir, 'converted', 'main', 'objects' )
tabs_directory = os.path.join( project_root_dir, 'converted', 'main', 'tabs' )
package_file_path = os.path.join( project_root_dir, 'converted', 'main', 'package.xml' )


for root, dirs, files in os.walk(object_directory):
    print('Parsing .object files...')
    for f in files: 
        if f.endswith('.object'):
            
            with open(os.path.join(object_directory, f), encoding='utf-8', mode='r') as object_file: 
                file_content = object_file.read().replace(r'xmlns="http://soap.sforce.com/2006/04/metadata"', '')
                object_parsed = (parker.data(parse_xml(file_content), preserve_root=True))

                fields = object_parsed['CustomObject']['fields']

                for e in fields:
                    if is_field_assignable(e):
                        field_name = ('{}.{}'.format(f.replace('.object', ''), e['fullName']))

                        profile_nodes.append('' + 
                            '<fieldPermissions>            \n'
                            '    <editable>true</editable> \n'
                            '    <field>{}</field>         \n'
                            '    <readable>true</readable> \n'
                            '</fieldPermissions>           \n'
                            .strip()
                            .format(field_name)
                        )
    print('Files parsed.\n')

#parsing tabs
for root, dirs, files in os.walk(tabs_directory):
    print('Parsing .tab files...')
    for f in files: 
        if f.endswith('.tab'):

            tab_nodes.append('' + 
                '<tabVisibilities>                       \n' 
                '    <tab>{}</tab>                       \n' 
                '    <visibility>DefaultOn</visibility>  \n' 
                '</tabVisibilities>                        '
                .strip()
                .format(f.replace('.tab', ''))
            )
            
    print('Files parsed.\n')

file_dir = (os.path.join(go_up(object_directory, times=2), 'profileDeploy', 'profiles'))
if not os.path.exists(file_dir):
    print('Creating default structure...')
    os.makedirs(file_dir)
print('Using default structure (./converted/profileDeploy).\n')

print('Adding record types visibilities...')

package_file = open(package_file_path, 'r', encoding='utf-8')
package_file_content = package_file.read().replace(r'xmlns="http://soap.sforce.com/2006/04/metadata"', '')

package_file_content = (parker.data(parse_xml(package_file_content), preserve_root=True))

record_types = next((a for a in package_file_content['Package']['types'] if a['name'] == 'RecordType' ), None)['members']

record_type_dict = defaultdict(list)
for k, v in [record_type.split('.') for record_type in record_types]:
    record_type_dict[k].append(v)

record_type_visibilities_nodes = list()
for object_name, record_type in record_type_dict.items():
    for index, record_type in enumerate(record_type_dict[object_name]):
        record_type_visibilities_nodes.append( ('' + 
            '<recordTypeVisibilities>'                                      + '\n' + 
            '    <default>{is_default}</default>'                           + '\n' + 
            '    <recordType>{object_name}.{record_type_name}</recordType>' + '\n' + 
            '    <visible>true</visible>'                                   + '\n' + 
            '</recordTypeVisibilities>').strip().format(
                is_default=('true' if index == 0 else 'false'),
                object_name=object_name,
                record_type_name=record_type
            ) )

print('All record types are visible. (The first RecordType found of each object is set as the default).\n')

print('Writing "package.xml" file...')
with open(os.path.join(go_up(file_dir), 'package.xml'), mode='w') as f:
    f.write(
        '<?xml version="1.0" encoding="UTF-8"?>                    ' + '\n' + 
        '<Package xmlns="http://soap.sforce.com/2006/04/metadata"> ' + '\n' + 
        '  <types>                                                 ' + '\n' + 
        '    <name>Profile</name>                                  ' + '\n' + 
        '    <members>*</members>                                  ' + '\n' + 
        '  </types>                                                ' + '\n' + 
        '  <version>45.0</version>                                 ' + '\n' + 
        '</Package>'
    )
print('File written.\n')
        
print('Writing "Admin" profile...')

field_permissions_str = '\n'.join(profile_nodes)
tab_visibilities_str = '\n'.join(tab_nodes)
record_type_visibility_str = '\n'.join(record_type_visibilities_nodes)

with open(os.path.join(file_dir, 'Admin.profile-meta.xml'), mode='w') as f:
    f.write(
        '<?xml version="1.0" encoding="UTF-8"?>'                    + '\n' +
        '<Profile xmlns="http://soap.sforce.com/2006/04/metadata">' + '\n' +
        field_permissions_str                                       + '\n' +
        record_type_visibility_str                                  + '\n' +
        tab_visibilities_str                                        + '\n' +
        '</Profile>'
    )
print('Admin profile written.\n')
