'''
videoutil.py
method video_pipe
method face_presence
method save_frames
testing methods
'''
import cv2
import numpy as np

def video_pipe(path, parameters = None):
    '''
    video_pipe(path, parameters = {}) : yield numpy frames(cv2 imgs)
    path : filepath of video
    parameters : dictionary of parameters
    possible parameters : outoften
    Generator function for a video pipe
    '''
    if parameters == None:
        parameters = {'outoften' : 1}
    vc = cv2.VideoCapture(path)
    i = 0
    while True:
        i += 1
        ret, frame = vc.read()
        if ret == False:
            break
        if i%(10//parameters['outoften']) == 0:
            yield frame
    vc.release()

def face_presence(frame, parameters = None):
    '''
    face_presence(frame, parameters = None) : boolean is_face_present
    frame : np matrix containing image in which you want to detect faces
    parameters : {} containing optional parameters
    '''
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(frame_gray, 1.3, 5)
    return len(faces) > 0

def save_frames(frames, img_name_generator, img_format = 'jpg'):
    '''
    save_frames(frames, img_name_generator, img_format = 'jpg') : [ filenames ]
    frames : [ np matrix images to be stored ]
    img_name_generator : method(n) to generate the nth filename
    img_format : format of images to be saved
    '''
    i = 0
    filenames = []
    for frame in frames:
        filename = img_name_generator(i)
        cv2.imwrite(filename + '.' + img_format, frame)
        i += 1
        filenames.append(filename + '.' + img_format)
    return filenames

# Testing methods follow
def __basic_namegen(i):
    return 'imgbasic%03d'%i
if __name__ == '__main__':
    face_frames = []
    for frame in video_pipe('./videoplayback.mp4', {'outoften': 1}):
        isfaces = face_presence(frame)
        if isfaces :
            face_frames.append(frame)
    save_frames(face_frames, __basic_namegen)

