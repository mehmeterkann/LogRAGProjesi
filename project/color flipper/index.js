 const body = document.getElementsByTagName("body")[0]

 function setColor(color){
    body.style.backgroundColor=color;
 }

 function randomColor(){
    const red = Math.random();
    const redValue = red*255;
    
    const green = Math.random();
    const greenValue = green*255;

    const blue = Math.random();
    const blueValue = blue*255;

    const randomized = `rgb(${redValue},${greenValue},${blueValue})`;
    body.style.backgroundColor=randomized;
 }