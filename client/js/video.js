var app = angular.module("videoApp", ["ngRoute"]);

// Services to deal with the XMLHttpRequests and the like

function ComService($http) {
    this.getVideo = function getVideo(rId) {
	var get_promise = $http({
	    url: "http://localhost:6700/get_video",
	    method: "GET",
	    params: {id: rId}
	});
	return get_promise
    };
    this.searchVideo = function searchVideo() {
	var search_promise = $http({
	    url: "http://localhost:6700/search_videos",
	    method: "GET"
	});
	return search_promise;
    };

}

function ViewCtrl(ComService,$routeParams) {
    this.videoData = {};
    this.routeParams = $routeParams;
    this.init = function init(rId, context) {
	ComService
	    .getVideo(rId)
	    .then(
		function successCallback(res) {
		    console.log("Promise resolved");
		    context.videoData = res.data;
		},
		function failureCallback(err) {
		    console.log("Promise rejected");
		    console.log(err);
		});
    };
}

function SearchCtrl(ComService) {
    this.videos = [];
    this.init = function(context) {
	ComService
	    .searchVideo()
	    .then(function successCallback(res) {
		console.log(res.data[0].title);
		context.videos = res.data;
	    }, function errorCallback(err) {
		console.log(err);
	    });
    };
}


app.service("ComService", ComService);
app.controller("ViewCtrl", ViewCtrl);
app.controller("SearchCtrl", SearchCtrl);


// Enable troubleshooting
app.config(function($logProvider, $locationProvider, $routeProvider){
    $logProvider.debugEnabled(true); //Set up logging for errors
    // Set up location for video viewing get requests


    $routeProvider
	.when("/", {
	    templateUrl: "search.html",
	    controller: "SearchCtrl",
	    controllerAs: "sc"
	})
	.when("/search", {
	    templateUrl: "search.html",
	    controller: "SearchCtrl",
	    controllerAs: "sc"
	})
	.when("/upload", {
	    templateUrl: "upload_box.html",
	   
	})
	.when("/view/:id", {
	    templateUrl: "viewbasic.html",
	    controller: ViewCtrl,
	    controllerAs: "vc"
	});
});
