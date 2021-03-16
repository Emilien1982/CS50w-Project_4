const btn = document.querySelector('#follow_btn');
const followers_count = document.querySelector('#followers_count');
const visited_user_id = document.querySelector('h1').dataset.visited_id;
const user_id = document.querySelector('#user').dataset.user_id;

// If the visited_user is different that the user, the Follof button appear
if (visited_user_id !== user_id) {
   let is_following = btn.innerHTML == "Follow"? false : true;

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


const edit_handler = (event) => {
    const post = event.target.parentElement;
    const edit_link = event.target;
    const post_text_elt = event.target.nextElementSibling;
    // get the content of the post
    const post_content = post_text_elt.innerHTML;
    // get the post id
    const post_id = edit_link.dataset.post_id;
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
        const new_content = text_area.value;
        fetch(`/post-update/${post_id}`, {
            method: "PUT",
            body: JSON.stringify(`${new_content}`)
        });
        post_text_elt.innerHTML = new_content;
        post.replaceChild(post_text_elt, update_area);
        edit_link.style.display = "block";

        console.log(new_content);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const edit_links = document.querySelectorAll(".edit-links");
    console.log(edit_links);
    for (const link of edit_links) {
        link.addEventListener('click', edit_handler);
    }
})
