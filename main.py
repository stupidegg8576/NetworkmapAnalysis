import pandas
import tag_apply
import tag_searching 
import tag_filtering
import sys
import getopt


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

def apply_tag(device_data:pandas.DataFrame, tag_data_path:str, max_search:int = 0) -> pandas.DataFrame:
    device_with_tag, device_without_tag = tag_apply.apply_tag(device_data, tag_data_path, max_search)
    return device_with_tag, device_without_tag 

def search_tag(device_data:pandas.DataFrame, max_search:int = 0):
    #searching common substring as tags
    #output_file = pandas.DataFrame(tag_searching.tag_search(device_data, max_search=max_search))
    #vendor_tag = tag_searching.tag_search(device_data.loc[:,'Vendor_Class'].to_list())
    print(device_data)
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

def convert_to_lower_case(device_data:pandas.DataFrame) -> pandas.DataFrame:
    
    for a in device_data.columns:
        device_data[a] = device_data[a].str.lower().str.strip()
    return device_data
        

if __name__ == '__main__':
    sys.argv = ['.\\main.py', '-i', '.\\Data\\device_vh.csv', '-t', '.\\tag.yaml', '-n', '.\\Data\\New_tag.csv', \
                    '-o', '.\\Data\\Device_with_tag.csv', '-u', '.\\Data\\Device_without_tag.csv', '-m', '100']
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:t:o:u:n:m:", ["input_file=", "input_tag_data=", \
                                                "output_with_tag=", "output_without_tag=", "output_new_tag", "maximum_search="])
    except getopt.GetoptError:
        print("Something wrong with opts")
        raise getopt.GetoptError("Something wrong with opts")
    
    maximum_search = 0
    print(opts)
    

    for i in opts:
        if len(i) < 2:
            raise getopt.GetoptError("Something wrong with opts")
        if i[0] == '-i':
            input_device_data_path = i[1]
        elif i[0] == '-t':
            input_tag_data_path = i[1]
        elif i[0] == '-o':
            output_path_device_with_tag = i[1]
        elif i[0] == '-u':
            output_path_device_without_tag = i[1]
        elif i[0] == '-n':
            output_path_new_tag = i[1]
        elif i[0] == '-m':
            try:
                maximum_search = int(i[1])
            except ValueError:
                raise getopt.GetoptError("opt: maximum search error")            
        else:
            print("FGDFG")
            print(i)
            raise getopt.GetoptError("Something wrong with opts")

    #read device data(only with vendor and host name)
    device_DataFrame = read_device_data_file(input_device_data_path)
    #conver to lower case
    device_DataFrame = convert_to_lower_case(device_DataFrame)

    #apply tag in tag file to all device 
    device_with_tag, device_without_tag = apply_tag(device_DataFrame, input_tag_data_path, maximum_search)    
    
    #save the result
    device_with_tag = pandas.DataFrame.from_dict(device_with_tag, orient='index') 
    device_without_tag = pandas.DataFrame.from_dict(device_without_tag, orient='index')
    
    #creat index list
    index=['Vendor_Class','Host_Name']
    device_without_tag.set_axis(index, axis='columns', inplace=True)
    for i in range(2,device_with_tag.columns.stop):
        index.append('Tag_' + str(i-1))
    device_with_tag.set_axis(index, axis='columns', inplace=True)
    
    #output to .csv
    device_with_tag.to_csv(output_path_device_with_tag, sep=';', index=False)  
    device_without_tag.to_csv(output_path_device_without_tag, sep=';', index=False)  

    '''
    #searching new tag in device has no tag
    search_result = search_tag(device_without_tag, max_search=0)
    filtered_tag = filter_tag(search_result, max_search=0)
    #save new tags
    output_file = pandas.DataFrame(filtered_tag, index=['Count']).rename_axis('Tag', axis=1).transpose().reset_index()
    print(output_file)
    output_file.to_csv(output_path_new_tag, sep=';')        
   
        
    #output_file = pandas.DataFrame(filter_tag(device_data),index=['Count']).rename_axis('Name', axis=1).transpose().reset_index()
    #output_file = search_tag(device_data)
    #output_file = apply_tag(device_data, max_check=0)
    #
    #tag_apply.print_tag_static()
'''