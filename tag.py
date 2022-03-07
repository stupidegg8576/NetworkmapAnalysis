import yaml

TAGFILE_PATH = 'tag.yaml'
MAX_TAG = 10

def tagfile_check(tagyaml):
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
    
    print("Tagfile Check Pass")

def with_check(target_string:list, vendor_class:str, host_name:str):
    #check if vendor calss or host name contain any target strings 
    if type(target_string) is not list or type(vendor_class) is not str or type(host_name) is not str:
        raise BaseException("withcheck: input wrong data type")
    
    for s in target_string:
        if s.lower() in vendor_class or s.lower() in host_name:
            return True
            #if a target string is in vendor class or host name
    
    #doesn't contain any target string
    return False 
    
def without_check(target_string:list, vendor_class:str, host_name:str):
    #check if vendor calss or host name contain any target strings 
    if type(target_string) is not list or type(vendor_class) is not str or type(host_name) is not str:
        raise BaseException("withoutcheck: input wrong data type")

    for s in target_string:
        if s.lower() not in vendor_class and s.lower() not in host_name:
            #if any target string is not in vendor class and host name
            return True            
    
    #all target string is in vendor class or host name
    return False 
   
def exactly_with_check(target_string:list, vendor_class:str, host_name:str):
    #check if vendor calss or host name contain target strings 
    #and no other letters infront or behind target strings
    if type(target_string) is not list or type(vendor_class) is not str or type(host_name) is not str:
        raise BaseException("exactlywithcheck: input wrong data type")

    for s in target_string:
        v = vendor_class.find(s.lower())
        h = host_name.find(s.lower())
        vcheck = True
        hcheck = True
        if v > 0:
            #contain s
            if v == 0:
                #s is at start of v, skip check infront
                pass
            elif vendor_class[v-1].isalpha():
                #the char infront s is a letter
                vcheck = False
            if v + len(s) == len(vendor_class):
                #s is at the last char of vendor_class
                pass
            elif vendor_class[v-1].isalpha():
                #the char after s is a letter
                vcheck = False                
        else:
            #doesn't contain s
            vcheck = False
        if h > 0:
            #contain s
            if h == 0:
                #s is at start of h, skip check infront
                pass
            elif host_name[h-1].isalpha():
                #the char infront s is a letter
                hcheck = False
            if h + len(s) == len(host_name):
                #s is at the last char of host_name
                pass
            elif host_name[v-1].isalpha():
                #the char after s is a letter
                hcheck = False                
        else:
            #doesn't contain s
            hcheck = False

        if vcheck or hcheck:
            #a target string exactly in vendor class or host name
            return True

    #after for loop, no any target string is exactly in vendor class or host name 
    return False 
    
def mac_check(target_string:list, mac_addr:str):
    #check if Mac matched any target Mac
    if type(target_string) is not list or type(mac_addr) is not str:
        raise BaseException("maccheck: input wrong data type")


    for s in target_string:        
        for i in len(s):
            if s[i] != 'X' or s[i] != 'x' or s[i] != mac_addr[i]:
                #Fail if 'X', fail if != x and mac
                break
            #success if any Mac addr fully matched
            return True                        
    #didn't match any target mac addr    
    return False

def has_tag(target_tag:list, tags:list):
    #check if any target tag is in the previous tag list
    for t in target_tag:
        if t.lower() in tags:
            #if any target tag is in the list
            return True
    return False

def no_tag(target_tag:list, tags:list):
    #check if any target tag is not in the previous tag list
    for t in target_tag:
        if t.lower() not in tags:
            #if any tatget tag is in the list
            return True
    return False

def get_tags(mac_addr:str, vendor_class:str, host_name:str):
    
    passed_tags = []
    """
    Tag structure will be like:

    Apple: #tag name
        con1: #conditions
            with: [apple,Apple]  #subconditions and their target strings
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
                        check_flag = without_check(tagyaml[tag][conditions][subconditions],vendor_class,host_name)
                    
                    elif subconditions.startswith('with'):
                        check_flag = with_check(tagyaml[tag][conditions][subconditions],vendor_class,host_name)
                    
                    elif subconditions.startswith('exactlywith'):
                        check_flag = exactly_with_check(tagyaml[tag][conditions][subconditions],vendor_class,host_name)
                    
                    elif subconditions.startswith('mac'):
                        check_flag = mac_check(tagyaml[tag][conditions][subconditions],mac_addr)
                                        
                    elif subconditions.startswith('hastag'):
                        #send all previous tag to check if this device has a tag or not
                        check_flag = has_tag(tagyaml[tag][conditions][subconditions],passed_tags)
                        
                    elif subconditions.startswith('notag'):
                        check_flag = no_tag(tagyaml[tag][conditions][subconditions],passed_tags)
                                            
                    else:
                        raise BaseException("Tag file error: can't find subcondition")

                    if check_flag is False:
                        #subconditions and together
                        #so no need to keep going when any subconditions failed
                        break
                        
                #check will stay at true if passed all check
                if check_flag:
                    #add tag to success tag if any condition was fully passed 
                    passed_tags.append(tag)              
                    #stop checking this tag and try next tag
                    break 
                    
    
    return passed_tags



try:
    #read tagfile
    file = open(TAGFILE_PATH,'r')    
except Exception:
    raise BaseException("Tagfile Read Failed : " + TAGFILE_PATH)

print("Read tagfile : " + TAGFILE_PATH)

tagyaml = yaml.load(file,Loader=yaml.CLoader)
tagfile_check(tagyaml)