/*
* The REST API for SaveSortMovie
*/

// Fetch dependencies
var express = require("express");
var md5 = require("blueimp-md5");
var getDuration = require("get-video-duration");
var serveStatic = require("serve-static");
var fileUpload = require('express-fileupload');
var multer = require("multer");

// Set up Multer
var storage = multer.diskStorage({
    destination: function (req, file, cb) {
	cb(null, __dirname + '/video_store');
    },
    filename: function (req, file, cb) {
	
	cb(null, Date.now() + "-" + file.originalname);
    }
});
var upload = multer({storage:storage });

// Set up application and model
var app; 
var videoModel; 

var init = function init(v) {
    app = express();
    
    videoModel = v;
    // Set up static file serving
    app.use(serveStatic(__dirname + '/client'));
    app.use(serveStatic(__dirname + '/video_store'));
}

// Mainloop
var watch = function watch() {
    app.get("/get_video", upload.array(), function getVideo(req, res) {
	// Get video from ID
	var rId = req.query.id;
	videoModel.find({id: rId},
	    function getVideoCallback(err, videos) {
		if (err) {
		    console.log(err)
		    res.sendStatus(503);
		}
		if (videos.length == 0) res.sendStatus(404);
		else res.send(videos[0]);
		console.log(videos[0]);
	    });
    });
    
    app.post("/upload_video",
	     upload.single("vid"),
	     function addVideo(req, res) {
		 // Save video to database
		 var videoData = req.body;
		 videoData.id = md5(req.file.filename);
		 videoData.actors = [];
		 videoData.tags = videoData.tags.split(" ");
		 videoData.filepath = req.file.filename;
		 getDuration(__dirname + "/video_store/" + videoData.filepath).then(function (duration){
		     videoData["length"] = duration;
		     videoModel
			 .create(videoData,
				 function addVideoCallback(err,addedVideo) {
				     if(err) {
					 console.log(err);
					 res.sendStatus(503);
				     }
				     console.log(addedVideo);
				     res.sendStatus(200);
				 }
				);
		 });
	     });

    app.get("/search_videos",
	    upload.array(),
	    function searchVideo(req, res) {
		videoModel.find({},
				function svCallback(err,vids) {
				    res.status(200);
				    for(var i = 0; i != vids.length; i++) {
					var id = vids[i].id;
					var title = vids[i].title;
					var actors = vids[i].actors;
					var length = vids[i].length;
					vids[i] = {};
					vids[i] = {
					    id: id,
					    title: title,
					    actors: actors,
					    length: length
					};
				    }
				    console.log(vids);
				    res.end(JSON.stringify(vids));
				}
			       );
	    });

    app.get("/", upload.array(), function(req, res) {
	res.sendFile('client/view.html', {root: __dirname });
    });
    // Start listening
    app.listen(6700);
}


module.exports = {init: init, watch: watch};
