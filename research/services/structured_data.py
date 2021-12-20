class Output():
    def __init__(self):
        pass

    def response_api(self, code, data):
        codes_messages = {
            200: "Success!",
            400: "Bad request.",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Data don't founded!",
            500: "Internal server error!",
            502: "Bad Gateway"
        }
        if code in codes_messages.keys():
            msg = codes_messages[code]
        else:
            msg = 'Error!'
            code = 404
        if type(data) != list:
            data = [data]
        response = {'message': msg, 'results': data, 'status': code}, code

        return response

    def return_funtion(self, code, data):
        response = {'results': data, 'status': code}
        return response

    def standart_dash(self, list_input, value_int=False):
        count = 1
        list_of_dicts= []

        for item in list_input:
            dicts_result = {}
            dicts_result['label'] = item
            if value_int is True:
                dicts_result['value'] = count
            else:
                dicts_result['value'] = item
            count +=1
            list_of_dicts.append(dicts_result)
        return list_of_dicts

    def standart_from_series(self, series_data, names):
        list_of_dicts = []
        for index_serie in series_data.index:
            dicts_result = {}
            dicts_result[names[0]] = index_serie
            dicts_result[names[1]] = str(series_data[index_serie])
            list_of_dicts.append(dicts_result)
        return list_of_dicts

    def standart_from_dicts(self, dict_data, names):
        list_of_dicts = []
        for key_dict in dict_data.keys():
            dicts_result = {}
            dicts_result[names[0]] = key_dict
            dicts_result[names[1]] = str(dict_data[key_dict])
            list_of_dicts.append(dicts_result)
        return list_of_dicts


