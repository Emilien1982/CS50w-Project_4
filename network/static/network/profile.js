const btn = document.querySelector('#follow_btn');
const followers_count = document.querySelector('#followers_count');
const visited_user_id = document.querySelector('h1').dataset.visited_id;
console.log(btn.innerHTML);
let is_following = btn.innerHTML == "Follow"? false : true;
console.log("is_following: " + is_following);

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
