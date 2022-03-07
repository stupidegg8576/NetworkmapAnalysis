from re import M
import pandas
import tag

#setting
#device_list.csv
INPUT_DATA_PATH = "Data\\device_list.csv"
OUTPUT_DATA_PATH = "Data\\test.csv"

#Read Device list file
def read_device_data_file(data_path:str):
    try:
        device_data = pandas.read_csv(data_path,on_bad_lines='skip',delimiter=';')    
    except Exception:
        raise FileExistsError("Device list read failed : " + data_path)
    print("Read Device list : " + data_path)
    return device_data


def apply_tag(device_data:pandas.DataFrame, max_check:int = 10000):
    n = 0
    output_file = pandas.DataFrame()
    for device in device_data.iloc():
        #max 
        if (max_check != 0) and (n > max_check):
            break 
        n = n + 1
        if not n % 1000:
            print(str(n) + ' / ' + str(len(device_data)))
        #for each device in data, send MAC, Vendor Class, Host Name, tags[] to get_tags()
        #get_tags() return a list of string of tags
        #convert all string to lower case temporary to avoid case sensitive
        tags = tag.get_tags(device[1],device[2].lower(),device[3].lower())

        if tags:
            #convert gotten tags to pandas.Series 
            tags = pandas.Series(tags)
            #add tags to device data
            device = pandas.concat((device,tags),ignore_index=True)
            #add device data to out put file
            output_file = pandas.concat((output_file,device),ignore_index=True,axis=1)       
    
    return output_file 


if __name__ == '__main__':
    device_data = read_device_data_file(INPUT_DATA_PATH)
    output_file = apply_tag(device_data, max_check=0)
    output_file.T.to_csv(OUTPUT_DATA_PATH)
