import pandas
#import tag_apply
import tag_searching 
import tag_filtering

#setting
#device_list.csv
INPUT_DATA_PATH = "Data\\device_vh.csv"
OUTPUT_DATA_PATH = "Data\\tagfiltered.csv"

#Read Device list file
def read_device_data_file(data_path:str):
    try:
        device_data = pandas.read_csv(data_path,on_bad_lines='skip',delimiter=';')    
    except Exception:
        raise FileExistsError("Device list read failed : " + data_path)
    print("Read Device list : " + data_path)
    return device_data

def write_result_file(data_path:str, data):
    try:
        pandas.read_csv(data_path,on_bad_lines='skip',delimiter=';')    
    except Exception:
        raise FileExistsError("write result file failed : " + data_path)

def apply_tag(device_data:pandas.DataFrame, max_check:int = 0):
    n = 0
    output_file = pandas.DataFrame(device_data)
    
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
        tags = tag_apply.get_tags(device[1],device[2].lower(),device[3].lower())

        if tags:
            #convert gotten tags to pandas.Series 
            tags = pandas.Series(tags)
            #add tags to device data
            device = pandas.concat((device,tags),ignore_index=True)
            #add device data to out put file
            output_file = pandas.concat((output_file,device),ignore_index=True,axis=1)   
    
    return output_file 

def search_tag(device_data:pandas.DataFrame, max_search:int = 0):
    #searching common substring as tags
    #output_file = pandas.DataFrame(tag_searching.tag_search(device_data, max_search=max_search))
    #vendor_tag = tag_searching.tag_search(device_data.loc[:,'Vendor_Class'].to_list())
    device_list = []
    for t in device_data.loc[:,'Host_Name'].to_list():
        t = t.strip()
        if t != '':
            device_list.append(t.strip())
    for t in device_data.loc[:,'Vendor_Class'].to_list():
        t = t.strip()
        if t != '':
            device_list.append(t.strip())

    return tag_searching.tag_search(device_list,max_search)
         
def filter_tag(tag_data:dict, max_search:int = 0) -> dict:

    return tag_filtering.tag_filter(tag_data, max_search)

def convert_to_lower(device_data:pandas.DataFrame) -> pandas.DataFrame:
    
    for a in device_data.columns:
        device_data[a] = device_data[a].str.lower()
    return device_data
        

if __name__ == '__main__':

    device_DataFrame = read_device_data_file(INPUT_DATA_PATH)
    device_DataFrame = convert_to_lower(device_DataFrame)
    search_result = search_tag(device_DataFrame, max_search=0)
    filtered_tag = filter_tag(search_result, max_search=0)
    output_file = pandas.DataFrame(filtered_tag, index=['Count']).rename_axis('Tag', axis=1).transpose().reset_index()
    print(output_file)
    output_file.to_csv(OUTPUT_DATA_PATH, sep=';')        
   
        
    #output_file = pandas.DataFrame(filter_tag(device_data),index=['Count']).rename_axis('Name', axis=1).transpose().reset_index()
    #output_file = search_tag(device_data)
    #output_file = apply_tag(device_data, max_check=0)
    #
    #tag_apply.print_tag_static()
