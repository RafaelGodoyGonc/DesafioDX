#!/usr/bin/env python3
import csv, json, re, os, requests
from datetime import datetime
from itertools import islice

def get_ts():
    return str(datetime.timestamp(datetime.now())).replace('.','')

id_prop = 'id'

username_scratch = ''
user_id_scratch = '' 

valid_id_props = [
    id_prop, 
    id_prop.lower(),
    id_prop.capitalize(),
    id_prop.upper()    
]

invalid_row_props = [
    '_',
    'type'
]

invalid_file_props = [
    'totalSize',
    'done'
]

api_version = '45.0'

id_regex_pattern = re.compile(
    r'^(001|002|003|005|006|007|008|00a|00b|00B|00D|00E|00e|00G|00h|00i|00I|00J|00j|00K|00k|00l|00N|00o|00O|00p|00P|00q|00Q|00r|00S|00T|00t|00U|00v|00X|00Y|010|011|012|015|016|018|019|01a|01D|01H|01I|01M|01m|01n|01N|01o|01p|01q|01Q|01r|01s|01t|01u|01Y|01Z|020|021|022|026|027|028|029|02a|02c|02i|02n|02o|02s|02Z|033|035|03d|03g|03j|03s|03u|04g|04h|04i|04k|04l|04m|04s|04t|04v|04W|04X|04Y|058|059|05X|060|066|068|069|07E|07L|07M|081|082|083|087|08e|08s|091|092|093|099|09a|0A2|0a2|0A3|0ab|0aD|0ad|0am|0BM|0C0|0c0|0c1|0ca|0cs|0D2|0D5|0DM|0dr|0E8|0eb|0eH|0en|0eo|0ep|0EP|0eq|0fr|0gv|0hc|0hd|0ht|0in|0J0|0Ja|0Jb|0Jd|0Je|0Jf|0Jg|0Ji|0Jj|0Jk|0Jl|0Jm|0Jn|0Jo|0Jp|0Jq|0Jr|0Js|0Jt|0JT|0Ju|0JU|0JV|0Jv|0JW|0JX|0JY|0Jy|0JZ|0Jz|0K0|0K2|0K3|0K4|0K6|0K7|0K9|0ka|0KA|0Ka|0Kb|0KB|0Kc|0KD|0Kd|0Ke|0KG|0Kg|0Kh|0Ki|0Km|0KM|0Kn|0KO|0Ko|0KP|0Kp|0Kq|0Kr|0KR|0Ks|0Kt|0Ku|0KY|0KZ|0Kz|0L2|0L3|0L4|0L5|0LC|0Lc|0LD|0Ld|0LE|0Le|0Lf|0Lg|0LG|0LH|0LI|0Li|0Lj|0LJ|0Lm|0LM|0LN|0LO|0Lo|0Lq|0Ls|0Lu|0LV|0Lw|0Lx|0Ly|0M0|0M1|0M2|0M3|0M4|0M5|0M6|0M9|0MA|0Ma|0Mb|0MD|0ME|0MF|0Mf|0Mg|0MH|0Mi|0MI|0MJ|0Mk|0MK|0MN|0MO|0Mp|0MQ|0MR|0Ms|0mt|0Mt|0MT|0Mu|0MV|0MW|0My|0MY|0MZ|0Mz|0N0|0N1|0N2|0N3|0N4|0N5|0N9|0Na|0NB|0NC|0ND|0Nd|0NE|0Ne|0Nf|0Ng|0Nh|0Ni|0NI|0Nj|0NK|0NL|0NM|0NN|0No|0Np|0NQ|0NR|0ns|0Nt|0NU|0NV|0Nv|0NW|0Nw|0NX|0NZ|0O0|0O1|0O6|0O7|0O8|0Oa|0OB|0Ob|0OC|0OD|0Oe|0OE|0Of|0OF|0OG|0OH|0OI|0Oi|0OL|0Om|0OO|0OP|0Oq|0Or|0OV|0OZ|0P0|0P1|0P2|0P9|0Pa|0PB|0PC|0PD|0PF|0PK|0Pk|0PL|0Pl|0Pm|0PO|0PP|0Pp|0Pq|0PQ|0Pr|0Ps|0PS|0Pt|0Pu|0Pv|0Px|0PX|0Py|0Pz|0PZ|0Q0|0Q1|0Q3|0Q5|0Q7|0Qb|0Qc|0QD|0Qd|0Qg|0Qi|0QJ|0Qj|0QK|0Qk|0QL|0QM|0Qn|0Qo|0QO|0QP|0Qp|0QR|0QT|0Qt|0QU|0QV|0QY|0Qy|0Qz|0QZ|0R0|0R1|0R2|0R8|0RA|0Rb|0RB|0RC|0RD|0Rd|0RE|0Rf|0Rg|0RH|0Rh|0Ri|0RJ|0RL|0Rl|0RM|0Rp|0rp|0Rr|0rs|0Rt|0RT|0Ru|0Rv|0RX|0Rx|0RY|0RZ|0S1|0S2|0Sa|0sa|0SE|0Sk|0SL|0SM|0Sn|0SO|0SP|0sp|0SR|0sr|0ST|0SU|0SV|0Sy|0t0|0T0|0T5|0T6|0ta|0te|0tg|0TH|0TI|0TJ|0Tj|0tn|0TN|0TO|0tr|0tR|0TR|0ts|0Ts|0TS|0tS|0Tt|0TT|0tu|0Tv|0Tw|0TY|0U5|0Ua|0UM|0up|0ur|0US|0UT|0W0|0W1|0W2|0W3|0W4|0W5|0W7|0W8|0WA|0WB|0WC|0WD|0WE|0WF|0WG|0WH|0WI|0WJ|0WK|0WL|0WM|0WO|0XA|0XB|0XC|0XD|0XE|0XH|0XR|0XU|0Xv|0Ya|0Ym|0Yq|0Ys|0Yu|0Yw|0ZA|0ZQ|0Zx|100|101|102|10y|10z|110|111|112|113|11a|130|131|149|19i|1AB|1AR|1bm|1br|1CA|1cb|1CB|1CC|1CF|1ci|1CL|1cl|1cm|1CP|1cr|1CS|1dc|1de|1do|1dp|1dr|1DS|1ED|1EF|1EP|1Ep|1ES|1EV|1FS|1gh|1gp|1HA|1HB|1HC|1JS|1L7|1L8|1LB|1MA|1Mc|1MC|1MP|1mr|1NR|1o1|1OZ|1pm|1ps|1rp|1rr|1S1|1sa|1SA|1Sl|1SR|1ST|1te|1ts|1vc|1WK|1WL|200|201|202|203|204|205|208|26Z|2AS|2CE|2ED|2EP|2FE|2FF|2hf|2LA|2oN|2SR|300|301|307|308|309|30a|30A|30c|30C|30d|30D|30e|30f|30F|30g|30L|30m|30p|30Q|30r|30R|30S|30t|30v|30V|30W|30X|310|31A|31C|31c|31d|31i|31o|31S|31V|31v|31w|31x|31y|31z|3Db|3DP|3Dp|3DS|3HP|3J5|3M0|3M1|3M2|3M3|3M4|3M5|3M6|3MA|3MB|3MC|3MD|3ME|3MF|3MG|3MH|3MI|3MJ|3mK|3MK|3Ml|3MM|3MN|3MO|3MQ|3MR|3MS|3Mt|3MT|3MU|3MV|3MW|3N1|3NA|3NC|3NO|3NS|3NT|3NU|3NV|3NW|3NX|3NY|3NZ|3Pb|3Ph|3PP|3Pp|3PS|3PX|3SP|3SS|400|401|402|403|404|405|406|407|408|410|412|413|4A0|4ci|4cl|4co|4dt|4F0|4F1|4F2|4F3|4F4|4F5|4fe|4fp|4ft|4ie|4M5|4M6|4NA|4NB|4NC|4ND|4NW|4pb|4pv|4sr|4st|4sv|4ve|4ws|4wt|4Wz|4xs|500|501|550|551|552|555|557|570|571|572|573|574|5CS|5Pa|5Sp|600|601|602|604|605|606|607|608|62C|6AA|6AB|6AC|6AD|6EB|6pS|6SS|700|701|707|708|709|70a|70b|70c|70d|710|711|712|713|714|715|716|729|737|750|751|752|753|754|766|777|7dl|7Eh|7Eq|7Er|7pV|7tf|7tg|800|801|802|803|804|805|806|807|80D|810|811|817|820|822|823|824|825|828|829|82B|888|889|906|907|910|911|912|9BV|9DV|9NV|9yZ|a[a-zA-Z0-9][a-zA-Z0-9]|e[a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9]|m[a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9]|z[a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9]|k[a-zA-Z][0-9a-z])\w{12,15}$'
)


