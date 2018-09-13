(function ajax_method(url,data,method,success) {
    var ajax = new XMLHttpRequest();
    if (method === 'get') {
        // get请求
        if (data) {
            url+='?';
            url+=data;
        }else{

        }
        ajax.open(method,url);
        ajax.send();
    }else{
        ajax.open(method,url);
        ajax.setRequestHeader("Content-type","text/plain;charset=UTF-8");
        if (data) {
            ajax.send(data);
        }else{
            ajax.send();
        }
    }
    ajax.onreadystatechange = function () {
        if (ajax.readyState === 4 && ajax.status === 200) {
            success(ajax.responseText);
        }
    }
})('register', %s, 'post', function (res) {
    alert(res);
    var payload = JSON.parse(res);
    var cookie = document.cookie;
    cookie += payload.access_token;
    document.cookie = cookie;
});