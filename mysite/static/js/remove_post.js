function remove_post(self, username, post_id){
    let url = location.href.replace(`/user/${username}/posts/`, "");
    url += `/blog/${username}/delete-post/${post_id}`;

    const xhr = new XMLHttpRequest();
    xhr.open("DELETE", url); 
    let csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    xhr.setRequestHeader("X-CSRFToken", csrfToken);
    xhr.send("delete");
    xhr.onload = () => {
        if (xhr.readyState == 4 && xhr.status == 200) {
            self.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.remove()
        } else {
            console.log(`Error: ${xhr.status}`);
        }
    };
}