import pandas
import tag_apply
import keyword_search
import sys
import yaml
import getopt

# Read Device list file


def read_device_data_file(data_path: str):
    try:
        device_data = pandas.read_csv(
            data_path,  delimiter=';')
    except Exception:
        raise FileExistsError("Device list read failed : " + data_path)
    print("Read Device list : " + data_path)
    return device_data


def write_result_file(data_path: str, data):
    try:
        pandas.read_csv(data_path, on_bad_lines='skip', delimiter=';')
    except Exception:
        raise FileExistsError("write result file failed : " + data_path)


def apply_tag(device_data: pandas.DataFrame, input_path_tag_vendor_class: str, input_path_tag_host_name: str, max_search: int = 0) -> dict:
    device_with_tag, device_without_tag = tag_apply.apply_tag(
        device_data, input_path_tag_vendor_class, input_path_tag_host_name, max_search)
    return device_with_tag, device_without_tag


def search_new_keyword(device_without_tag: pandas.DataFrame, device_list: pandas.DataFrame, setting: dict):
    # split vendor_class and host_name to search new tag
    device_without_tag_vendor_class = []
    device_without_tag_host_name = []
    device_list_vendor_class = []
    device_list_host_name = []

    for t in device_without_tag.loc[:, 'Vendor_Class'].to_list():
        t = t.strip()
        if t != '':
            device_without_tag_vendor_class.append(t)
    for t in device_list.loc[:, 'Vendor_Class'].to_list():
        t = t.strip()
        if t != '':
            device_list_vendor_class.append(t)
    print("searching new Vendor_class keywords")
    vendor_class_tag = keyword_search.keyword_search(
        device_without_tag_vendor_class, device_list_vendor_class, setting)

    for t in device_without_tag.loc[:, 'Host_Name'].to_list():
        t = t.strip()
        if t != '':
            device_without_tag_host_name.append(t)
    for t in device_list.loc[:, 'Host_Name'].to_list():
        t = t.strip()
        if t != '':
            device_list_host_name.append(t)
    print("searching new Host_name keywords")
    host_name_tag = keyword_search.keyword_search(
        device_without_tag_host_name, device_list_host_name, setting)

    return vendor_class_tag, host_name_tag


def convert_to_lower_case(device_data: pandas.DataFrame) -> pandas.DataFrame:
    # convert to lower case and cut off blank space at string end
    device_data['Vendor_Class'] = device_data['Vendor_Class'].str.lower().str.strip()
    device_data['Host_Name'] = device_data['Host_Name'].str.lower().str.strip()
    return device_data


def get_setting():

    setting = {}
    # default settings
    setting['maximum_search'] = 0
    setting['minimum_search_string_len'] = 3
    setting['ratio_count_as_different_tag'] = 0.2
    setting['input_path_tag_vendor_class'] = './Data/tag_vendor.yaml'
    setting['input_path_tag_host_name'] = './Data/tag_host.yaml'
    setting['input_path_device_data'] = './Data/device_list.csv'
    setting['input_path_keyword_blacklist'] = './Data/keyword_blacklist.yaml'
    setting['output_path_device_with_tag'] = './Data/device_device_with_tag.csv'
    setting['output_path_device_without_tag'] = './Data/device_without_tag.csv'
    setting['output_path_new_keyword_vendor_class'] = './Data/new_keyword_vendor_class.csv'
    setting['output_path_new_keyword_host_name'] = './Data/new_keyword_host_name.csv'

    try:
        # read tagfile
        setting_file = open('setting.yaml', 'r')
    except Exception:
        print("Tagfile Read Failed : " + 'setting.yaml')
        print("Using default setting")
        return setting

    print("Read setting file: " + 'setting.yaml')

    # update setting
    setting.update(yaml.load(setting_file, Loader=yaml.FullLoader))

    if type(setting['maximum_search']) == str:
        try:
            setting['maximum_search'] = int(setting['maximum_search'])
        except:
            print("Something wrong in setting.yaml")
    if type(setting['minimum_search_string_len']) == str:
        try:
            setting['minimum_search_string_len'] = int(
                setting['minimum_search_string_len'])
        except:
            print("Something wrong in setting.yaml")
    if type(setting['ratio_count_as_different_tag']) == str:
        try:
            setting['ratio_count_as_different_tag'] = float(
                setting['ratio_count_as_different_tag'])
        except:
            print("Something wrong in setting.yaml")

    return setting


