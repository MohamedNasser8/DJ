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
});
var wavesurfer1 = WaveSurfer.create({
  container: "#waveform1",
  waveColor: "#e3bbee",
  progressColor: "#fe38ab",
  barHeight: 4,
  reponsive: true,
  hideScrollbar: true,
});

let path = document.getElementById("flask_data").getAttribute("path");
let path1 = document.getElementById("flask_data").getAttribute("path-mode");
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

// let waves = document.getElementById('waveform').children
// console.log(waves)
// for(let i=0;i<waves.length;i++){
// }

/*scroll buttons */
let values = JSON.parse(
  document.getElementById("flask_data").getAttribute("data")
);
console.log(values);
let n = Object.keys(values).length;
let str = "";
for (let i = 0; i < n; i++) {
  str += `<div class="container">
        <div class="number" id="number${i}">${
    values[`slider${i}`]["value"]
  }</div>
        <input type="range" min="-10" max="10" value=${
          values[`slider${i}`]["value"]
        } class="slider" id="slider${i}" name="slider${i}">

        <div style = "transform: rotate(90deg);">${
          values[`slider${i}`]["name"]
        }</div>
    </div>`;
}

str += `
<div class="custom-file">
<input type="file" class="custom-file-input" name = "file" id="inputGroupFile01" onchange="uploadfile()"">
</div>

  <input class="btn btn-primary" type="submit" value="Submit">
  `;
document.getElementsByClassName("all-sliders")[0].innerHTML = str;

const sliders = document.getElementsByClassName("slider");
const number = document.getElementsByClassName("number");
for (let i = 0; i <= number.length; i++) {
  sliders[i].oninput = function () {
    number[i].innerHTML = sliders[i].value;
  };
}

function uploadfile() {
  let inp = document.getElementById("inputGroupFile01");
  console.log(inp.files[0]);
  let fr = new FileReader();
  fr.onload = function () {
    console.log(fr.result);
    // document.getElementById("audio-play").src =  fr.result
    wavesurfer.load(fr.result);
  };
  fr.readAsDataURL(inp.files[0]);
}
