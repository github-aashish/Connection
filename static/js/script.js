var crsr = document.querySelector("#cursor");
// var crsr_blur = document.querySelector("#cursor-blur");
document.addEventListener("mousemove",function(dets){
    //console.log(dets.y);
    //console.log(dets.y);
    crsr.style.left = dets.x+"px";
    crsr.style.top = dets.y+"px";
    // crsr_blur.style.left = dets.x - 240 + "px";
    // crsr_blur.style.top = dets.y - 240 + "px";
});

// const save = document.querySelector('.save');
// const currentcrsr = document.querySelector('#cursor');

// save.addEventListener('mouseover', function() {
//     // Set all changes only once to reduce repaint/reflow
//     crsr.style.cssText = `
//         height: 50px;
//         width: 50px;
//         background: url('../images/search.gif');
//         background-size: contain;
//         background-repeat: no-repeat;
//         background-position: center;
//     `;
// });

// save.addEventListener('mouseout', function() {
//     // Reset all styles in one go
//     crsr.style.cssText = `
//         height: 00px;
//         width: 0px;
//         background: none;
//     `;
// });