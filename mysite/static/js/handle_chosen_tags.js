function handle_select(){
    let select = document.getElementById("id_tags");
    let list = document.getElementsByClassName("list-group")[0];
    let hidden_input_div = document.getElementById("hidden_inputs");

    console.log(list.children.length);

    let selected_child = select.selectedOptions[0];

    if (selected_child.value === ""){
        return;
    }
    let array_of_inputs = Array.from(hidden_input_div.children);
    
    let list_element = document.createElement("button");  
    let chosen_tag_input = array_of_inputs.find(input => {
        if (input.getAttribute("value") === ""){
            return true;
        }
        return false;
    });

    list_element.innerHTML = selected_child.innerHTML;
    list_element.type = "button";
    list_element.value = selected_child.value;
    chosen_tag_input.value = selected_child.value;
    list_element.setAttribute("position",select.selectedIndex);

    list_element.setAttribute("class", "list-group-item-action list-group-item w-dynamic");
    list_element.addEventListener("pointerover", _ =>{ 
        list_element.setAttribute("class", "list-group-item list-group-item-action list-group-item-danger w-dynamic");
    });
    list_element.addEventListener("pointerleave", _ =>{ 
        list_element.setAttribute("class", "list-group-item list-group-item-action list-group-item w-dynamic");
    });
    list_element.setAttribute("onclick","remove_selected_tag(this)");
    
    list.append(list_element);

    selected_child.disabled = true;

    if (is_invalid_select()){
        select.disabled = true;
    }

    select.value = "";

    console.log(select.selectedOptions[0].innerHTML);
}

function is_invalid_select(){
    let list = document.getElementsByClassName("list-group")[0];
    if (list.children.length === 3){
        return true;
    }
    return false;
}

function remove_selected_tag(list_element){
    let select = document.getElementById("id_tags");
    let position = parseInt(list_element.getAttribute("position"));
    let hidden_input_div = document.getElementById("hidden_inputs");
    let array_of_inputs = Array.from(hidden_input_div.children);

    let list_element_input = array_of_inputs.find(input =>{
        if (input.value == list_element.value){
            return true;
        }
        return false;
    });
    list_element_input.setAttribute("value", "");
    
    if (select.disabled){
        select.disabled = false;
    }
    select.options[position].disabled = false;
    list_element.remove();
}

window.addEventListener("DOMContentLoaded", _ =>{
    let list = document.createElement("ul");
    let select = document.getElementById("id_tags");
    let hidden_input_div = document.getElementById("hidden_inputs");
    let array_of_inputs = Array.from(hidden_input_div.children);
    array_of_inputs.forEach(input =>{
        input.setAttribute("value", "");
    })

    list.setAttribute("class","list-group");
    list.setAttribute("name","chosen-tags");
    document.getElementById("chosen_tags").append(list);
    document.getElementById("id_tags").name = "";

    select.addEventListener("change", handle_select);
    select.value="";
});