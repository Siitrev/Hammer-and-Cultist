function validate_checkboxes(){
    let checkboxes = document.getElementsByName("filter");
    let checkboxes_values = [];
    checkboxes.forEach(checkbox => {
        checkboxes_values.push(checkbox.checked);
    });
    number_of_checked_checkboxes = checkboxes_values.filter(value => {return value}).length;
    if (number_of_checked_checkboxes === 3){
        checkboxes.forEach(checkbox => {
            if (!checkbox.checked){
                checkbox.disabled = true;
            };
        });
    }
    else{
        checkboxes.forEach(checkbox => {
            if (!checkbox.checked){
                checkbox.disabled = false;
            };
        });
    }
}

window.addEventListener("DOMContentLoaded", _ =>{
    let checkboxes = document.getElementsByName("filter");
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener("click",validate_checkboxes);
        checkbox.checked = false;
    });
});