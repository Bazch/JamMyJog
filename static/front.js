window.onload=function(){
    document.getElementById("bpmSlider").addEventListener("input", function(){
    var sliderValue = document.getElementById("bpmSlider").value;
    document.getElementById("bpmSliderText").innerHTML = sliderValue;
    });
}

function updateSlider(element) {
    var sliderValue = document.getElementById("bpmSlider").value;
    console.log(sliderValue);
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/slider?value=" + sliderValue, true);
    xhr.send(sliderValue);
}

