import os
import json

def get_dir_info(path):
    dir_dict = {}
    for root, dirs, files in os.walk(path):
        if not dirs:
            # 如果当前目录没有子目录，则说明当前目录为末端目录
            # 将当前目录作为key加入字典中，并用空列表做value
            dir_dict[root] = []
        # else:
            # # 如果当前目录有子目录，则将每个子目录作为key加入字典中，并用空列表做value
            # for d in dirs:
            #     dir_dict[os.path.join(root, d)] = []
        
        # 将当前目录下所有文件数量累加到末端目录的列表中
        if root in dir_dict:
            dir_dict[root].append(len(files))
    return dir_dict

if __name__ == '__main__':
    path = './droneVideos'
    dir_dict = get_dir_info(path)
    print(dir_dict)
    # 构建json数据格式
    json_data = {}
    for k, v in dir_dict.items():
        parent_dir = os.path.basename(os.path.dirname(k))
        child_dir = os.path.basename(k)
        if parent_dir not in json_data:
            json_data[parent_dir] = {}
        json_data[parent_dir][child_dir] = sum(v) - 1

    # 将数据写入json文件
    with open('dir_info.json', 'w') as f:
        json.dump(json_data, f, indent=4)

