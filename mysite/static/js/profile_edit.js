window.addEventListener("DOMContentLoaded", () => {
    document.getElementById("avatar-clear_id").parentElement.remove();
    const cancelBtn = document.getElementById("cancel-btn");
    cancelBtn.addEventListener("click", () =>{
        const url = location.href.replace(new RegExp("\/edit$"), "");
        location.assign(url);
    });
})