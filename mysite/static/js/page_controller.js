async function controller(action){
    let url = window.location.href;
    let pageIndex = url.indexOf("page");
    if(pageIndex != -1){
        console.log(pageIndex)
        let newPageNum = parseInt(url.substring(pageIndex+5, url.indexOf("?")));
        if (isNaN(newPageNum)){
            newPageNum = parseInt(url.substring(url.lastIndexOf("/")+1));
        }
        if (action === "next"){
            newPageNum = newPageNum + 1;
            url = url.replace(/\/page\/\d/,`/page/${newPageNum}`);
        }
        else if (action === "previous"){
            newPageNum = newPageNum - 1;
            if (newPageNum == 1){
                url = url.replace(/\/page\/\d/,'');
            }
            else{
                url = url.replace(/\/page\/\d/,`/page/${newPageNum }`);
            }
        }   
    }
    else{
        if (action === "next"){
            url = url.replace(/\/blog\//,`/blog/page/2`);
        }
    }
    if (!url.endsWith("#sortForm")){
        url += "#sortForm"
    }
    document.location.assign(url);
}
