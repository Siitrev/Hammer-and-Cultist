import { getCookie } from "./cookies.js"

window.addEventListener("DOMContentLoaded", () =>{
    document.getElementById("cancel-btn").addEventListener("click", () => {
        history.back();
    })

    let publishBtn = document.getElementById("publish-btn");
    if (publishBtn !== null){
        publishBtn.addEventListener("click", () =>{
            let url = window.location.pathname;
            url = url.replace("edit-post", "publish-post")
            const csrf = getCookie("csrftoken");
            fetch(url, {
                method : "PATCH",
                headers: {'X-CSRFToken': csrf},
                mode: 'same-origin'
            }).then(res => window.location.assign(res.url))
        })
    }
})