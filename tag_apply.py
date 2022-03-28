import pandas
import yaml


def tagfile_check(tagyaml:pandas.DataFrame):
    #check if tag file is correct
    if not isinstance(tagyaml,dict):
        raise BaseException("Tagfile Check Failed")
    for tag in tagyaml:
        #apple in tagfile, [apple] is a dict
        if not isinstance(tagyaml[tag],dict):
            raise BaseException("Tagfile Check Failed")
        for conditions in tagyaml[tag]:
            #con1 in apple, [con1] is a dict
            if not isinstance(tagyaml[tag][conditions],dict):
                raise BaseException("Tagfile Check Failed")
            if 'con' in conditions:
                for subconditions in tagyaml[tag][conditions]:
                    #subconditions is in conditions, [subconditions] is a list of strings
                    #with: "[apple,ipad]" this will be tagyaml[tag][conditions][subconditions]
                    if not isinstance(tagyaml[tag][conditions][subconditions],list):
                        raise BaseException("Tagfile Check Failed")
                    #convert tags to lower case
                    tagyaml[tag][conditions][subconditions] = [keyword.replace(keyword, keyword.lower()) for keyword in tagyaml[tag][conditions][subconditions]]
                    
    print("Tagfile Check Pass")

def with_check(keyword:list, device:str):
    #check if vendor calss or host name contain any target strings 
    if type(keyword) is not list or type(device) is not str:
        raise BaseException("withcheck: input wrong data type")
    
    for s in keyword:
        if s in device:
            return True
            #if a target string is in vendor class or host name
    
    #doesn't contain any target string
    return False 
    
def without_check(keyword:list, device:str):
    #check if vendor calss or host name contain any target strings 
    if type(keyword) is not list or type(device) is not str:
        raise BaseException("withoutcheck: input wrong data type")

    for s in keyword:
        if s in device:
            #if any target string is in vendor class and host name
            return False            
    
    #all target string is not in vendor class or host name
    return True 
   
def exactly_with_check(keyword:list, device:str):
    #check if vendor calss or host name contain target strings 
    #and no other letters infront or behind target strings
    if type(keyword) is not list or type(device) is not str:
        raise BaseException("exactlywithcheck: input wrong data type")

    for s in keyword:
        i = device.find(s)
        check = True
        if i > 0:
            #contain s
            if i == 0:
                #s is at start of i, skip check infront
                pass
            elif device[i-1].isalpha():
                #the char infront s is a letter
                check = False
            if i + len(s) == len(device):
                #s is at the last char of vendor_class
                pass
            elif device[i-1].isalpha():
                #the char after s is a letter
                check = False                
        else:
            #doesn't contain s
            check = False

        if check:
            #a target string exactly in vendor class or host name
            return True

    #after for loop, no any target string is exactly in vendor class or host name 
    return False 
    
def mac_check(keyword:list, mac_addr:str):
    #check if Mac matched any target Mac
    if type(keyword) is not list or type(mac_addr) is not str:
        raise BaseException("maccheck: input wrong data type")


    for s in keyword:        
        for i in len(s):
            if s[i] != 'X' or s[i] != 'x' or s[i] != mac_addr[i]:
                #Fail if 'X', fail if != x and mac
                break
            #success if any Mac addr fully matched
            return True                        
    #didn't match any target mac addr    
    return False

def mac_between(target_mac_range:list, mac_addr:str):
    #check if mac_addr is in target mac range
    #target_mac_range[0] <= mac addr <= target_mac_range[1]
    if type(target_mac_range) is not list or type(mac_addr) is not str:
        raise BaseException("mac_between: input wrong data type")
    if len(target_mac_range) < 2:
        # should input at least 2 mac
        raise BaseException("Tag file error: mac_between() input target mac should a list with 2 mac")

    if mac_format_check(mac_addr) is False:
        #mac_addr is a bad mac
        return False

    for c in range(len(mac_addr)):
        if  (target_mac_range[0][c] != 'x' and target_mac_range[0][c] > mac_addr[c]) or \
            (target_mac_range[1][c] != 'x' and target_mac_range[1][c] < mac_addr[c]):
            #target_mac_range[0] <= mac addr <= target_mac_range[1]
            return False
    #pass 
    return True

def mac_format_check(mac:str):

    mac_char = 'abcdefx'

    #check if : is in right place
    for i in range(2,15,3):
        if mac[i] != ':':
            return False

    #check if max is in right format
    for i in (0,1,3,4,6,7,9,10,12,13,15,16):
        if not mac[i].isnumeric() and mac[i] not in mac_char:
            return False
    return True

