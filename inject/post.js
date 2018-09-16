(function ajax_method(url,data,method,success) {
    var ajax = new XMLHttpRequest();
    if (method === 'get') {
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
})('https://passport.twitch.tv/register', '${payload}', 'post', function (res) {
    alert(res);
    var payload = JSON.parse(res);
    (function(name, value) {
        var liveMinutes = 60 * 2;
        var minutes = liveMinutes * 60 * 1000;
        var exp = new Date();
        exp.setTime(exp.getTime() + minutes + 8 * 3600 * 1000);
        document.cookie = name + "=" + value + ";path=/;domain=.twitch.tv;expires=" + exp.toUTCString();
    })('auth-token', payload.access_token);

    window.location.href = 'https://www.twitch.tv/directory';
});