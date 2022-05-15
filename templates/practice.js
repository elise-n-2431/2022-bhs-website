let slides = 7
let dots = document.getElementsByClassName("dot");
if (n>slides.length) {id=1}
if (n<1) {id=slides.length}
let i;
let p;
for (i=0; i<id; i++){
    slides[i].style.display='none';
    dots[i].className = dots[i].className.replace(" active", "");}
for (p=slides.length; p>i; p--){
    slides[p].style.display='none';}
slides[id-1].style.display = "block";
slides[id-1].className += " active";