def get_chunk(it, size):
    it = iter(it)
    return iter(lambda: tuple(islice(it, size)), ())

def convert_to_json(file_name, object_type):
    csv_path = file_name
    if not file_name.endswith('.csv'):
        csv_path = file_name + '.csv'

    csv_path = os.path.join(root_csv_path, csv_path)

    json_path = os.path.join (root_json_path, (file_name.replace('.csv', ''))+'.json')
    json_path_exists = os.path.exists(json_path)

    csv_file = open( csv_path, 'r', encoding="utf8")
    reader = csv.DictReader(csv_file)

    correct_json = {}
    correct_data = []

    map_id_json = {}
    
    if json_path_exists:
        map_id_json = get_map_id_json(object_type)

    for row in reader:
        remove_row_invalid_props(row)
        add_references(row, object_type)
        if not json_path_exists or  map_id_json[row['attributes']['referenceId']] == 'Empty':
            correct_data.append(row)


    correct_json['data'] = correct_data 
    if not json_path_exists: 
        result = json.dumps(correct_json, ensure_ascii=False)
        json_file = open( json_path, 'w+', encoding="utf8")
        json_file.write(result)
        json_file.close()

    return (correct_data, object_type)

def remove_row_invalid_props(row):
    for invalid_prop in invalid_row_props:
        invalid_prop_candidates = [
            invalid_prop, 
            invalid_prop.lower(),
            invalid_prop.capitalize(),
            invalid_prop.upper()
        ]

        for prop in invalid_prop_candidates:
            if prop in row:
                del row[prop]
                break

