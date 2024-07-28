function handle_select(){
    let select = document.getElementById("id_tags");
    let list = document.getElementsByClassName("list-group")[0];
    let hidden_input_div = document.getElementById("hidden_inputs");

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

    chosen_tag_input.value = selected_child.value;
    
    list.append(create_list_element(selected_child, select.selectedIndex));

    selected_child.disabled = true;

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

function create_list_element(option, position){
    let list_element = document.createElement("button");  
    list_element.innerHTML = option.innerHTML;
    list_element.type = "button";
    list_element.value = option.value;
    list_element.setAttribute("position", position);

    list_element.setAttribute("class", "list-group-item-action list-group-item w-dynamic");
    list_element.addEventListener("pointerover", _ =>{ 
        list_element.setAttribute("class", "list-group-item list-group-item-action list-group-item-danger w-dynamic");
    });
    list_element.addEventListener("pointerleave", _ =>{ 
        list_element.setAttribute("class", "list-group-item list-group-item-action list-group-item w-dynamic");
    });
    list_element.setAttribute("onclick","remove_selected_tag(this)");
    return list_element
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

function fill_on_load(select, array_of_inputs, list){
    array_of_options = Array.from(select.options);
    array_of_inputs.forEach(input => {
        if (input.value !== ""){
            let position = 0; 
            array_of_options.forEach(option => {
                if (option.value === input.value){
                    list.append(create_list_element(option, position))
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
    let hidden_input_div = document.getElementById("hidden_inputs");
    let array_of_inputs = Array.from(hidden_input_div.children);
    array_of_inputs.forEach(input =>{
        if (!input.hasAttribute("value"))
            input.setAttribute("value", "");
    })

    list.setAttribute("class","list-group");
    list.setAttribute("name","chosen-tags");
    document.getElementById("chosen_tags").append(list);
    document.getElementById("id_tags").name = "";

    select.addEventListener("change", handle_select);
    select.value="";

    fill_on_load(select, array_of_inputs, list)
});