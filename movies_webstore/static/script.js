function AddFavorites(){
    const get_url = window.location.href;
    const regex = /\/+[0-9]+\//;
    const getUrl = get_url.match(regex);
    const getUrlRegEx = getUrl[0].slice(1,-1);
    console.log(getUrlRegEx);

    $.post( "/movieID", {
        js_movieID: getUrlRegEx 
    });
}