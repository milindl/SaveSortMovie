'''
identify.py
method identify_person
method frameset_identify_person
test methods
variable CLIENT_ID
variable CLIENT_SECRET
variable KEY
'''

from cloudinarypipeline import CloudinaryPipeline

import json
import requests

__KEYFILE = open('KEY')
KEY = __KEYFILE.readlines()[0]
__KEYFILE.close()
__CLOUDINARY_DATA = open('CLOUDINARY_DATA')
__lines = __CLOUDINARY_DATA.readlines()
API_KEY = __lines[0].split(':')[1][:-1]
API_SECRET = __lines[1].split(':')[1][:-1]
CLOUD_NAME = __lines[2].split(':')[1][:-1]

def identify_person(gname, img_path, path_type='path'):
    '''
    identify_person(gname, img_path, path_type) : [(personId,confidence)]
    gname : group in which to look for person
    img_path : url or filepath to image
    path_type = 'url' or 'path' depending on above
    '''
    # First prepare image
    i_pipe = CloudinaryPipeline(img_path,
                                {'cloud_name': CLOUD_NAME,
                                 'api_key': API_KEY,
                                 'api_secret': API_SECRET},
                                path_type)

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
    
    # If OpenCV detected a Face but Microsoft cannot
    if len(f_ids) == 0:
        return []

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

def frameset_identify_person(filepaths, gname):
    '''
    frameset_identify_person(filepaths, gname) : { personId:summation_of_score }
    filepaths : [ filepaths for images ]
    gname : group name
    '''
    persons_found = {}
    for filepath in filepaths:
        print("Processing " + filepath)
        faces_in_fp = identify_person(gname, filepath, path_type='path')
        for elem in faces_in_fp:
            person_id = elem[0]
            confidence = elem[1]
            if person_id not in persons_found:
                persons_found[person_id] = 0
            persons_found[person_id] += confidence
            print persons_found
    return persons_found

def __basic_namegen(i):
    return 'imgbasic%03d'%i


if __name__ == '__main__':
    # Testing
    import sys
    import videoutil as vu
    import createperson
    face_frames = []
    print("Starting basic OpenCV processing")
    for frame in vu.video_pipe(sys.argv[1], {'outoften':0.1}):
        isfaces = vu.face_presence(frame)
        if isfaces:
            face_frames.append(frame)
    filepaths = vu.save_frames(face_frames, __basic_namegen)
    print("Saved OpenCV processed frames")
    print("Starting Face Detect - Face Identify cycle")
    p_f = frameset_identify_person(filepaths, 'actors')
    print(p_f)
    for key in p_f.keys():
        print(createperson.person_details(key, 'actors'))
