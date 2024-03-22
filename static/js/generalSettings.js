var developement_mode = true;
var disableEditing = true; 


window.onload = function() {

    if (disableEditing) {
        document.body.classList.add("disable-edit");
    } else {
        document.body.classList.remove("disable-edit");
    }
};