////////// Manage Follow button  ///////////////
const btn = document.querySelector('#follow_btn');
const followers_count = document.querySelector('#followers_count');
const visited_user_id = document.querySelector('h1').dataset.visited_id;
//const user_id = document.querySelector('#user').dataset.user_id;

// If the visited_user is different that the user, the Follow button appear
if (btn) {
   let is_following = btn.innerHTML.includes("Follow")? false : true;

    btn.addEventListener('click', () => {
        // toggle Follow/Unfollow in database
        fetch(`/follow/${visited_user_id}`);
        // Update the counter and the plurilize of "person(s)"
        let count = parseInt(followers_count.innerHTML);
        if (is_following) {
            btn.innerHTML = "Follow";
            count -= 1;
        } else {
            btn.innerHTML = "Unfollow";
            count += 1;
        }
        let person_s = count == 1? "person" : "persons";
        followers_count.innerHTML = count;
        document.querySelector("#counter_person").innerHTML = person_s;

        is_following = !is_following;
    }) 
}

///////////// Manage updating a post ////////////////////
const edit_handler = (event) => {
    const edit_link = event.target;
    const post_elt = edit_link.parentElement;
    // get the -elt id
    const post_id = post_elt.dataset.post_id;

    const post_text_elt = document.querySelector(`#post-content-${post_id}`);
    // get the content of the post
    const post_content = post_text_elt.innerHTML;
    // Diplay the editor(prefilled) and hide the post content + the edit link
    edit_link.style.display = "none";
    const update_area = document.createElement("div");
    update_area.innerHTML = `
    <textarea id="text-area-${post_id}" class="post-textarea" type="text" name="text" placeholder="Posts are 280 characters max" maxlength="280"></textarea>
    <br>
    <button id="save-btn-${post_id}" class="btn btn-primary">Save</button>`
    const text_area = update_area.querySelector(`#text-area-${post_id}`);
    text_area.innerHTML = post_content;
    post_elt.replaceChild(update_area, post_text_elt);
    // handle the save btn click
    update_area.querySelector(`#save-btn-${post_id}`).addEventListener('click', () => {
        // get the modifiacted content and fetch it to the API
        const new_content = text_area.value;
        fetch(`/post-update/${post_id}`, {
            method: "PUT",
            body: JSON.stringify(`${new_content}`)
        });
        // Replace the textarea with the normal post display
        post_text_elt.innerHTML = new_content;
        post_elt.replaceChild(post_text_elt, update_area);
        edit_link.style.display = "block";
        // Display a modified label in place of update time
        if (post_text_elt.nextElementSibling.classList.contains("update_time") ||
            post_text_elt.nextElementSibling.classList.contains("modified")) {
            // means the <p> for the update time already exist
            const time_update_elt = post_text_elt.nextElementSibling;
            time_update_elt.classList.add("modified");
            time_update_elt.classList.remove("update_time");
            time_update_elt.innerHTML = "MODIFIED";
        } else {
            // means the post has never been updated before
            const time_update_elt = document.createElement('p');
            time_update_elt.classList.add("modified");
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

//////////////// Manage Likes  /////////////////////:
document.addEventListener('DOMContentLoaded', () => {
    const like_btns = document.querySelectorAll(".like-btn");
    for (const like_btn of like_btns) {
        like_btn.addEventListener('click', () => {
            const post_id = like_btn.dataset.post_id;
            // toggle the like/unlike in the database
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
