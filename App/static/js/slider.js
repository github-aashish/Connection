const message = ()=>{
    console.log("Slider Function");
}

function makeSlides(element){
    alert("making slides")
    const slides = element.querySelectorAll('.slide');
    slides.forEach(
    (slide,index)=>{
        slide.style.left = `${index * 100}%`;
    }
);
}

const goNext = (e)=>{
    counter = parseInt(e.parentElement.getAttribute('data-current'));
    Slides = parseInt(e.parentElement.getAttribute('data-slidesNo'));
    if(counter<Slides.length-1){
        e.parentElement.setAttribute("data-current",`${counter+1}`);
        counter++;
        slideImage(e,counter);
    }
    else{
        e.parentElement.setAttribute("data-current",`0`);
        counter = 0;
        slideImage(e,counter);
    }
    
}
const goPrev = (e)=>{
    counter = parseInt(e.parentElement.getAttribute('data-current'));
    Slides = parseInt(e.parentElement.getAttribute('data-slidesNo'));
    if(counter > 0){
        e.parentElement.setAttribute('data-current') = counter - 1;
        counter--;
        slideImage(e,counter);
    }
    else{
        e.parentElement.setAttribute('data-current') = Slides - 1;
        counter = Slides - 1;
        slideImage(e,counter);
    }
    
}

const slideImage = (e,counter)=>{
    parentSlider = e.parentElement;
    slides = parentSlider.querySelectorAll('.slide');
    console.log(slides);
    slides.forEach((slide)=>{
        slide.style.transform = `translateX(-${counter*100}%)`;
    })
}
