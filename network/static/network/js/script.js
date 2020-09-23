//this is the script for like, edit 
var like = document.querySelectorAll(".liked")
like.forEach(element => {
    element.addEventListener("click", () => handleLike(element));

});



var edit = document.querySelectorAll('.edit');
edit.forEach(element => {
    element.addEventListener("click", () => handleEdit(element));
})

var text_area = document.querySelectorAll('.textarea');

text_area.forEach(element => {
    element.addEventListener("keyup", (e) => {
        if (e.keyCode == 13 && e.shiftKey) return;
        if (e.keyCode == 13) {
            id = element.getAttribute('data-id');
            value = element.value;


            form = new FormData();
            form.append('post_id', id);
            form.append('new_value', value);
            fetch('/editpost', {
                method: "POST",
                body: form,
            }).then(res => {
                document.getElementById(`post-content-${id}`).textContent = value;
                document.getElementById(`post-content-${id}`).style = "block";
                element.style.display = "none";
                element.value = value.trim();

                edit_btn = document.getElementById(`edit-btn-${id}`);
                edit_btn.setAttribute('data-state', 'closed');
            })
        }
    })
})
function handleEdit(element) {
    id = element.getAttribute('data-id');
    state = element.getAttribute('data-state');
    if (state == 'closed') {
        document.getElementById(`post-edit-${id}`).style.display = "block";
        element.setAttribute('data-state', 'open');
    }
    else if (state == 'open') {
        document.getElementById(`post-edit-${id}`).style.display = "none";
        element.setAttribute('data-state', 'closed');
    }
}



function handleLike(element) {
    element.addEventListener('click', () => {

        post_id = element.getAttribute('data-id');
        is_liked = element.getAttribute('data-is_liked');
        icon = document.getElementById(`post-like-${post_id}`);
        count = document.getElementById(`post-count-${post_id}`);
        console.log(post_id, is_liked);
        form = new FormData();
        form.append("post_id", post_id);
        form.append("is_liked", is_liked);
        fetch('/like', {
            method: 'POST',
            body: form,

        }).then((res) => res.json())
            .then((res) => {
                if (res.status == 201) {
                    if (res.is_liked === 'true') {
                        icon.innerHTML = `<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-heart-fill" fill="currentColor"
                        xmlns="http://www.w3.org/2000/svg">
                        <path fill-rule="evenodd"
                            d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314z" />
                    </svg>`;
                        element.setAttribute('data-is_liked', "true");

                    }
                    else {
                        // is_liked was returned false
                        icon.innerHTML = `<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-heart" fill="currentColor"
                        xmlns="http://www.w3.org/2000/svg">
                        <path fill-rule="evenodd"
                            d="M8 2.748l-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01L8 2.748zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143c.06.055.119.112.176.171a3.12 3.12 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15z" />
                    </svg>`;
                        element.setAttribute('data-is_liked', "false");

                    }
                    count.textContent = res.like_count;
                }


            }).catch(function (res) {
                alert('OOPS! Something went wrong.');
            });

    });

}