let searchForm = document.querySelector('.search-form');

document.querySelector('#search-btn').onclick = () =>{
    searchForm.classList.toggle('active');
    navbar.classList.remove('active');
}



let navbar = document.querySelector('.navbar');

document.querySelector('#menu-btn').onclick = () =>{
    navbar.classList.toggle('active');
    searchForm.classList.remove('active');
}

window.onscroll = () =>{
    searchForm.classList.remove('active');
    navbar.classList.remove('active');
}



const myslide = document.querySelectorAll('.myslider'),
        dot = document.querySelectorAll('.dot');

let counter = 1;
sliderfun(counter);

let timer = setInterval(autoslide, 8000);
function autoslide(){
    counter += 1;
    sliderfun(counter);
}

function plusSlides(n){
    counter += n;
    sliderfun(counter);
    resetTimer();
}

function currentSlide(n){
    counter += n;
    sliderfun(counter);
    resetTimer();
}

function resetTimer(){
    clearInterval(timer);
    timer = setInterval(autoslide, 8000);
}

function sliderfun(n){
    let i;
    for (i = 0;i<myslide.length; i++) {
        myslide[i].style.display = "none";
    }
    for (i = 0;i<dot.length; i++) {
        dot[i].classList.remove('active');
    }

    if (n > myslide.length) {
        counter = 1;
    }

    if (n < 1) {
        counter = myslide.length;
    }
    myslide[counter - 1].style.display = "block";
    dot[counter - 1].classList.add('active');
}

var swiper = new Swiper(".product-slider", {
    loop:true,
    spaceBetween: 20,
    autoplay: {
        delay: 7500,
        disableOnInteraction: false,
    },
    centeredSlides: true,
    breakpoints: {
      0: {
        slidesPerView: 1,
      },
      768: {
        slidesPerView: 2,
      },
      1020: {
        slidesPerView: 3,
      },
    },
});


'use strict';



/**
 * navbar toggle
 */

const overlay = document.querySelector("[data-overlay]");
const navOpenBtn = document.querySelector("[data-nav-open-btn]");
const navbar1 = document.querySelector("[data-navbar]");
const navCloseBtn = document.querySelector("[data-nav-close-btn]");

const navElems = [overlay, navOpenBtn, navCloseBtn];

for (let i = 0; i < navElems.length; i++) {
  navElems[i].addEventListener("click", function () {
    navbar1.classList.toggle("active");
    overlay.classList.toggle("active");
  });
}



/**
 * header & go top btn active on page scroll
 */

const header = document.querySelector("[data-header]");
const goTopBtn = document.querySelector("[data-go-top]");

window.addEventListener("scroll", function () {
  if (window.scrollY >= 80) {
    header.classList.add("active");
    goTopBtn.classList.add("active");
  } else {
    header.classList.remove("active");
    goTopBtn.classList.remove("active");
  }
});