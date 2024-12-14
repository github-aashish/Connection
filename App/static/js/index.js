
//Like Post

function like_post(element) {
    let id = element.dataset.post_id;
    fetch('/n/post/'+parseInt(id)+'/like', {
        method: 'PUT'
    })
    .then(() => {
        let count = element.querySelector('.likes_count');
        let value = count.innerHTML;
        value++;
        count.innerHTML = value;
        element.querySelector('.svg-span').innerHTML = `
            <svg width="1.1em" height="1.1em" viewBox="0 -1 16 16" class="bi bi-heart-fill" fill="#e0245e" xmlns="http://www.w3.org/2000/svg">
                <path fill-rule="evenodd" d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314z"/>
            </svg>`;
        element.setAttribute('onclick','unlike_post(this)');
    })
}

// Unlike Post
function unlike_post(element) {
    let id = element.dataset.post_id;
    fetch('/n/post/'+parseInt(id)+'/unlike', {
        method: 'PUT'
    })
    .then(() => {
        let count = element.querySelector('.likes_count');
        let value = count.innerHTML;
        value--;
        count.innerHTML = value;
        element.querySelector('.svg-span').innerHTML = `
            <svg width="1.1em" height="1.1em" viewBox="0 -1 16 16" class="bi bi-heart" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                <path fill-rule="evenodd" d="M8 2.748l-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01L8 2.748zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143c.06.055.119.112.176.171a3.12 3.12 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15z"/>
            </svg>`;
        element.setAttribute('onclick','like_post(this)');
    })
}

function save_post(element) {
    let id = element.dataset.post_id;
    fetch('/n/post/'+parseInt(id)+'/save', {
        method: 'PUT'
    })
    .then(() => {
        element.querySelector('.saved-span').innerHTML = `
            <svg width="2em" height="2em" viewBox="0.5 0 15 15" class="bi bi-bookmark-fill" fill="#17bf63" xmlns="http://www.w3.org/2000/svg">
                        <path fill-rule="evenodd" d="M3 3a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v12l-5-3-5 3V3z"/>
                    </svg>
                    <p>Unsave</p>`;
        element.setAttribute('onclick','unsave_post(this)');
    });
}

function unsave_post(element) {
    let id = element.dataset.post_id;
    fetch('/n/post/'+parseInt(id)+'/unsave', {
        method: 'PUT'
    })
    .then(() => {
        element.querySelector('.saved-span').innerHTML = `
        <svg width="2em"  height="2em" viewBox="0.5 0 15 15" class="bi bi-bookmark" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                        <path fill-rule="evenodd" d="M8 12l5 3V3a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v12l5-3zm-4 1.234l4-2.4 4 2.4V3a1 1 0 0 0-1-1H5a1 1 0 0 0-1 1v10.234z"/>
                    </svg>
                    <p>Save</p>`;
        element.setAttribute('onclick','save_post(this)');
    });
}


//Comments Functionalities

function show_comment(element) {
    let post_div = element.parentElement.parentElement;
    let post_id = post_div.dataset.post_id;
    let comment_div = post_div.querySelector('.comment-div');
    let comment_div_data = comment_div.querySelector('.comment-div-data');
    let comment_comments = comment_div_data.querySelector('.comment-comments');
    if(comment_div.style.display === 'block') {
        //comment_div.querySelector('input').focus()
        comment_div.style.display = 'none';
        return;
    }
    comment_div.querySelector('#spinner').style.display = 'block';
    comment_div.style.display = 'block';
    fetch('/n/post/'+parseInt(post_id)+'/comments')
    .then(response => response.json())
    .then(comments => {
        comments.forEach(comment => {
            display_comment(comment,comment_comments);
        });
    })
    .then(() => {
        setTimeout(() => {
            comment_div.querySelector('.spinner-div').style.display = 'none';
            comment_div.querySelector('.comment-div-data').style.display = 'block';
            comment_div.style.overflow = 'auto';
        }, 1000);
    });
}

function write_comment(element) {
    let post_id = element.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.dataset.post_id;
    let comment_text = element.querySelector('.comment-input').value;
    let comment_comments = element.parentElement.parentElement.parentElement.parentElement.querySelector('.comment-comments');
    let comment_count = element.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.querySelector('#comment-count')
    if(comment_text.trim().length <= 0) {
        return false;
    }
    fetch('/n/post/'+parseInt(post_id)+'/write_comment',{
        method: 'POST',
        body: JSON.stringify({
            comment_text: comment_text
        })
    })
    .then(response => response.json())
    .then(comment => {
        console.log(comment);
        element.querySelector('input').value = '';
        comment_count.innerHTML++;
        display_comment(comment[0],comment_comments,true);
        return false;
    });
    return false;
}

function display_comment(comment, container, new_comment=false) {
    //let writer = document.querySelector('#user_is_authenticated').dataset.username;
    let eachrow = document.createElement('div');
    eachrow.className = 'eachrow';
    eachrow.setAttribute('data-id', comment.id);
    eachrow.innerHTML = `
        <div class="comment-profile-pic">
            <a href='/${comment.commenter.username}'>
                <img class="small-profilepic" src=${comment.commenter.profile_pic}>
            </a>
        </div>
        <div class="each-comment">
            <div class="comment-text-div">
                <div class="comment-user">
                    <a href="/${comment.commenter.username}">
                        ${comment.commenter.first_name} ${comment.commenter.last_name}
                    </a>
                </div>
                <div class="comment-body">
                ${comment.body}
                </div>
            </div>
        </div>`;
    if (new_comment) {
        eachrow.classList.add('godown');
        let comments = container.innerHTML;
        container.prepend(eachrow);
    }
    else {
        container.append(eachrow);
    }
}


