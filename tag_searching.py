import pandas

#setting
#how many times find in data to be count as a new tag
COUNT_AS_TAG = 3

tags = {}

def tag_search(device_data:list, max_search:int = 10000) -> dict:
    n = 0
    for device in device_data:
        #max loop times
        n = n + 1
        if max_search != 0 and n >= max_search:
            break

        if not n % 10:
            print("tag_search: " + str(n))

        for start in range(0,len(device)-3):
            #mim string long = 3
            end = len(device)

            while end >= start + 3:
                if search_tag_dict(device[start:end]):
                    #already in dictionary, pass
                    break

                t = search_device_data(device_data,device[start:end])
                
                if t > COUNT_AS_TAG:
                    tags[device[start:end]] = t

                end = end - 1

    return tags


def search_device_data(device_data:list, target:str,max:int = 10000) -> int:
    count = 0
    n = 0
    for device in device_data:
        n = n + 1
        if max != 0 and n > max:
            return count
        if target in device:
            count = count + 1
    return count
            
def search_tag_dict(target:str) -> str:
    #search if target is any existing tag's substring
    for tag in tags:
        if target in tag:
            return tag
    #return '' if none
    return ''


    