if __name__ == '__main__':
    # load setting
    setting = get_setting()
    opts = sys.argv

    searching_new_keyword = False

    # update setting if using args
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:t:o:u:n:k", ["input_file=", "input_tag_data=",
                                                                 "output_with_tag=", "output_without_tag=", "output_new_tag", "searching new keyword"])
    except getopt.GetoptError:
        print("Something wrong with opts")
        raise getopt.GetoptError("Something wrong with opts")

    maximum_search = 0
    print(opts)

    # update setting if using args
    for i in opts:
        if len(i) < 2:
            raise getopt.GetoptError("Something wrong with opts")
        if i[0] == '-i':
            input_device_data_path = i[1]
        elif i[0] == '-t':
            input_tag_data_path = i[1]
            setting['input_path_device_data'] = i[1]
        elif i[0] == '-v':
            setting['input_path_tag_vendor_class'] = i[1]
        elif i[0] == '-h':
            setting['input_path_tag_host_name'] = i[1]
        elif i[0] == '-o':
            output_path_device_with_tag = i[1]
            setting['output_path_device_with_tag'] = i[1]
        elif i[0] == '-u':
            output_path_device_without_tag = i[1]
            setting['output_path_device_without_tag'] = i[1]
        elif i[0] == '-n':
            output_path_new_tag = i[1]
        elif i[0] == '-k':
            searching_new_keyword = True

    if True:
        # read device data(only with vendor and host name)
        device_DataFrame = read_device_data_file(
            setting['input_path_device_data'])

        # conver to lower case
        device_DataFrame = convert_to_lower_case(device_DataFrame)

        # apply tag in tag file to all device
        # apply_tag will return 2 dict with [vendor_class, host_name] or [vendor_class, host_name, tag1, tag2....]
        device_with_tag, device_without_tag = apply_tag(
            device_DataFrame, setting['input_path_tag_vendor_class'], setting['input_path_tag_host_name'], setting['maximum_search'])

        # convert dict to pandas.DataFrame
        device_with_tag = pandas.DataFrame.from_dict(
            device_with_tag, orient='index')
        device_without_tag = pandas.DataFrame.from_dict(
            device_without_tag, orient='index')

        # creat index list for saving file
        index = ['Vendor_Class', 'Host_Name']

        # device_without_tag only have ['Vendor_Class','Host_Name']
        # if there is data in device_without_tag
        if device_without_tag.columns.size:
            device_without_tag.set_axis(index, axis='columns', inplace=True)

        # device_tag may has many tags, so add tags at end of index
        # if there is data in device_with_tag
        if device_with_tag.columns.size:
            for i in range(2, device_with_tag.columns.size):
                # add column as tag_1, tag_2 ....
                index.append('Tag_' + str(i-1))
            device_with_tag.set_axis(index, axis='columns', inplace=True)

        # output to .csv
        device_with_tag.to_csv(
            setting['output_path_device_with_tag'], sep=';', index=False)
        device_without_tag.to_csv(
            setting['output_path_device_without_tag'], sep=';', index=False)

    if searching_new_keyword:
        # searching new tag in device_without_tag
        vendor_class_new_keywords, host_name_new_keywords = search_new_keyword(
            device_without_tag, device_DataFrame, setting)

        # saving new tags to file
        output_vendor_class_new_keywords = pandas.DataFrame.from_dict(
            vendor_class_new_keywords, orient='index')
        output_host_name_new_keywords = pandas.DataFrame.from_dict(
            host_name_new_keywords, orient='index')

        output_vendor_class_new_keywords.to_csv(
            setting['output_path_new_keyword_vendor_class'], sep=';')
        output_host_name_new_keywords.to_csv(
            setting['output_path_new_keyword_host_name'], sep=';')
