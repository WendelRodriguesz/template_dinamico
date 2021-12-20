import json
import os


def get_data():
    try:
        USEREMAILS = list()
        # dir = os.getcwd()
        # exclu = len(dir)
        # dir = dir[:exclu]
        # filepath = '/database/useremails.json'
        # # caminho = dir + filepath
        caminho = './database/useremails.json'
        # print(caminho)

        with open(caminho) as file_json:
            config = json.load(file_json)

        c = 0
        for key in config:
            USEREMAILS.append(' ')
            USEREMAILS[c] = (config.get(key))
            c += 1

        return USEREMAILS

    except Exception as err:
        print('Error! ', err)
        return 404

