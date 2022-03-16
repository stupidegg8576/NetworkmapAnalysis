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