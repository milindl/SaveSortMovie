#!/usr/bin/env python2
'''
This is a CLI interface to create a person
This also deals with the initial task of person group creation
createperson create NAME
'''
import json
import requests
KEYFILE = open('KEY')
KEY = ''
for line in KEYFILE:
    KEY = line
    break
KEYFILE.close()

def create_pgroup(name, userdata=''):
    '''
    Method to create person group
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
    Method to create a new person
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
    Method to delete a person from a group
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
    return 'Removed successfully'

def list_persons(gname):
    '''
    Method to list all people in a group. 
    Fetches data locally, does NOT sync.
    '''
    with open(gname+'.group') as gfile:
        return [
            line[:-1] for line in gfile.readlines()
            ]
    
def person_details(person_id, gname):
    '''
    Method to return person details as JSON
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
    Method to add a set of faces to a person
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
    return 'Completed successfully. Consider training'

def train(gname):
    '''
    Method to train a group
    '''
    url = 'https://api.projectoxford.ai/face/v1.0/persongroups/' + gname + '/train'
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': KEY,
    }
    res = requests.post(url, headers=headers)
    if res.status_code == 202:
        return ''
    else:
        print(res.json())
        raise ValueError('Bad argument')

def is_train(gname):
    '''
    Method to see if a network has finished training
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
    Main function (entry point)
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
