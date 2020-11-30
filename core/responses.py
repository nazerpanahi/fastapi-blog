def general_response(data, message, code=200, data_key='data', message_key='message', code_key='code'):
    resp = dict()
    if data is not None and data_key is not None:
        resp.update({data_key: data})
    if message is not None and message_key is not None:
        resp.update({message_key: message})
    if code is not None and code_key is not None:
        resp.update({code_key: code})
    return resp


def ok_response(data=None, message='OK', code=200, data_key='data', message_key='message', code_key='code'):
    return general_response(data=data,
                            message=message,
                            code=code,
                            data_key=data_key,
                            message_key=message_key,
                            code_key=code_key)


def nok_response(data=None, message='NOK', code=200, data_key='data', message_key='message', code_key='code'):
    return general_response(data=data,
                            message=message,
                            code=code,
                            data_key=data_key,
                            message_key=message_key,
                            code_key=code_key)