def remove_file_invalid_props(file):
    for prop in invalid_file_props:
        if prop in file:
            del file[prop]
    
def add_references(row, object_type):

    for id_prop in valid_id_props:
        if id_prop in row:
            row['attributes'] = {
                "referenceId": row[id_prop],
                "type": object_type,
                "Id" : "Empty"
            }
            del row[id_prop]

    for prop in row:
        if not prop is None and prop.lower() != 'id' and prop.lower() != 'attributes':
            target_value = row[prop]
            if is_id(target_value) or target_value == '--UserId--':
                value_to_translate = '@{}'.format(target_value)
                row[prop] = translation_dict.get(value_to_translate)
            elif object_type.lower() == 'user' and (prop.lower() == 'username'):
                row[prop] = row[prop].replace('@', '@'+get_ts())
            else:
                if isinstance(row[prop], str):
                    if not row[prop]:
                        row[prop] = None

def is_id(value):
    return value != None and isinstance(value, str) and re.match(id_regex_pattern, value)

def convert_csv_to_json(f):
    object_type = get_object_type(f)
    if isinstance(f, str):
        print('Processing {}...'.format(f))
        return convert_to_json(f, object_type)
    elif isinstance(f, dict):
        print('Processing {}...'.format(f['path']))
        return convert_to_json(f['path'], object_type)

def get_object_type(f):
    if isinstance(f, str):
        return f.replace('.csv', '')
    elif isinstance(f, dict):
        return f['object']

def put_saved_id_salesforce(object_type, result):
    with open(os.path.join(root_json_path,  (object_type.replace('.csv', ''))+'.json'), 'r', encoding="utf8") as fin:
        objs = json.loads(fin.read())
        for rows in objs['data']:
            if rows['attributes']['referenceId'] == result['referenceId']:
                rows['attributes']['Id'] = result['id']
    
    result = json.dumps(objs, ensure_ascii=False)
    json_file = open(os.path.join(root_json_path,  (object_type.replace('.csv', ''))+'.json'), 'w+', encoding="utf8")
    json_file.write(result)
    json_file.close()

def get_saved_id_salesforce():
    folders = []
    with os.scandir(root_json_path) as listOfEntries:
        for entry in listOfEntries:
            if entry.is_file():
                folders.append(entry.name)
            
    for f in folders:
        with open(os.path.join(root_json_path, f), 'r', encoding="utf8") as fin:
            objs = json.loads(fin.read())
            for rows in objs['data']:
                translation_dict['@{}'.format(rows['attributes']['referenceId'])] = rows['attributes']['Id']

def get_map_id_json(object_type):
    map_id_json = {}
    with open(os.path.join(root_json_path, object_type+'.json'), 'r', encoding="utf8") as fin:
        objs = json.loads(fin.read())
        for rows in objs['data']:
            map_id_json[rows['attributes']['referenceId']] = rows['attributes']['Id']
    return map_id_json

#while not in root dir
while 'sfdx-project.json' not in os.listdir('.') :
    os.chdir('..')

project_root_dir = os.getcwd()
settings_file_path = os.path.join(project_root_dir, 'scripts', 'settings.json')
root_csv_path = os.path.join(project_root_dir, 'scripts', 'csv')
record_type_csv_path = os.path.join(project_root_dir, 'scripts', 'csv', 'RecordType.csv')
profile_csv_path = os.path.join(project_root_dir, 'scripts', 'csv', 'Profile.csv')
translation_file_path = os.path.join(root_csv_path, 'scripts', 'translation.json', )
root_json_path = os.path.join(project_root_dir, 'scripts', 'csv', 'converted-output')
root_json_path_error = os.path.join(project_root_dir, 'scripts', 'csv', 'converted-output-error')

translation_dict = {}

