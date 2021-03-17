

////////// Manage Follow button
const btn = document.querySelector('#follow_btn');
const followers_count = document.querySelector('#followers_count');
const visited_user_id = document.querySelector('h1').dataset.visited_id;
const user_id = document.querySelector('#user').dataset.user_id;

// If the visited_user is different that the user, the Follow button appear
if (btn) {
   let is_following = btn.innerHTML.includes("Follow")? false : true;

    btn.addEventListener('click', () => {
        fetch(`/follow/${visited_user_id}`);
        if (is_following) {
            btn.innerHTML = "Follow";
            followers_count.innerHTML = parseInt(followers_count.innerHTML) - 1;
        } else {
            btn.innerHTML = "Unfollow";
            followers_count.innerHTML = parseInt(followers_count.innerHTML) + 1;
        }
        is_following = !is_following;
    }) 
}

///////////// Manage updating a post
const edit_handler = (event) => {
    const post = event.target.parentElement;
    const edit_link = event.target;
    const post_text_elt = event.target.nextElementSibling;
    // get the content of the post
    const post_content = post_text_elt.innerHTML;
    // get the post id
    const post_id = edit_link.parentElement.dataset.post_id;
    // Diplay the editor(prefilled) and hide the post content + the edit link
    edit_link.style.display = "none";
    const update_area = document.createElement("div");
    update_area.innerHTML = `
    <textarea id="text-area" class="post-textarea" type="text" name="text" placeholder="Posts are 280 characters max" maxlength="280"></textarea>
    <br>
    <button id="save-btn" class="btn btn-primary">Save</button>`
    post.replaceChild(update_area, post_text_elt);
    const text_area = document.querySelector("#text-area");
    text_area.innerHTML = post_content;
    // handle the save btn click
    document.querySelector('#save-btn').addEventListener('click', () => {
        // get the modifiacted content and fetch it to the API
        const new_content = text_area.value;
        fetch(`/post-update/${post_id}`, {
            method: "PUT",
            body: JSON.stringify(`${new_content}`)
        });
        // Replace the textarea with the normal post display
        post_text_elt.innerHTML = new_content;
        post.replaceChild(post_text_elt, update_area);
        edit_link.style.display = "block";
        // Display the modified update time
        //console.log(post_text_elt.nextElementSibling);
        if (post_text_elt.nextElementSibling.classList.contains("update_time")) {
            console.log("already modified");
            // means the <p> for the update time already exist
            const time_update_elt = post_text_elt.nextElementSibling;
            time_update_elt.classList += " modified";
            time_update_elt.innerHTML = "MODIFIED";
        } else {
            console.log("never modified");
            // means the post never been updated before
            const time_update_elt = document.createElement('p');
            time_update_elt.classList += " modified";
            time_update_elt.innerHTML = "MODIFIED";
            post_text_elt.insertAdjacentElement('afterEnd', time_update_elt)
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const edit_links = document.querySelectorAll(".edit-links");
    for (const link of edit_links) {
        link.addEventListener('click', edit_handler);
    }
})

//////////////// Manage Likes
document.addEventListener('DOMContentLoaded', () => {
    const like_btns = document.querySelectorAll(".like-btn");
    for (const like_btn of like_btns) {
        like_btn.addEventListener('click', () => {
            const post_id = like_btn.parentElement.dataset.post_id;
            fetch(`/like/${post_id}`);
            // update the like-btn and the the likes count
            const like_counter = document.querySelector(`#counter_${post_id}`);
            const num_of_likes = parseInt(like_counter.innerHTML);
            if (like_btn.innerHTML.includes("Like")) {
                like_btn.innerHTML = "Unlike";
                like_counter.innerHTML = num_of_likes + 1;
            } else {
                like_btn.innerHTML = "Like";
                like_counter.innerHTML = num_of_likes - 1;
            }
        });
    }
})






// ACCORDER LE PLURIEL A "PERSON" APRES UN FOLLOW/UNFOLLOW