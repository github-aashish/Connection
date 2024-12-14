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

function checkUser(e){
    //console.log(e.value)
    uname = e.value;
    console.log(uname.length)
    if(uname.length<3){
        e.style.backgroundColor = 'rgba(255,0,0,0.5)';
    }
    else{
    //console.log(typeof uname)
    fetch('/userNameCheck/'+uname, {
        method: 'GET'
    })
    .then((res) => {
        //console.log(res)
        if (res.status === 200){
            e.style.backgroundColor = 'rgba(255,0,0,0.5)';
        }
        else{
            e.style.backgroundColor = 'rgba(0,255,0,0.5)';
        }
    });
}
}

function checkPassword(e){
    password = e.value;
    btn = document.getElementById('sbmtbtn');
    const hasNumber = /\d/; // Checks for at least one digit
    const hasCharacter = /[a-zA-Z]/; // Checks for at least one letter (uppercase or lowercase)
    if (password.length<6){
        e.style.backgroundColor = 'rgba(255,0,0,0.5)';
    }
    else if(hasNumber.test(password) && hasCharacter.test(password)){
        e.style.backgroundColor = 'rgba(0,255,0,0.5)';
        btn.disabled = false;
    }
    else{
        e.style.backgroundColor = 'rgba(255,0,0,0.5)';
    }
}