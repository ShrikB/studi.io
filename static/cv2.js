let video = document.getElementById("videoInput"); // video is the id of video tag
var canvas = document.getElementById("canvasOutput");

owo = [];
everything = [];
point = 0;

navigator.mediaDevices.getUserMedia({ video: true, audio: false })
    .then(function(stream) {
        video.srcObject = stream;
        video.play();
    })
    .catch(function(err) {
        console.log("An error occurred! " + err);
    });

function draw_canv() {
    context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, video.width, video.height);
    console.log("Drawn");
}

function send(ben) {
    draw_canv();

    var jqXHR = $.ajax({
        type: "POST",
        url: "/predict",
        data: { file: canvas.toDataURL().split(",")[1]},
        async: false
    });

    var result = jqXHR.responseText

    let chuck;
    if (parseInt(result) == 0) {
        //console.log("phone");
        chuck = 0;
    } else if (parseInt(result) == 1) {
        //console.log("talk");
        if (isText[0] == 1 && isText[1] == 0) {
            chuck = 1;  
        } else if (isText[0] == 0 && isText[1] == 1){
            chuck = 0;
        } else {
            chuck = 1;
        }

    } else if (parseInt(result) == 2) {
        //console.log("talk");
        chuck = 0;
    } else if (parseInt(result) == 3) {
        //console.log("talk");
        if (isText[0] == 1 && isText[1] == 0) {
            chuck = 0;  
        } else if (isText[0] == 0 && isText[1] == 1){
            chuck = 1;
        } else {
            chuck = 1;
        }
    } else if (parseInt(result) == 4) {
        //console.log("talk");
        chuck = 0;                    
    } else if (parseInt(result) == 5) {
        //console.log("talk");
        chuck = 0;            
    }
    if(owo.length == 5){
        owo.shift();
    }

    owo.push(chuck);
    everything.push(chuck)
    console.log(owo);
    if(((owo[0] + owo[1] + owo[2] + owo[3] + owo[4])/5) < 0.6){
        document.getElementById('noise').play();
        owo=[];
    }  
    if(((owo[0] + owo[1] + owo[2] + owo[3] + owo[4])/5) >= 0.8){
        point++;
        console.log(point)
    }  
}

var light;

function change() {
    if (!light) {
        light = window.setInterval(send,550);
    } else {
         var jqXHR = $.ajax({
             type: "POST",
             url: "/points",
             data: {points: point},
             async: false
         });

        window.clearInterval(light);
        light = null;
    }
}