//Comments Functionality Ends

//Follow And Unfollow

function follow_user(element, username, origin) {
    console.log("HAppening")
    fetch('/'+username+'/follow', {
        method: 'PUT'
    })
    .then(() => {
        element.setAttribute('onclick',onclick="unfollow_user(this,'${username}','suggestion')");
        element.innerHTML = `Connected`;
        // if(origin === 'suggestion') {
        //     element.parentElement.innerHTML = `<button class="btn btn-success" type="button" onclick="unfollow_user(this,'${username}','suggestion')">Following</button>`;
        // }
        // else if(origin === 'edit_page') {
        //     element.parentElement.innerHTML = `<button class="btn btn-success float-right" onclick="unfollow_user(this,'${username}','edit_page')" id="following-btn">Following</button>`;
        // }
        // else if(origin === 'dropdown') {
        //     ////////////////////////////////////////////////////////////////////////////////////////////
        // }

        // if(document.querySelector('.body').dataset.page === 'profile') {
        //     if(document.querySelector('.profile-view').dataset.user === username) {
        //         document.querySelector('#follower__count').innerHTML++;
        //     }
        // }
        // if(document.querySelector('.body').dataset.page === 'profile') {
        //     if(document.querySelector('.profile-view').dataset.user === document.querySelector('#user_is_authenticated').dataset.username) {
        //         document.querySelector('#following__count').innerHTML++;
        //     }
        // }
    });
}

function unfollow_user(element, username, origin) {
    Swal.fire({
        title : 'Confirm!',
        text : 'Do you want to Delete this?',
        icon : 'info',
        confirmButtonText : 'Continue',
        showCancelButton : true
    }).then((result)=>{
        if(result.isConfirmed){
            //console.log(element.getAttribute('data-username')); 
            uname = element.getAttribute('data-username')
            try{
                fetch('/'+uname+'/unfollow', {
                    method: 'PUT'
                })
                .then(() => {
                    element.setAttribute('onclick',onclick="follow_user(this,'${username}','suggestion')");
                    element.innerHTML = `Connect +`;
                    // if(origin === 'suggestion') {
                    //     element.parentElement.innerHTML = `<button class="btn btn-outline-success" type="button" onclick="follow_user(this,'${username}','suggestion')">Follow</button>`;
                    // }
                    // else if(origin === 'edit_page') {
                    //     element.parentElement.innerHTML = `<button class="btn btn-outline-success float-right" onclick="follow_user(this,'${username}','edit_page')" id="follow-btn">Follow</button>`;
                    // }
                    // else if(origin === 'dropdown') {
                    //     ///////////////////////////////////////////////////////////////////////////////////////////
                    // }
            
                    // if(document.querySelector('.body').dataset.page === 'profile') {
                    //     if(document.querySelector('.profile-view').dataset.user === username) {
                    //         document.querySelector('#follower__count').innerHTML--;
                    //     }
                    // }
                    // if(document.querySelector('.body').dataset.page === 'profile') {
                    //     if(document.querySelector('.profile-view').dataset.user === document.querySelector('#user_is_authenticated').dataset.username) {
                    //         document.querySelector('#following__count').innerHTML--;
                    //     }
                    // }
                }); 
            }
            catch(error){
                Swal.fire('error','Still a connection');
            }
        }
        else{
            Swal.fire('error','Action Aborted');
        }
    });  
}


//Search Loader
function loadLoader(){
    let Loader = document.getElementById("loadingGif");
    document.getElementById('searchForm').addEventListener('submit', function(event){
        console.log("***************Loading******************")
        Loader.style.display = "block";
    });
    
}

function editProfile(){
    let user_id = document.querySelector('#user-id').value
    let user_name = document.querySelector('#username').value
    let user_bio = document.querySelector('#ubio').value
    fetch('/edit-profile',{
        method: 'PUT',
        body: JSON.stringify({
            user_id: user_id,
            user_name: user_name,
            user_bio: user_bio
        })
    })
    .then((res)=>{
       if(res.status == 200){
        Swal.fire({
            title: 'Success',
            text: "Profile Updated Successfully",
            icon: 'success',  // or 'error', 'warning', etc.
            confirmButtonText: 'OK'
        });
       }
       else{
        Swal.fire({
            title: 'Error',
            text: "Error in Updating Profile",
            icon: 'error',  // or 'error', 'warning', etc.
            confirmButtonText: 'OK'
        });
       }
    });
    setTimeout(()=>{
        window.location.reload();
    },2000);
}

function deletePost(postId){
    Swal.fire({
        title: "Are you sure?",
        text: "You won't be able to revert this!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Yes, delete it!"
      }).then((result) => {
        if (result.isConfirmed) {
            fetch('/delete-post',{
                method: 'DELETE',
                body: JSON.stringify({
                    post_id: postId,
                })
            }).then((res)=>{
                if(res.status == 200){
                    Swal.fire({
                        title: "Deleted!",
                        text: "Post Deleted",
                        icon: "success"
                      });
                      setTimeout(()=>{
                        window.location.reload();
                    },2000);
                }
                else{
                    Swal.fire({
                        title: "Failed!",
                        text: "Post Not Deleted",
                        icon: "error"
                      });
                }
            })
        }
      });
      
}