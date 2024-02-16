var script_data = document.currentScript.dataset;

async function getData() {
    const data = script_data;
    let url = data.url;
    let button = document.getElementById("maxCom");
    let maxComs = parseInt(button.value) + 10;
    let comments = parseInt(data.commentsLen);
    if (maxComs >= comments){
      button.setAttribute("class", "d-none");
    }
    const response = await fetch(url + "?" + new URLSearchParams({maxCom : maxComs}), {
      method: "GET"
    });
    button.setAttribute("value", maxComs);
    return response.text(); 
  }
  
  function getComments(){
    getData().then(res=>{
      if(res != undefined){
        document.querySelectorAll("section.comments")[0].innerHTML = res;
      }
    });
  }
window.addEventListener("DOMContentLoaded", getComments());