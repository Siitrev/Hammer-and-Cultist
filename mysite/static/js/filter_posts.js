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


  // try {
  //   btn_previous_page = document.getElementById("previous-page");
  // } catch (err) {
  //   btn_previous_page = null;
  // }
  // try {
  //   btn_next_page = document.getElementById("next-page");
  // } catch (err) {
  //   btn_next_page = null;
  // }
  let btn_previous_page = document.getElementById("previous-page");
  let btn_next_page = document.getElementById("next-page");
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
      if (btn_previous_page != null){
        btn_previous_page.remove();
      }
      let max_page = parseInt(document.getElementById("max-pages").value);
      btn_active_page.innerHTML = `1 of ${max_page} pages`;
      
      if (max_page < 2){
        if (btn_next_page != null){
          btn_next_page.remove();
        }
        btn_active_page.innerHTML = 1;
      } else if (btn_next_page == null){
        createNextButton();
      }
    } else {
      console.log(`Error: ${xhr.status}`);
    }
    return;
  }
  
}
/* <button type="button" class="btn btn-secondary p-0" id="next-page" onclick="controller('next')">
<svg xmlns="http://www.w3.org/2000/svg" width="40" height="30" fill="currentColor" class="bi bi-arrow-right" viewBox="0 0 16 16">
    <path fill-rule="evenodd" d="M1 8a.5.5 0 0 1 .5-.5h11.793l-3.147-3.146a.5.5 0 0 1 .708-.708l4 4a.5.5 0 0 1 0 .708l-4 4a.5.5 0 0 1-.708-.708L13.293 8.5H1.5A.5.5 0 0 1 1 8"/>
</svg>
</button> */

function createNextButton(){
  let page_controller = document.getElementById("page-controller");
  let btn = document.createElement("button");
  btn.setAttribute("type","button");
  btn.setAttribute("class","btn btn-secondary p-0");
  btn.setAttribute("id","next-page");
  btn.setAttribute("onclick","controller('next')");

  let svg = document.createElementNS("http://www.w3.org/2000/svg","svg");
  svg.setAttribute("xmlns","http://www.w3.org/2000/svg");
  svg.setAttribute("width","40");
  svg.setAttribute("height","30");
  svg.setAttribute("fill","currentColor");
  svg.setAttribute("class","bi bi-arrow-right");
  svg.setAttribute("viewBox","0 0 16 16");
  
  let path = document.createElementNS("http://www.w3.org/2000/svg", "path");
  path.setAttribute("fill-rule", "evenodd");
  path.setAttribute("d", "M1 8a.5.5 0 0 1 .5-.5h11.793l-3.147-3.146a.5.5 0 0 1 .708-.708l4 4a.5.5 0 0 1 0 .708l-4 4a.5.5 0 0 1-.708-.708L13.293 8.5H1.5A.5.5 0 0 1 1 8");

  svg.appendChild(path);
  btn.appendChild(svg);
  
  page_controller.append(btn);
}