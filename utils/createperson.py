#!/usr/bin/env python2
'''
createperson.py
This is a CLI interface to create a person
method create_pgroup
method create_person
method delete_person
method list_persons
method person_details
method add_faces
method is_train
method train
variable KEY
'''
import json
import requests
__KEYFILE = open('KEY')
KEY = ''
for line in __KEYFILE:
    KEY = line
    break
__KEYFILE.close()

def create_pgroup(name, userdata=''):
    '''
    create_pgroup(name, userdata='') : Microsoft response
    name : name of new group
    userdata = optional associated data
    '''
    url = 'https://api.projectoxford.ai/face/v1.0/persongroups/' + name
    headers = {
        'Ocp-Apim-Subscription-Key' : KEY,
        'Content-Type': 'application/json',
    }
    payload = {'name': name, 'userData': userdata}
    res = requests.put(url, headers=headers, data=json.dumps(payload))
    return res

def create_person(name, gname, user_data=None):
    '''
    create_person(name, gname, user_data=None) : personId
    name : person name
    gname : group name (previously created group must be used)
    user_data : optional user data
    '''
    url = 'https://api.projectoxford.ai/face/v1.0/persongroups/' + gname + '/persons'
    headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': KEY,
    }
    payload = {
        'name':name,
        }
    if user_data != None:
        payload['userData'] = user_data
    res = requests.post(url, headers=headers, data=json.dumps(payload))
    if res.status_code == 200:
        person_id = res.json()['personId']
        with open(gname + '.group', 'a+') as gfile:
            gfile.write(person_id)
            gfile.write("\n")
        return person_id
    else:
        print(res.json())
        raise ValueError('Bad argument')
    return ''

def delete_person(person_id, gname):
    '''
    delete_person(person_id, gname) : boolean
    person_id : personId of the person to be removed
    gname: group name
    '''
    headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': KEY,
    }
    url = 'https://api.projectoxford.ai/face/v1.0/persongroups/' + gname + '/persons/' + person_id
    res = requests.delete(url, headers=headers)
    if res.status_code == 200:
        lines = []
        with open(gname+'.group', 'r') as gfile:
            lines = gfile.readlines()
        if person_id+'\n' in lines:
            lines.remove(person_id + '\n')
            with open(gname+'.group', 'w') as gfile:
                for line in lines:
                    gfile.write(line)
    else:
        print(res.json())
        raise ValueError('Bad argument')
    return True

def list_persons(gname):
    '''
    list_persons() : []
    gname : group name
    NOTE: fetches data from local file.
    Any changes to group via other applications will not reflect here.
    '''
    with open(gname+'.group') as gfile:
        return [
            line[:-1] for line in gfile.readlines()
            ]
    
def person_details(person_id, gname):
    '''
    person_details(person_id, gname) : JSON
    person_id : personId
    gname : group name
    '''
    url = 'https://api.projectoxford.ai/face/v1.0/persongroups/' + gname + '/persons/' + person_id
    headers = {
        'Ocp-Apim-Subscription-Key' : KEY,
        'Content-Type': 'application/json',
    }
    res = requests.get(url, headers=headers)
    return res.json()
    
def add_faces(person_id, gname, img_list):
    '''
    add_faces(person_id, gname, img_list) : boolean
    person_id : personId
    gname : group name
    img_list : [ image urls ]
    Adds images to a person, however, still requires training to use
    '''
    headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': KEY,
    }
    url = 'https://api.projectoxford.ai/face/v1.0/persongroups/' + gname + '/persons/' + person_id + '/persistedFaces'
    for img in img_list:
        data = {
            'url': img
            }
        res = requests.post(url, data = json.dumps(data), headers = headers)
        if res.status_code == 200:
            print(img + ' added sucessfully' + '\n')
        else:
            print(res.json())
            raise ValueError('Bad argument')
    return True

def train(gname):
    '''
    train(gname) : None
    gname : group name
    Trains a group. Needs to be called after adding faces
    '''
    url = 'https://api.projectoxford.ai/face/v1.0/persongroups/' + gname + '/train'
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': KEY,
    }
    res = requests.post(url, headers=headers)
    if res.status_code == 202:
        return
    else:
        print(res.json())
        raise ValueError('Bad argument')

def is_train(gname):
    '''
    is_train(gname) : boolean
    gname : group name
    Method to see if a group is still training or has been trained after train()
    '''
    url = 'https://api.projectoxford.ai/face/v1.0/persongroups/' + gname + '/training'
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': KEY,
    }
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        json_data = res.json()
        print('Status: ' + json_data['status'] + '\n')
        if json_data['status'] == 'succeeded':
            return True
        else:
            return False
    else:
        print(res.json())
        raise ValueError('Bad argument')

def main():
    '''
    main()
    Testing method
    '''
    import sys
    usage = '''
    Usage:
    ./createperson.py createperson NAME GROUPNAME [USERDATA]
    ./createperson.py addfaces PERSONID GROUPNAME img1 [img2 [img3...
    ./createperson.py train GROUPNAME 
    ./createperson.py istrain GROUPNAME
    ./createperson.py deleteperson PERSONID GROUPNAME
    ./createperson.py listpersons GROUPNAME
    ./creatperson.py persondetails PERSONID GROUPNAME
    '''
    if len(sys.argv) <= 2:
        print(usage)
        return

    if sys.argv[1] == 'createperson':
        if len(sys.argv) == 4:
            cp = create_person(
                sys.argv[2],
                sys.argv[3]
            )
            print(cp)
        elif len(sys.argv) == 5:
            cp = create_person(
                sys.argv[2],
                sys.argv[3],
                sys.argv[4]
            )
            print(cp)
        else:
            print(usage)

    elif sys.argv[1] == 'persondetails':
        if len(sys.argv) == 4:
            cp = person_details(sys.argv[2], sys.argv[3])
            print(cp)
        else:
            print(usage)
            
    elif sys.argv[1] == 'deleteperson':
        if len(sys.argv) == 4:
            cp = delete_person(sys.argv[2], sys.argv[3])
            print cp
        else:
            print(usage)
    elif sys.argv[1] == 'listpersons':
        if len(sys.argv) == 3:
            cp = list_persons(sys.argv[2])
            print('\n'.join(cp))
        else:
            print(usage)
        
    elif sys.argv[1] == 'addfaces':
        if len(sys.argv) >= 5:
            cp = add_faces(
                sys.argv[2],
                sys.argv[3],
                sys.argv[4:]
            )
            print(cp)
        else:
            print(usage)
            
    elif sys.argv[1] == 'train':
        cp = train(sys.argv[2])
        print(cp)
        
    elif sys.argv[1] == 'istrain':
        cp = is_train(sys.argv[2])
        print(cp)
        
if __name__ == '__main__':
    main()