def has_tag(key_tag:list, device_tags:list):
    #check if any target tag is in the previous tag list
    for t in key_tag:
        if t.lower() in device_tags:
            #if any target tag is in the list
            return True
    return False

def no_tag(key_tag:list, device_tags:list):
    #check if any target tag is not in the previous tag list
    for t in key_tag:
        if t.lower() not in device_tags:
            #if any tatget tag is in the list
            return True
    return False

def get_tags(tagyaml, device:str):
    #input a device info
    #check if its info match any tag's condition in tag file
    device_tags = []
    """
    Tag structure will be like:

    Apple: #tag name
        con1: #conditions
            with: [apple,Apple]  #subconditions and their keywords
            without: [MicroSoft]
        con2: 
            with:[ipad]
    """
    #Apple in tagfile, tagyaml[Apple] is a dict
    for tag in tagyaml:
        #con1 in Apple, [con1] is a dict
        for conditions in tagyaml[tag]:
            #check if conditions is a tag conditions
            #may have other thing in this level in future, reserve for some tag data
            if conditions.startswith('con'):
                #set a flag                 
                check_flag = True

                #with,without... are in conditions
                #subconditions is a string
                #tagyaml[tag][conditions][subconditions] is a list of strings
                for subconditions in tagyaml[tag][conditions]:

                    #with or without or ...
                    
                    if subconditions.startswith('without'):
                        check_flag = without_check(tagyaml[tag][conditions][subconditions], device)
                    
                    elif subconditions.startswith('with'):
                        check_flag = with_check(tagyaml[tag][conditions][subconditions], device)
                    
                    elif subconditions.startswith('exactlywith'):
                        check_flag = exactly_with_check(tagyaml[tag][conditions][subconditions], device)
                    
                    elif subconditions.startswith('mac'):
                        check_flag = mac_between(tagyaml[tag][conditions][subconditions], device)
                                        
                    elif subconditions.startswith('hastag'):
                        #send all previous tag to check if this device has a tag or not
                        check_flag = has_tag(tagyaml[tag][conditions][subconditions], device_tags)
                        
                    elif subconditions.startswith('notag'):
                        check_flag = no_tag(tagyaml[tag][conditions][subconditions], device_tags)
                                            
                    else:
                        raise BaseException("Tag file error: can't find subcondition")

                    if check_flag is False:
                        #subconditions and together
                        #so no need to keep going when any subconditions failed
                        break
                        
                #check will stay at true if passed all check
                if check_flag:
                    #add tag to device_tags if any condition was fully passed 
                    device_tags.append(tag.lower())      
                    '''
                    #update tag_statics
                    if tag_statics.get(tag):
                        tag_statics[tag] = tag_statics[tag] + 1
                    else:
                        tag_statics[tag] = 1'''                        
                    #stop checking this tag and try next tag                    
                    break                     

    return device_tags

def apply_tag(device_data:pandas.DataFrame, input_path_tag_vendor_class:str, input_path_tag_host_name:str, max_check:int=0) -> dict:
    
    tag_vendor_class = read_tag_data_file(input_path_tag_vendor_class, check=True)
    tag_host_name = read_tag_data_file(input_path_tag_host_name, check=True)
    
    n = 0
    device_with_tag = {}
    device_without_tag = {}
    print("Apply tags..")
    l = ' / ' + str(len(device_data))

    for device in device_data.iloc():
        #max 
        if (max_check != 0) and (n > max_check):
            break 
        
        if not n % 100:
            print(str(n) + l,end='\r')
        n = n + 1
        #for each device in data, send MAC, Vendor Class, Host Name, tags[] to get_tags()
        #get_tags() return a list of string of tags
        #convert all string to lower case temporary to avoid case sensitive

        tags = get_tags(tag_vendor_class, device['Vendor_Class'])
        tagsh = get_tags(tag_host_name, device['Host_Name'])   
        for t in tagsh:
            if t not in tags:
                tags.append(t)
        
        #if a device has tag, add it to device_with_tag      
        if tags:
            device_with_tag[n] = [device['Vendor_Class'], device['Host_Name']] + tags
        else:
            device_without_tag[n] = [device['Vendor_Class'], device['Host_Name']]
    
    print("")
    return device_with_tag, device_without_tag


def read_tag_data_file(tag_data_path:str, check=False):
    try:
        #read tagfile
        tag_file = open(tag_data_path,'r')    
    except Exception:
        raise IOError("Tagfile Read Failed : " + tag_data_path)

    print("Read tagfile : " + tag_data_path)

    tagyaml = yaml.load(tag_file, Loader=yaml.FullLoader)
    #check tag data is in right format
    if check:
        tagfile_check(tagyaml)

    return tagyaml