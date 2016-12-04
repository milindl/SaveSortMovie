/*
* This is the main application. Here, I will deal with
* the mongoose model, the REST api that angular will use
*/

var mongoose = require("mongoose");
var REST = require("./REST.js");


// Set up mongoose
mongoose.connect("mongodb://localhost/savesortmovie");
var db = mongoose.connection;
var videoSchema = mongoose.Schema({
    filepath: String,
    title: String,
    id: String,
    length: Number,
    actors: [String],
    tags: [String]
});

var Video = mongoose.model("Video", videoSchema);
console.log(REST);
REST.init(Video);


db.on("error", console.error.bind(console, "Connection Error: "));

db.once("open", REST.watch);


