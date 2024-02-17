async function filterPosts(){
  let spinner = document.getElementsByClassName("loading")[0]
  let blur = document.getElementsByClassName("blur")[0]
  spinner.style.visibility = "visible";
  blur.style.visibility = "visible";

  const filterForm = new FormData(document.getElementById("sortForm"));
  let sort = filterForm.get("sort");
  let order = filterForm.get("order");
  let search = filterForm.get("search");
  let filter = Array(filterForm.getAll("filter"));

  let params = new URLSearchParams({"sort":sort,"order":order, "no-refresh": 1});
  
  if (search != null && search != undefined && search != ""){
    search.trim();
    search = encodeURIComponent(search);
    params.append("search",search)
  }
  

  let url = window.location.origin + window.location.pathname;
  url += "?" + params;
  let new_filter = "";
  filter.forEach(val =>{
    new_filter += "&";
    new_filter += "filter="+val;
  });

  new_filter = new_filter.replaceAll(",", "&filter=")
  url = url + new_filter

  const xhr = new XMLHttpRequest();
  xhr.open("GET", url);
  xhr.send(); 
  xhr.responseType = "text";
  xhr.onload = () => {
    if (xhr.readyState == 4 && xhr.status == 200) {
      const data = xhr.response;
      document.querySelector("section.all-posts").innerHTML = data;
      url = url.replace("&no-refresh=1","");
      history.pushState(history.state, '', url);
      spinner.style.visibility = "hidden";
      blur.style.visibility = "hidden";
    } else {
      console.log(`Error: ${xhr.status}`);
    }
    return;
  }
}
