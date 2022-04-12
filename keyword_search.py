from itertools import repeat
import tag_apply
import multiprocessing
import time


def count_as_diff_keyword(a: int, b: int, ratio_count_as_different_tag: float):
    # if the difference of two keyword's device count are bigger than ratio_count_as_different_tag
    # count as two different keyword
    if a > b:
        return ((a - b) / a) > ratio_count_as_different_tag
    else:
        return ((b - a) / b) > ratio_count_as_different_tag


def get_keywords_in_tagfile(setting: dict):
    keywords_in_tagfile = {}

    try:
        tag_host_name = tag_apply.read_tag_data_file(
            setting['input_path_tag_host_name'])
        tag_vendor_class = tag_apply.read_tag_data_file(
            setting['input_path_tag_vendor_class'])
    except IOError:
        print("IOError: keyword_searching get_keyword_in_tagfile")
        raise IOError

    for tag in tag_host_name:
        for conditions in tag_host_name[tag]:
            if 'con' in conditions:
                for subconditions in tag_host_name[tag][conditions]:
                    for keywords in tag_host_name[tag][conditions][subconditions]:
                        # store all keywords in keyword_in_tagfile
                        # -1 means hasn't been searched
                        keywords_in_tagfile[keywords] = -1

    for tag in tag_vendor_class:
        for conditions in tag_vendor_class[tag]:
            if 'con' in conditions:
                for subconditions in tag_vendor_class[tag][conditions]:
                    for keywords in tag_vendor_class[tag][conditions][subconditions]:
                        # store all keywords in keyword_in_tagfile
                        # -1 means hasn't been searched
                        keywords_in_tagfile[keywords] = -1

    return keywords_in_tagfile


def get_keyword_blacklist(setting: dict):
    try:
        keyword_blacklist = tag_apply.read_tag_data_file(
            setting['input_path_keyword_blacklist'])
    except IOError:
        print("IOError: get_keyword_blacklist")
    return keyword_blacklist


def keyword_filter(keywords_data: dict, device_list: list, setting: dict) -> dict:

    # remove tag that less than 10
    temp = {}
    for k in keywords_data:
        if keywords_data[k] > 10:
            temp[k] = keywords_data[k]
        else:
            break
    keywords_data = temp

    n = 0
    l = ' / ' + str(len(keywords_data))
    ratio_count_as_different_tag = setting['ratio_count_as_different_tag']
    maximum_search = setting['maximum_search']

    # get keywords using now from tag datebase
    keywords_in_tagfile = get_keywords_in_tagfile(setting)
    keyword_blacklist = get_keyword_blacklist(setting)

    # to store good keyword and its device count
    good_keywords = {}
    for keyword in keywords_data:
        # tag = tag name
        # tag_data[tag] = the number of device has this tag

        if not n % 100:
            print("Filtering out tags from datebase and blacklist: " +
                  str(n) + l, end='\r')
        if maximum_search != 0 and n >= maximum_search:
            break
        n = n + 1

        # check if new keyword is in keyword_blacklist
        keyword_is_in_blacklist = False
        for blacklist in keyword_blacklist:
            for blackwords in blacklist:
                if keyword in blackwords:
                    keyword_is_in_blacklist = True
                    break
        # if new keyword is in keyword_blacklist, continue to next one
        if keyword_is_in_blacklist:
            continue

        is_a_new_keyword = True
        # find out if there is an another_keyword better than thiskeyword
        for another_keyword in keywords_data:
            # if tag is another_tag's substring and diffirence between two tag's devices number is not big
            if keyword is not another_keyword and keyword in another_keyword and not count_as_diff_keyword(keywords_data[keyword], keywords_data[another_keyword], ratio_count_as_different_tag):
                is_a_new_keyword = False
                break
        for k_in_tagfile in keywords_in_tagfile:
            if keyword != k_in_tagfile and keyword in k_in_tagfile:
                # -1 means keyword hasn't been searched before
                if keywords_in_tagfile[k_in_tagfile] == -1:
                    keywords_in_tagfile[k_in_tagfile] = search_device_data(
                        k_in_tagfile, device_list)[1]
                # if these two keyword are same and the difference of their device count is not big
                # there is already a similar keyword in tag databade
                if not count_as_diff_keyword(keywords_data[keyword], keywords_in_tagfile[k_in_tagfile], ratio_count_as_different_tag):
                    is_a_new_keyword = False
                    break

        # if all other tag are not similar, add it to good keywords
        if is_a_new_keyword:
            good_keywords[keyword] = keywords_data[keyword]

    print("Filtering out tags from datebase and blacklist: " + str(n) + l, end='\r')
    print("\nKeywords filtering Done!")
    return good_keywords


class multi_data():
    pass


def search_a_keyword(device_name, m):

    keyword_this_process = set()
    # from each device_without_tag_name
    # get all sub string longer than minimum string long
    # and search how many times it apears in device_list

    for start in range(0, len(device_name) - m.minimum_search_string_len):
        if device_name[start:] in keyword_this_process:
            # if already in dictionary, break
            # next string is substring of [start:],so if tags cotain [start:], tag will contain all  later strings
            break
        for end in range(len(device_name), start + m.minimum_search_string_len, -1):
            if device_name[start:end] in keyword_this_process:
                # if already in dictionary, pass
                break
            # store the number of device has tag in tags{}
            keyword_this_process.add(device_name[start:end])

    return keyword_this_process


def keyword_search(device_without_tag: list, device_list: list, setting: dict) -> dict:
    # for all device_without_tag, search all other device in device list
    # try to find keywords for generating new tag

    l = '/' + str(len(device_without_tag))

    minimum_search_string_len = setting['minimum_search_string_len']
    print(str(len(device_without_tag)) + " device can't be classified.")

    pool = multiprocessing.Pool(multiprocessing.cpu_count())

    m = multi_data()
    m.device_list = device_without_tag
    m.minimum_search_string_len = minimum_search_string_len
    print("Searching new key word...")
    words = pool.starmap(search_a_keyword, zip(device_without_tag, repeat(m)))

    pool.close()
    pool.join()
    keywords = set()
    for w in words:
        keywords.update(w)

    print("Count the number of device with tags...")

    pool = multiprocessing.Pool(int(multiprocessing.cpu_count()/2))

    temp = pool.starmap(search_device_data, zip(
        list(keywords), repeat(device_without_tag)))

    pool.close()
    pool.join()

    keywords = {}
    for t in temp:
        keywords[t[0]] = t[1]

    # sort tag by device number
    keywords = dict(
        sorted(keywords.items(), key=lambda item: item[1], reverse=True))
    print("\nTag search done!")

    return keyword_filter(keywords, device_without_tag, setting)


def search_device_data(target_substring, device_list):
    count = 0
    for device_name in device_list:
        if target_substring in device_name:
            count = count + 1
    return (target_substring, count)
