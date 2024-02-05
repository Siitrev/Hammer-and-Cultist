async function filterPosts(first_load = false){
  const xhr = new XMLHttpRequest();
  let url = window.location.href + "sort/posts";
  if (first_load){
    xhr.open("GET", url);
    xhr.send(); 
    xhr.responseType = "text";
    xhr.onload = () => {
      if (xhr.readyState == 4 && xhr.status == 200) {
        const data = xhr.response;
        document.querySelector("section.all-posts").innerHTML = data;
      } else {
        console.log(`Error: ${xhr.status}`);
      }
    };
    return
  }
  const form = document.getElementById("sortForm");
  const formData = new FormData(form);
  let spinner = document.getElementsByClassName("loading")[0]
  let blur = document.getElementsByClassName("blur")[0]
  spinner.style.visibility = "visible";
  blur.style.visibility = "visible";
  request = {};
  sortSelect = formData.get("sort");
  sortDirection = formData.get("order");
  filters = formData.getAll("filter");
  request["sort"] = sortSelect;
  request["order"] = sortDirection;
  request["filters"] = filters;
  
  let json = JSON.stringify(request);
  console.log(json);

  xhr.open("POST", url); 

  let csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
  
  xhr.setRequestHeader("X-CSRFToken", csrfToken); 
  xhr.setRequestHeader("Accept", "application/json");
  xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  xhr.send(json);
  xhr.onload = () => {
    if (xhr.readyState == 4 && xhr.status == 200) {
      const data = xhr.response;
      document.querySelector("section.all-posts").innerHTML = data;
      spinner.style.visibility = "hidden";
      blur.style.visibility = "hidden";
    } else {
      console.log(`Error: ${xhr.status}`);
    }
  };
}
filterPosts(true)