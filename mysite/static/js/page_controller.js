async function controller(action){
    let url = window.location.href;
    let page_index = url.indexOf("page");
    if(page_index != -1){
        console.log(page_index)
        let new_page_num = parseInt(url.substring(page_index+5, url.indexOf("?")));
        if (isNaN(new_page_num )){
            new_page_num = parseInt(url.substring(url.lastIndexOf("/")+1));
        }
        if (action === "next"){
            new_page_num = new_page_num + 1;
            url = url.replace(/\/page\/\d/,`/page/${new_page_num}`);
        }
        else if (action === "previous"){
            new_page_num = new_page_num - 1;
            if (new_page_num == 1){
                url = url.replace(/\/page\/\d/,'');
            }
            else{
                url = url.replace(/\/page\/\d/,`/page/${new_page_num }`);
            }
        }   
    }
    else{
        if (action === "next"){
            url = url.replace(/\/blog\//,`/blog/page/2`);
        }
    }
    document.location.assign(url);
}
