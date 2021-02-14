var isText = [0, 0];
var count1 = 1;
var count2= 1;
var startStop = false;

function togglet(){
  count1++;
  if(count1%2 != 1){
    isText[0] = 1;
    alert("Text is enabled")
  } else {
    isText[0] = 0;
    alert("Text is disabled")
  }
  console.log(isText);
}

function toggleo(){
  count2++;
  if(count2%2 != 1){
    isText[1] = 1;
    alert("Online is enabled")
  } else {
    isText[1] = 0;
    alert("Online is disabled")
  }
  console.log(isText);

}

function  toggleOn(){
    startStop = !startStop;
    console.log(startStop);
}
