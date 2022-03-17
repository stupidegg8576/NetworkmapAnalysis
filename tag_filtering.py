import time
import pandas


#minimum number to count as a tag
MIN = 5

#threshold of counting as a diffrent tag
AS_DIFF_TAG = 0.2



def count_as_diff_tag(a:int, b:int):
    if a > b:
        return ((a - b)/ a) > AS_DIFF_TAG
    else:
        return ((b - a)/ b) > AS_DIFF_TAG

def tag_filter(tag_data:dict, max_search:int = 0) -> dict:
    clean_data = {}
    print("Tag filtering")
    n = 0
    l = ' / ' + str(len(tag_data))
    for tag in tag_data:
        #tag = tag name
        #tag_data[tag] = the number of device has this tag
        
        if not n % 1000:
            print(str(n) + l, end= '\r')
        if max_search != 0 and n >= max_search:
            break
        n = n + 1
        
        is_a_new_tag = True
        for another_tag in tag_data:            
            #if tag is another_tag's substring and two tag's devices number diffirence is not big
            if tag is not another_tag and tag in another_tag and not count_as_diff_tag(tag_data[tag], tag_data[another_tag]):
                is_a_new_tag = False
                break

        #if all other tag are not similar
        if is_a_new_tag:
            clean_data[tag] = tag_data[tag]

    print("\nTag filtering Done!")
    return clean_data
