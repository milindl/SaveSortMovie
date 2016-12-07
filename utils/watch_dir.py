'''
watch_dir.py
method watch_directory(directory_path)
methid update_mongo(filename, actors)
test methods
'''

import os, glob
from pymongo import MongoClient
import identify
import createperson
import videoutil as vu
import sys, select
import time
import logging
from watchdog.observers import Observer
import watchdog.events

def watch_directory(path):
    '''
    watch_directory(dir_path)
    path: path to directory
    Watches the specified directory for addition of file
    Detects actors in the file, and adds to mongo
    '''
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    event_handler = CreationEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

    
def update_mongo(filename, actors):
    '''
    update_mongo(filename, actors)
    filename: string
    actors [] of strings
    '''
    client = MongoClient('mongodb://localhost/')
    db = client.savesortmovie
    db.videos.update_one(
        {'filepath':filename},
        {
          '$set': {
              'actors': actors
          }  
        }
    )


def basic_namegen(i):
    return str(time.time()) + 'imgbasic%03d'%i

    
class CreationEventHandler(watchdog.events.FileSystemEventHandler):
    def on_created(self, e):
        # Set up filename
        print('Detected creation of: ')
        print(str(e.src_path))
        src_p = e.src_path
        print(e.src_path[:-len(e.src_path.split('/')[-1])])
        # Identification
        face_frames = []
        print("Starting basic OpenCV processing")
        for frame in vu.video_pipe(src_p, {'outoften':0.05}):
            isfaces = vu.face_presence(frame)
            if isfaces:
                face_frames.append(frame)
        filepaths = vu.save_frames(face_frames, basic_namegen)
        print("Saved OpenCV processed frames")
        print("Starting Face Detect - Face Identify cycle")
        p_f = identify.frameset_identify_person(filepaths, 'actors')
        actors = [createperson.person_details(key, 'actors')['name']
                  for key in p_f.keys()]
        # Updating Mongo
        print("Updating mongo")
        update_mongo(e.src_path.split('/')[-1], actors)

        # Clean up
        img_files = glob.glob('*.jpg')
        print('Removing these files:\n ' + '\n'.join(img_files))
        print('You have 10 seconds to abort this deletion. Press q RET to abort deletion')
        i, __l, __m = select.select( [sys.stdin], [], [], 10)
        if i:
            print('Done, not deleting')
            return
        
        for img_file in img_files:
            os.remove(img_file)
        print('Done, with cleanup')

if __name__ == '__main__':
    watch_directory(sys.argv[1])
