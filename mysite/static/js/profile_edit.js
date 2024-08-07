window.addEventListener("DOMContentLoaded", () => {
    let uselessCheckbox = document.getElementById("avatar-clear_id");
    if (uselessCheckbox != null){
        uselessCheckbox.parentElement.remove();
    }
    const cancelBtn = document.getElementById("cancel-btn");
    cancelBtn.addEventListener("click", () =>{
        const url = location.href.replace(new RegExp("\/edit$"), "");
        location.assign(url);
    });
})