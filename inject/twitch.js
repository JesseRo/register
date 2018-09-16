(function() {
    var buttons = document.getElementsByTagName("button");

    for (var i in buttons) {
        if (buttons[i].attributes) {
            if (buttons[i].attributes['data-a-target']) {
                if (buttons[i].attributes['data-a-target'].value === "signup-button") {
                    buttons[i].click();
                    return
                }
            }
        }
    }
    window.location.href = 'https://twitch.amazon.com/link?confirm=ALWAYS&locale=en-US&returnUri=https%3A%2F%2Ftwitch.amazon.com%2Fprime%2Fsignup%2Fus%3FdiscoveryLocation%3Dsm_w_tup_ntp_t_c%26locale%3Den-US&tv=eyJraWQiOiJjb20uYW1hem9uLnJlc3Bhd24uc3RvcmUud2Vic2l0ZS5rZXlzLmp3dC5wcm9kO0NyZWRlbnRpYWw7MSIsImFsZyI6IkhTNTEyIn0.eyJpYXQiOjE1MzcwOTU0MDYsInN1YiI6IkFWSVcwVjZTSUE3RFciLCJ0aWQiOiIyNTkxNjk4NjQiLCJuYW1lIjoiZmRnZHNhaGoiLCJhY2NvdW50VHlwZSI6InVzZXIiLCJzZXNzaW9uIjoiMTMxLTg0MTg0MTEtNzQ3MzIyMCIsImV4cCI6MTUzNzA5NjMwNn0.-S6FRvPi3-AJlwBYMZLKU3Wte6Ga5PnfhR8PJY818gU1-ZE-cwM7Lr25_j0PhJfCMM8oPEFmRt64fa_WYqmv4Q';
})();