async function filterPosts(){
  // Get loading elements
  let spinner = document.getElementsByClassName("loading")[0]
  let blur = document.getElementsByClassName("blur")[0]
  
  // Start loading
  spinner.style.visibility = "visible";
  blur.style.visibility = "visible";

  // Get form data
  const filterForm = new FormData(document.getElementById("sortForm"));
  let sort = filterForm.get("sort");
  let order = filterForm.get("order");
  let search = filterForm.get("search");
  let filter = Array(filterForm.getAll("filter"));

  let params = new URLSearchParams({"sort":sort,"order":order, "no-refresh": 1});

  // Clear search value
  if (search != null && search != undefined && search != ""){
    search.trim();
    search = encodeURIComponent(search);
    params.append("search",search)
  }
  


  // Preapare URL
  let url = window.location.origin + window.location.pathname;
  if(window.location.pathname.indexOf("page") != -1){
    url = url.replace(/\/page\/\d/,"");
  }
  url += "?" + params;
  let new_filter = "";
  filter.forEach(val =>{
    new_filter += "&";
    new_filter += "filter="+val;
  });
  
  new_filter = new_filter.replaceAll(",", "&filter=");
  url = url + new_filter;

  // Get page controller info
  let btn_previous_page;
  let btn_next_page;
  try {
    btn_previous_page = document.getElementById("previous-page");
  } catch (err) {
    btn_previous_page = null;
  }
  try {
    btn_next_page = document.getElementById("previous-page");
  } catch (err) {
    btn_next_page = null;
  }
  let btn_active_page = document.getElementById("active-page");

  // Send request
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

      // Set controller
      if (btn_previous_page){
        btn_previous_page.visibility = "visible";
      }
      let max_page = document.getElementById("max-pages").value;
      btn_active_page.innerHTML = `1 of ${max_page} pages`;
      if (btn_next_page){
        btn_next_page.visibility = "visible";
      }
      if (max_page === "1" || max_page === "0"){
        if (btn_next_page){
          btn_next_page.visibility = "hidden";
        }
        btn_active_page.innerHTML = 1;
      }
    } else {
      console.log(`Error: ${xhr.status}`);
    }
    return;
  }
}
