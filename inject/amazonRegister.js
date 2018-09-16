(function(account){
    document.getElementById('ap_customer_name').value = account.username;
    document.getElementById('ap_email').value = account.email;
    document.getElementById('ap_password').value = account.password;
    document.getElementById('ap_password_check').value = account.repeat;
    document.getElementById('continue').click();
})(${account});