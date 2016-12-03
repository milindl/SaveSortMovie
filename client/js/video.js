/*
JavaScript file for the angularjs end of my video view
*/

var app = angular.module('videoApp', []);


app.controller('ViewVideo', function () {
    this.video = vid;
    this.relatedVideos = relatedVids;
})



/* Random data for testing purposes */

var vid = {
    "path" : "videoplayback.mp4",
    "title" : "Title of the Video Which is Descriptive",
    "tags": [
	"tag1",
	"tag2",
	"tag3"
    ],
    "length": 678,
    "actors":[
	"actor1",
	"actor2"
	]
}
var relatedVids = [
    {
	"title": "A RL 1",
	"length" : 567
    },
    {
	"title": "A RL 2",
	"length" : 678
    },
    {
	"title":"A RL 4",
	"length" : 456
    }
];
