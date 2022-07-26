var myLabels = document.getElementsByTagName('label');
var j = 1
for (var i = 0; i < myLabels.length; i++) {
    console.log(myLabels[i])
    if (myLabels[i].innerHTML == 'Contenurep:') {
        myLabels[i].innerHTML = "Réponse " + j
        myLabels[i].style.fontWeight = "bold"
        myLabels[i].style.color = "black"
        j++
    }
}

for (var i = 0; i < myLabels.length; i++) {
    console.log(myLabels[i])
    if (myLabels[i].innerHTML == 'Valeur:') {
        myLabels[i].innerHTML = "Points"
    }
}