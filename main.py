import pandas
import tag_apply
import tag_searching 

#setting
#device_list.csv
INPUT_DATA_PATH = "Data\\device_vh.csv"
OUTPUT_DATA_PATH = "Data\\result.csv"

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

def search_tag(device_data:pandas.DataFrame, max_search:int = 10000):
    #searching common substring as tags
    #output_file = pandas.DataFrame(tag_searching.tag_search(device_data, max_search=max_search))
    #vendor_tag = tag_searching.tag_search(device_data.loc[:,'Vendor_Class'].to_list())
    host_list = []
    for t in device_data.loc[:,'Host_Name'].to_list():
        host_list.append(t.strip())


    host_tag = tag_searching.tag_search(host_list,max_search=1000)
    host_tag = dict(sorted(host_tag.items(),key= lambda item: item[1], reverse=False))
    
    for i in host_tag:
        print(i + " : " + str(host_tag[i]))
    return 
    

if __name__ == '__main__':
    device_data = read_device_data_file(INPUT_DATA_PATH)
    search_tag(device_data)
    #output_file = search_tag(device_data)
    #output_file = apply_tag(device_data, max_check=0)
    #output_file.to_csv(OUTPUT_DATA_PATH)
    #tag_apply.print_tag_static()