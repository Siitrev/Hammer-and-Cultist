
async function like(evt){
    let url = location.href
    const xhr = new XMLHttpRequest();
    xhr.open("PUT", url); 
    let csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    xhr.setRequestHeader("X-CSRFToken", csrfToken);

    xhr.send("Update");
    xhr.onload = () => {
        if (xhr.readyState == 4 && xhr.status == 200) {
            document.getElementById("like-count").innerHTML = `Likes: ${xhr.responseText}`;
            evt.target.innerHTML = "Dislike";
            evt.target.value = "dislike";
            evt.target.removeEventListener("click", like);
            evt.target.addEventListener("click", dislike);
        } else {
            console.log(`Error: ${xhr.status}`);
        }
    };
}

async function dislike(evt){
    let url = location.href

    const xhr = new XMLHttpRequest();
    xhr.open("DELETE", url); 
    let csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    xhr.setRequestHeader("X-CSRFToken", csrfToken);

    xhr.send("Delete");
    xhr.onload = () => {
        if (xhr.readyState == 4 && xhr.status == 200) {
            document.getElementById("like-count").innerHTML = `Likes: ${xhr.responseText}`;
            evt.target.innerHTML = "Like";
            evt.target.value = "like"
            evt.target.removeEventListener("click", dislike);
            evt.target.addEventListener("click", like);
        } else {
            console.log(`Error: ${xhr.status}`);
        }
    };
}

window.addEventListener("DOMContentLoaded", () =>{
    let like_controller = document.getElementById("like-controller");
    if(like_controller.value === "like"){
        like_controller.addEventListener("click", like);
    }
    else if(like_controller.value === "dislike"){
        like_controller.innerHTML = "Dislike";
        like_controller.addEventListener("click", dislike);
    }
});