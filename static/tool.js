var video = document.querySelector("#videoElement");

if (navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({
        video: true
            // after allowing the camera start the video stream
    }).then(function(stream) {
        video.srcObject = stream
            //play the video
        video.play();
    }).catch(function(error) {
        console.log(error);
    });
}

var image = document.getElementById('image'),
    context = image.getContext('2d'); //setting for resolution of image

var imagee = document.getElementById('sadge'),
    sadge = imagee.getContext('2d');

function disppic() {
    context.drawImage(video, video.width / 2 + 50, video.height / 2 + 50, 400, 400, 0, 0, 150, 150);
    picture = sadge.drawImage(video, image.width / 2, image.height / 2, 200, 200, 0, 0, 28, 28);
}

/********************************************************************************************************** */

var textbookb = document.getElementById("textbook");
var onlineb = document.getElementById("online");

var btext = false;
var bonline = false;

function togglet(){
    textbookb.style.backgroundColor = "#FCD1D1";
    onlineb.style.backgroundColor = "#AEE1E1";

    btext = true;
    bonline = false;
}

function toggleo(){
    textbookb.style.backgroundColor = "#AEE1E1";
    onlineb.style.backgroundColor = "#FCD1D1";

    btext = false;
    bonline = true;
}