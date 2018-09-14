(function(account){
    $('#ap_customer_name').value = account.username;
    $('#ap_email').value = account.email;
    $('#ap_password').value = account.password;
    $('#ap_password_check').value = account.repeat;
    $('#continue').click();
})('${account}');