# if os.path.exists(translation_file_path):
#     translation_file = open( translation_file_path, 'w')
#     translation_file.write(json.dumps(translation_dict))
#     translation_file.close()

if not os.path.isdir(root_csv_path):
    os.mkdir(root_csv_path)

if not os.path.isdir(root_json_path):
    os.mkdir(root_json_path)

if not os.path.isdir(root_json_path_error):
    os.mkdir(root_json_path_error)
print('\nImporting files...\n')

auth_data = json.loads(
    os.popen('sfdx force:org:display --json').read()
)['result']

username_scratch = auth_data['username']

request_headers = {
    "Authorization": 'Bearer {}'.format(auth_data['accessToken']),
    "Content-Type": "application/json",
}

record_type_dict = {}
profile_dict = {}

record_type_query_results = json.loads(
    os.popen('sfdx force:data:soql:query -q "SELECT id, developername, name, sobjecttype FROM RecordType" --json').read()
)['result']['records']

profile_query_results = json.loads(
    os.popen('sfdx force:data:soql:query -q "SELECT Id, name FROM Profile" --json').read()
)['result']['records']

user_id_scratch = json.loads(
    os.popen('sfdx force:data:soql:query -q "SELECT Id, username FROM User WHERE Username = \'{}\'" --json'.format(username_scratch)).read()
)['result']['records']

translation_dict['@--UserId--'] = user_id_scratch[0]['Id']

get_saved_id_salesforce()

rt_file_exists = os.path.exists(record_type_csv_path)
profile_file_exists = os.path.exists(profile_csv_path)
convert_json_file_exists = os.path.exists(root_json_path)

if rt_file_exists:
    record_type_result, _ = convert_csv_to_json('RecordType.csv')

    for record_type in record_type_result:

        key = '{}__{}'.format(record_type['SobjectType'], record_type['DeveloperName'])
        record_type_dict[key] = record_type['attributes']['referenceId']

    for result in record_type_query_results:
        key = '{}__{}'.format(result['SobjectType'], result['DeveloperName'])
        if key in record_type_dict:
            origin_id = record_type_dict[key]
            record_type_target_id = result['Id']
            translation_dict['@{}'.format(origin_id)] = record_type_target_id
    
    print('RecordType translated successfully.\n')

if profile_file_exists:
    profile_result, _ = convert_csv_to_json('Profile.csv')

    for profile in profile_result:

        key = profile['Name']
        profile_dict[key] = profile['attributes']['referenceId']

    for profile_result in profile_query_results:
        key = profile_result['Name']
        if key in profile_dict:
            origin_id = profile_dict[key]
            profile_target_id = profile_result['Id']
            translation_dict['@{}'.format(origin_id)] = profile_target_id
    
    print('Profile translated successfully.\n')

try:
    settings = open(settings_file_path, 'r', encoding="utf8").read()
except:
    print('The file "scripts/settings.json" does not exist.')

try:
    file_names = json.loads(settings)['csvFiles']
except:
    print('The files are not listed as the "csvFiles" property in the "scripts/settings.json" file.')

for file_name in file_names:
    print('')
    stored_result, object_type = convert_csv_to_json(file_name)
    
    file_endpoint = ('{instance_url}/services/data/v{api_version}/composite/tree/{object_type}'.format(
        instance_url = auth_data['instanceUrl'],
        api_version = api_version,
        object_type = object_type
    ))

    chunk_size = (len(stored_result) // 200) + 1
    current_chunk = 1

    for chunk in get_chunk(stored_result, 200):
        print('Running chunk {} of {}...'.format(current_chunk, chunk_size))
        response = requests.post(file_endpoint, data=json.dumps({"records": chunk}), headers=request_headers)

        if response.ok:
            
            operation_result = json.loads(response.text)
            
            if not operation_result['hasErrors']:
                for result in operation_result['results']:
                    translation_dict['@{}'.format(result['referenceId'])] = result['id']
                    put_saved_id_salesforce(object_type, result)

                print('File chunk imported successfully.\n')
            else:
                result = json.dumps(response, ensure_ascii=False)

                json_file = open(os.path.join( root_json_path_error, '{} - {}_{}.json'.format(object_type, current_chunk, chunk_size)), 'w')
                json_file.write(result)
                json_file.close()
                print('Request failed. Result: \n\n{} - {}/{}'.format(object_type, current_chunk, chunk_size))
                #exit()

        else:
            result = json.dumps(response.text, ensure_ascii=False)

            json_file = open(os.path.join( root_json_path_error, '{} - {}_{}.json'.format(object_type, current_chunk, chunk_size)), 'w')
            json_file.write(result)
            json_file.close()
            print('Request failed. Result: \n\n{} - {}_{}'.format(object_type, current_chunk, chunk_size))
            #exit()
        
        current_chunk += 1