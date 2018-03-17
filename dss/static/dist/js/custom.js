const slots =2;
const itemsInRow = 8;
for (var i = 1; i <= slots; i++) {
 var breakAt = Math.floor(Math.sqrt(slots));
 var element = `<div class="slot" id=slot${i} ondrop="drop(event)" ondragover="allowDrop(event)"></div>`;
 $("#inventory").append(element);
 if (i % itemsInRow == 0) {
   var divider = '<div style="clear: both;"></div>';
   $("#inventory").append(divider);
 }
}

var item = `<img src="https://www.google.co.in/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&cad=rja&uact=8&ved=0ahUKEwi1oN-QtMfWAhUMqo8KHeyJDRMQjRwIBw&url=http%3A%2F%2Fwww.gamemaps.com%2Fdetails%2F16987&psig=AFQjCNF2e70dLPANxvOJWm9O_saQLD2faQ&ust=1506671833842793" draggable="true" ondragstart="drag(event)" id=item1 class="tooltip" title="A simple sword">`
$('#slot1').append(item);

function allowDrop(ev) {
 ev.preventDefault();
}

function drag(ev) {
 ev.dataTransfer.setData("text", ev.target.id);
}

function drop(ev) {
 ev.preventDefault();
 var data = ev.dataTransfer.getData("text");
 ev.target.appendChild(document.getElementById(data));
}

$('.tooltip').tooltipster();