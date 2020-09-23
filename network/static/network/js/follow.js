var follow_btn = document.getElementById("follow-btn");
follow_btn.addEventListener('click', () => {
    user = follow_btn.getAttribute('data-user');
    cur_user = follow_btn.getAttribute('data-target-user');
    command = follow_btn.textContent.trim();

    console.log(user, cur_user, command);
    form = new FormData();
    form.append("user", user);
    form.append("cur_user", cur_user);
    form.append("command", command);
    fetch("/follow", {
        method: "POST",
        body: form,

    }).then(res => res.json())
        .then(res => {
            if (res.status == 201) {
                follow_btn.textContent = res.command;
                document.getElementById('followers').textContent = `Followers: ${res.follow_count}`;

            }
        });

});