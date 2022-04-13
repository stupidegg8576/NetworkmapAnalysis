import yaml
import json
import sys
import os

opts = sys.argv

input_type = None
output_type = None
output_path = None

# get input file path
if len(opts) > 1:
    input_path = opts[1]

# check if file exists and file format
if os.path.exists(input_path):

    if 'json' in input_path:
        input_type = 'json'
        output_type = 'yaml'
    elif 'yaml' in input_path:
        input_type = 'yaml'
        output_type = 'json'
else:
    print('input file not exist')
    raise FileExistsError('input file not exist')

# get output file path
if len(opts) > 2:
    if output_type in opts[2]:
        output_path = opts[2]
    else:
        print('Something wrong with output file path')
# if not assigning output file path
else:
    print('Using default output file path')
    output_path = input_path[0:-4] + output_type

try:
    input_file = open(input_path, 'r')
except IOError:
    raise IOError('Something wrong with open input file')

if input_type == 'json':
    input_dict = json.loads(input_file.read())
elif input_type == 'yaml':
    input_dict = yaml.load(input_file, Loader=yaml.FullLoader)

input_file.close()

print('convert ' + input_path + ' to :' + output_path)

try:
    output_file = open(output_path, 'w')
except IOError:
    raise IOError('Something wrong with open output file')

if output_type == 'json':
    output_file.write(json.dumps(input_dict, indent=4))
elif output_type == 'yaml':
    output_file.write(yaml.dump(input_dict,  sort_keys=False))
