'''
identify.py
method indentify_person
test methods
variable CLIENT_ID
variable CLIENT_SECRET
variable KEY
'''
from imgurpipeline import ImgurPipeline
from imgurpython import ImgurClient

import json
import requests
__KEYFILE = open('KEY')
KEY = __KEYFILE.readlines()[0]
__KEYFILE.close()
__CLIENT_DATA = open('CLIENT_DATA')
__lines = __CLIENT_DATA.readlines()
CLIENT_ID = __lines[0].split(':')[1][:-1]
CLIENT_SECRET = __lines[1].split(':')[1][:-1]

def identify_person(gname, img_path, path_type='path'):
    '''
    identify_person(gname, img_path, path_type) : [(personId,confidence)]
    gname : group in which to look for person
    img_path : url or filepath to image
    path_type = 'url' or 'path' depending on above
    '''
    # First prepare image
    i_client = ImgurClient(CLIENT_ID, CLIENT_SECRET)
    i_pipe = ImgurPipeline(img_path, i_client, path_type)

    # Prepare and send Face Detect request
    fd_url = 'https://api.projectoxford.ai/face/v1.0/detect?returnFaceId=true'
    fd_headers = {
        'Ocp-Apim-Subscription-Key' : KEY,
        'Content-Type': 'application/json',
    }
    fd_payload = {
        'url':i_pipe.get_link()
        }
    fd_res = requests.post(
        fd_url,
        headers=fd_headers,
        data=json.dumps(fd_payload)
        )
    if fd_res.status_code != 200:
        print('Failed to communicate with Face Detect API')
        print(fd_res.json())
        raise ValueError('Bad argument')
    fdetected = fd_res.json()
    f_ids = [face['faceId'] for face in fdetected]

    # Delete imgur image
    i_pipe.delete()

    # Send Face Identify Request
    fi_url = 'https://api.projectoxford.ai/face/v1.0/identify'
    fi_headers = {
        'Ocp-Apim-Subscription-Key' : KEY,
        'Content-Type': 'application/json',
    }
    fi_payload = {
        'personGroupId':gname,
        'faceIds':f_ids,
        'maxNumOfCandidatesReturned':1,
        'confidenceThreshold':0.5
        }
    fi_res = requests.post(
        fi_url,
        headers=fi_headers,
        data=json.dumps(fi_payload)
        )
    if fi_res.status_code != 200:
        print('Error while using Face - Identify API')
        print(fi_res.json())
        raise ValueError('Bad argument')
    data = fi_res.json()
    faces_found = [(
        item['candidates'][0]['personId'],
        item['candidates'][0]['confidence']
        ) for item in data if len(item['candidates']) == 1 ]
    return faces_found

if __name__ == '__main__':
    # Testing
    f = identify_person('actors', 'http://media.vanityfair.com/photos/55b51427fff2c16856a73070/master/w_790,c_limit/will-smith-jay-z-emmett-till-hbo.jpg', path_type='url')
    print(f)
