import numpy as np
#np.save('record.npy',dir)
#record = np.load('record.npy',allow_pickle=True).item()
#print(record)
#print(type(record))
def recording(key,value):
    dict0 = {"author": "Robbitzhao"}
    dict1 = zip(key,value)
    dict0.update(dict1)
    return dict0

def saving(dict_,file):
    try:
        np.save(file,dict_)
        return 'success'
    except:
        return 'fail'

def loading(file):
    try:
        record = np.load(file, allow_pickle=True).item()
        return record
    except:
        return 0

def changing(file,key,value):
    try:
        record = np.load(file, allow_pickle=True).item()
        if len(key) == len(value):
            for i in range(len(key)):
                record[key[i]] = value[i]
        else: return 0
        np.save(file,record)
        return record
    except:
        return 0

def delete(file,key):
    try:
        record = np.load(file, allow_pickle=True).item()
        for i in range(len(key)):
            record.pop(key[i])
        else: return 0
        np.save(file,record)
        return record
    except:
        return 0