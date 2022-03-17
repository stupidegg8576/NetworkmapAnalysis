def tag_search(device_without_tag:list, device_list:list, max_search:int = 0, minimum_search_string_len:int = 3) -> dict:
    #for all device_without_tag, search all other device in device list 
    #try to find keywords for generating new tag
    tags = {} 
    n = 0
    l = '/' + str(len(device_without_tag))

    for device_without_tag_name in device_without_tag:
        
        #max loop times
        n = n + 1 
        if max_search != 0 and n >= max_search:
            break
        if not n % 10:
            print("tag_search: " + str(n) + l ,end='\r')
        
        #from each device_without_tag_name
        #get all sub string longer than minimum string long
        #and search how many times it apears in device_list      
        for start in range(0,len(device_without_tag_name) - minimum_search_string_len):
            if device_without_tag_name[start:] in tags:
                #if already in dictionary, pass
                break                
            for end in range(len(device_without_tag_name), start + minimum_search_string_len, -1):
                if device_without_tag_name[start:end] in tags:
                    #if already in dictionary, pass
                    break
                #store the number of device has tag in tags{}       
                tags[device_without_tag_name[start:end]] = search_device_data(device_list, device_without_tag_name[start:end])
    
    print("\nRemoving useless tags")
    #sort tag by device number
    tags = dict(sorted(tags.items(),key= lambda item: item[1], reverse=True)) 
    temp = {}
    n = 0
    l = '/' + str(len(tags))
    for t in tags:
        n = n + 1
        if not n % 1000:
            print("Removing: " + str(n) + l ,end='\r')

        if tags[t] > 10:
            temp[t] = tags[t]
        else:
            break

    print("\nTag search done!")    
    return temp


def search_device_data(device_list:list, target_device_name:str) -> int:
    count = 0
    for device_name in device_list:
        if target_device_name in device_name:
            count = count + 1
    return count            

    