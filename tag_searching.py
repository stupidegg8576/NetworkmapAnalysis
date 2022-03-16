import pandas
import time

#setting




def tag_search(device_data:list, max_search:int = 0) -> dict:
    tags = {} 
    n = 0
    l = '/' + str(len(device_data))
    for device in device_data:
        #max loop times
        n = n + 1       

        if max_search != 0 and n >= max_search:
            break

        if not n % 10:
            print("tag_search: " + str(n) + l ,end='\r')

        if device in tags:
            #if already in dictionary, pass 
            continue
        else:
            #mim string long
            MIN_STRING_LEN = 2
            for start in range(0,len(device) - MIN_STRING_LEN):                
                for end in range(len(device), start + MIN_STRING_LEN, -1):
                    if device[start:end] in tags:
                        #if already in dictionary, pass
                        break
                    #store the number of device has tag in tags{}       
                    tags[device[start:end]] = search_device_data(device_data,device[start:end])
    
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

        if tags[t] > 5:
            temp[t] = tags[t]
        else:
            break

    print("\nTag search done!")    
    return temp


def search_device_data(device_data:list, target:str) -> int:
    count = 0
    for device in device_data:
        if target in device:
            count = count + 1
    return count            

    