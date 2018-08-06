var buttons = document.getElementsByTagName("button");
for (var i in buttons){
    if (buttons[i].attributes){
        if (buttons[i].attributes['data-a-target']){
            if(buttons[i].attributes['data-a-target'].value === "signup-button"){
                buttons[i].click();
            }
        }
    }
}