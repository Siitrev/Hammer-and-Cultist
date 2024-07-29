function handle_select(){
    let select = document.getElementById("id_tags");
    let list = document.getElementsByClassName("list-group")[0];
    let hiddenInputDiv = document.getElementById("hidden_inputs");

    let selectedChild = select.selectedOptions[0];

    if (selectedChild.value === ""){
        return;
    }
    let arrayOfInputs = Array.from(hiddenInputDiv.children);
    
    let chosen_tag_input = arrayOfInputs.find(input => {
        if (input.getAttribute("value") === ""){
            return true;
        }
        return false;
    });

    chosen_tag_input.value = selectedChild.value;
    
    list.append(createListElement(selectedChild, select.selectedIndex));

    selectedChild.disabled = true;

    if (is_invalid_select()){
        select.disabled = true;
    }

    select.value = "";
}

function is_invalid_select(){
    let list = document.getElementsByClassName("list-group")[0];
    if (list.children.length === 3){
        return true;
    }
    return false;
}

function createListElement(option, position){
    let listElement = document.createElement("button");  
    listElement.innerHTML = option.innerHTML;
    listElement.type = "button";
    listElement.value = option.value;
    listElement.setAttribute("position", position);

    listElement.setAttribute("class", "list-group-item-action list-group-item w-dynamic");
    listElement.addEventListener("pointerover", _ =>{ 
        listElement.setAttribute("class", "list-group-item list-group-item-action list-group-item-danger w-dynamic");
    });
    listElement.addEventListener("pointerleave", _ =>{ 
        listElement.setAttribute("class", "list-group-item list-group-item-action list-group-item w-dynamic");
    });
    listElement.setAttribute("onclick","remove_selected_tag(this)");
    return listElement
}

function remove_selected_tag(listElement){
    let select = document.getElementById("id_tags");
    let position = parseInt(listElement.getAttribute("position"));
    let hiddenInputDiv = document.getElementById("hidden_inputs");
    let arrayOfInputs = Array.from(hiddenInputDiv.children);

    let listElementInput = arrayOfInputs.find(input =>{
        if (input.value == listElement.value){
            return true;
        }
        return false;
    });
    listElementInput.setAttribute("value", "");
    
    if (select.disabled){
        select.disabled = false;
    }
    select.options[position].disabled = false;
    listElement.remove();
}

function fill_on_load(select, arrayOfInputs, list){
    arrayOfOptions = Array.from(select.options);
    arrayOfInputs.forEach(input => {
        if (input.value !== ""){
            let position = 0; 
            arrayOfOptions.forEach(option => {
                if (option.value === input.value){
                    list.append(createListElement(option, position))
                    option.disabled = true
                }
                position++;
            })
        }
    })

    if (is_invalid_select()){
        select.disabled = true;
    }
}

window.addEventListener("DOMContentLoaded", _ =>{
    let list = document.createElement("ul");
    let select = document.getElementById("id_tags");
    let hiddenInputDiv = document.getElementById("hidden_inputs");
    let arrayOfInputs = Array.from(hiddenInputDiv.children);

    arrayOfInputs.forEach(input =>{
        if (!input.hasAttribute("value"))
            input.setAttribute("value", "");
    })

    list.setAttribute("class","list-group");
    list.setAttribute("name","chosen-tags");
    document.getElementById("chosen_tags").append(list);
    document.getElementById("id_tags").name = "";

    select.addEventListener("change", handle_select);
    select.value = "";

    fill_on_load(select, arrayOfInputs, list);

    let imgClearSpan = document.getElementById("image-clear_id");

    if (imgClearSpan !== null){
        imgClearSpan.parentElement.remove();
    }
});