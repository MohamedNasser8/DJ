switchBtn = document.getElementById("switch");
playBtn = document.getElementById("play");
stopBtn = document.getElementById("stop");
volumeBtn = document.getElementById("volume");
var wavesurfer = WaveSurfer.create({
  container: "#waveform",
  waveColor: "#e3bbee",
  progressColor: "#fe38ab",
  barHeight: 4,
  reponsive: true,
  hideScrollbar: true,
  plugins: [
    WaveSurfer.spectrogram.create({
      wavesurfer: wavesurfer,
      container: "#waveform",
      labels: true,
      height: 206,
    }),
  ],
});
var wavesurfer1 = WaveSurfer.create({
  container: "#waveform1",
  waveColor: "#e3bbee",
  progressColor: "#fe38ab",
  barHeight: 4,
  reponsive: true,
  hideScrollbar: true,
  plugins: [
    WaveSurfer.spectrogram.create({
      wavesurfer: wavesurfer,
      container: "#waveform1",
      labels: true,
      height: 206,
    }),
  ],
});

let path = document.getElementById("flask1").getAttribute("path");
let path1 = document.getElementById("flask1").getAttribute("path-mode");
wavesurfer1.load(path1);
wavesurfer.load(path);

switchBtn.onclick = function () {
  if (switchBtn.textContent == "Original Audio") {
    switchBtn.textContent = "Processed Audio";
    if (!wavesurfer.getMute()) wavesurfer.toggleMute();
    if (wavesurfer1.getMute()) wavesurfer1.toggleMute();
  } else {
    switchBtn.textContent = "Original Audio";
    if (!wavesurfer1.getMute()) wavesurfer1.toggleMute();
    if (wavesurfer.getMute()) wavesurfer.toggleMute();
  }
  volumeBtn.src = "static/images/volume.png";
};

playBtn.onclick = function () {
  if (switchBtn.innerHTML == "Original Audio") {
    if (!wavesurfer1.getMute()) wavesurfer1.toggleMute();
  } else {
    if (!wavesurfer.getMute()) wavesurfer.toggleMute();
  }
  wavesurfer1.playPause();
  wavesurfer.playPause();

  if (playBtn.src.match("play")) playBtn.src = "static/images/pause.png";
  else playBtn.src = "static/images/play.png";
};
stopBtn.onclick = function () {
  wavesurfer.stop();
  wavesurfer1.stop();

  playBtn.src = "static/images/play.png";
};

volumeBtn.onclick = function () {
  if (switchBtn.innerHTML == "Original Audio") {
    wavesurfer.toggleMute();
  } else {
    wavesurfer1.toggleMute();
  }
  if (volumeBtn.src.match("volume")) volumeBtn.src = "static/images/mute.png";
  else volumeBtn.src = "static/images/volume.png";
};
var slider = document.querySelector("#slider");

slider.oninput = function () {
  var zoomLevel = Number(slider.value);
  wavesurfer.zoom(zoomLevel);
  wavesurfer1.zoom(zoomLevel);
};

const data_from_flask = document.getElementById("flask1")
var dict_data = JSON.parse(document.getElementById("flask1").getAttribute("data"));


let n = data_from_flask.getAttribute("n_of_sliders");
if (n == ""){
  n = 4;
}

else{
  if(n == 10){
    document.getElementById("option1").checked = false
    document.getElementById("option2").checked = true
    document.getElementById("option3").checked = false


  }
  if (n == 3){
    document.getElementById("option1").checked = false
    document.getElementById("option2").checked = false
    document.getElementById("option3").checked = true
  }
}


changeContent();
function changeContent() {
  // wavesurfer.empty();
  // wavesurfer1.empty();

  // n = 4;

  if (document.getElementById("option1").checked) {
    n = 4;
    list = ["Piano", "Guitar", "Drums", "violin"];
  } else if (document.getElementById("option2").checked) {
    n = 10;
    list = ["A", "Y", "V", "Th", "Ch", "S", "O", "R", "N", "D"];
  } else if (document.getElementById("option3").checked) {
    n = 3;
    list = ["Trachycardia", "Flutterid", "Fibrillation"];
  }
  

  let str = `<div class="d-flex flex-wrap all-sliders">`;
  if (Object.keys(dict_data).length==0 || Object.keys(dict_data).length != n){
  for (let i = 0; i < n; i++) {
    str += `<div class="container1">
          <div class="number" id="number${i}">1</div>
          <input type="range" min="-10" max="10" value=1 class="slider" id="slider${i}" name="slider${i}">
          <div style = "transform: rotate(90deg);">${list[i]}</div>
      </div>`;
  }
}
else{
  for (let i = 0; i < n; i++) {

    str += `<div class="container1">
          <div class="number" id="number${i}">${dict_data[`slider${i}`]}</div>
          <input type="range" min="-10" max="10" value=${dict_data[`slider${i}`]} class="slider" id="slider${i}" name="slider${i}">
          <div style = "transform: rotate(90deg);">${list[i]}</div>
      </div>`;
  }

}

  str += `</div>
  <div class="upload"><div class="custom-file">
  <input type="file" class="custom-file-input" name = "file" id="inputGroupFile01" onchange="uploadfile()"">
  </div>
  <input type="range" min="-10" max="10" value=${n} name="num_sliders" style="display:none">

    <input class="btn btn-primary" type="submit" value="Submit"></div>
    `;
  document.getElementsByClassName("form")[0].innerHTML = str;
  const sliders = document.getElementsByClassName("slider");
  const number = document.getElementsByClassName("number");
  for (let i = 0; i < number.length; i++) {
    sliders[i].oninput = function () {
      number[i].innerHTML = sliders[i].value;
    };
  }
}

document.getElementById("option1").addEventListener("click", changeContent);
document.getElementById("option2").addEventListener("click", changeContent);
document.getElementById("option3").addEventListener("click", changeContent);

/*scroll buttons */

// let values = JSON.parse();

// n = Object.keys(values).length;

// document.getElementsByClassName("upload").innerHTML = str1;

function uploadfile() {
  let inp = document.getElementById("inputGroupFile01");
  console.log(inp.files[0]);
  let fr = new FileReader();
  fr.onload = function () {
    // document.getElementById("audio-play").src =  fr.result
    wavesurfer.load(fr.result);
  };
  fr.readAsDataURL(inp.files[0]);
}
