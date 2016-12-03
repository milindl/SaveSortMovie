var express = require("express");
var bodyParser = require("body-parser");
var md5 = require("blueimp-md5");
var getDuration = require("get-video-duration");
var serveStatic = require("serve-static");
var app; 
var videoModel; 

var init = function init(v) {
    app = express();
    app.use(bodyParser.json());
    videoModel = v;
    // Set up static file serving
    app.use(serveStatic(__dirname + '/client'));
    app.use(serveStatic(__dirname + '/video_store'));
}

var watch = function watch() {
    app.get("/get_video", function getVideo(req, res) {
	var rId = req.query.id;
	videoModel.find({id: rId},
	    function getVideoCallback(err, videos) {
		if (err) {
		    console.log(err)
		    res.sendStatus(503);
		}
		if (videos.length == 0) res.sendStatus(404);
		else res.send(videos[0]);
	    });
    });
    app.put("/add_video", function addVideo(req, res) {
	var videoData = req.body;
	var rString = "" + (Math.random());
	videoData["id"] = md5(videoData.title + rString)
	getDuration(__dirname + "/video_store/" + videoData.filepath).then(function (duration){
	    videoData["length"] = duration;
	    videoModel.create(videoData,
		function addVideoCallback(err, addedVideo) {
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
    app.get("/", function(req, res) {
	res.sendFile(__dirname + "/client/view.html");
    });
    app.listen(6700);
}


module.exports = {init: init, watch: watch};
