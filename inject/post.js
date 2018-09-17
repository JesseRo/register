var script=document.createElement("script");
script.type="text/javascript";
script.src="https://code.jquery.com/jquery-3.1.1.min.js";
document.getElementsByTagName('head')[0].appendChild(script);

script.onload = function() {
    jQuery.ajax({
        url:'https://passport.twitch.tv/register',
        type: 'POST',
        crossDomain: true,
        contentType: 'text/plain;charset=UTF-8',
        xhrFields: {withCredentials: true},
        data: '${payload}',
        success: function (res) {
            alert(res);
            var liveMinutes = 60 * 2000;
            var minutes = liveMinutes * 60 * 1000;
            var exp = new Date();
            exp.setTime(exp.getTime() + minutes + 8 * 3600 * 1000);
            document.cookie = "auth-token=" + res.access_token + ";path=/;domain=.twitch.tv;expires=" + exp.toUTCString();
            alert('redirect');
            window.location.href = 'https://twitch.amazon.com/link?confirm=ALWAYS&locale=en-US&returnUri=https%3A%2F%2Ftwitch.amazon.com%2Fprime%2Fsignup%2Fus%3FdiscoveryLocation%3Dsm_w_tup_ntp_t_c%26locale%3Den-US';
        }
    });
};

