# SaveSortMovie #
Note: I wrote the client in a slapdash way to learn Angular. I need to implement it in Angular2 when I get the time.
The Python backend should basically be OK.

An ongoing project providing a web-client and a server for viewing and uploading videos, and a python back-end that automatically categorizes those videos based on the actor(s).


I've used the following:

	
1. python
2. OpenCV for video processing
3. Microsoft Vision API
4. Cloudinary/Imgur(for storing images)
5. MongoDB (Database)
6. NodeJS + express for the server
7. Angular on the frontend


It's meant to be configured by someone on your intranet/LAN, and then you can run it in peace, using only the client. The instructions below detail the procedure for the "someone" who's installing it on your intranet/LAN.

## Instructions ##

###  Running the Server ###
Dependencies - 


1. Nodejs
2. npm
3. blueimp-md5
4. express
5. multer
6. get-video-duration
7. serve-static
8. body-parser [I may not use as of now, but it's a part of package.json]
9. mongoose
10. express-fileupload

There must be a folder video_store in the root of this repository before running.

To run the server, simply type 

```npm start```

after locating the correct directory(the root of this repository).

### Client Setup ###

Dependencies - 

1. angular.js inside client/js
2. angular-route.js inside client/js
3. a modern browser, like firefox or chrome. [untested on edge]

Simply navigate to [http://localhost:6700](http://locahost:6700/) after starting the nodejs server, mongodb, and the python watcher.

### MongoDB ###

Dependencies - 

1. MongoDB. Look at their site for installation instructions
2. You need to have a database called savesortmovie

Make sure to start mongo before starting the client.

### Python ###

1. python2 [Yes, I know it's old, but I needed some OpenCV stuff that I couldn't find in 3. Consequently, all stuff below needs to be for python2]
2. requests
3. cv2
4. numpy
5. watchdog
6. pymongo
7. cloudinary
7. imgurpython [only if for some reason you decide to switch to imgur over cloudinary]

You need to have 2 files in the util folder: 

1. CLOUDINARYDATA, which will be like:

   ```
   APIKEY:...
   APISECRET:...
   CLOUDNAME:...
   ```
2. KEY, which stores the Microsoft Vision API keys: 
   
   ```
   [key only, nothing else here]
   ```

Optionally, if you use imgur, you can replace CLOUDINARYDATA with CLIENT_DATA, and retain only the first two fields (CLIENTID: and CLIENTSECRET).

You also need to grab your `haarcascade_frontalface_default.xml` from wherever your cv2 installation is, and put it in here.

You need to train your copy of the program manually for the actors you wish to recognize. To do so, `cd` to the utils directory, and try the following: 


```
chmod +x createperson.py
./createperson.py
```

After all this is done, `cd` to the utils directory, and run

```
python2 watch_dir.py ../video_store
```
	
Now sit back, relax, as the script watches for any changes in the directory and updates mongo with the names of actors in added videos.
	


