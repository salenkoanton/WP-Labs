var name = false;
var author = false;
var file = false;
var text = false;
function checkButton(){
    btn = document.getElementById("submit-btn");
    if (name && author && file)
    {
        btn.removeAttribute("disabled");
    }
    else btn.setAttribute("disabled", true);
}
function nameValidator(){
    inp = document.getElementById("name-input");
    val = inp.value;
    if (val.length == 0){
        name = false;
        inp.setAttribute("placeholder", "Please enter name");
        inp.setAttribute("style", "border-color: #f55");
    }
    else{
        name = true;
        inp.setAttribute("style", "border-color: #af8");
    }
    checkButton();
}
function authorValidator(){
    inp = document.getElementById("author-input");
    val = inp.value;
    if (val.length == 0){
        author = false;
        inp.setAttribute("placeholder", "Please enter author name");
        inp.setAttribute("style", "border-color: #f55");
    }

    else{
        author = true;
        inp.setAttribute("style", "border-color: #af8");
    }
    checkButton();
}
function fileValidator(){
    inp = document.getElementById("file-input");
    val = inp.value;
    if (val.length == 0){
        file = false;
        inp.setAttribute("placeholder", "Please attach audio");
        inp.setAttribute("style", "border-color: #f55");
    }
    else{
        file = true;
    }
    checkButton();
}
/*
function textValidator(){
    inp = document.getElementById("name-input");
    val = inp.value;
    if (val.length == 0){
        name = false;
        inp.setAttribute("placeholder", "Please enter author name");
        inp.setAttribute("style", "background: #fbb");
    }

    else{
        name = false;
        inp.setAttribute("style", "background: #af8");
    }
}*/
document.getElementById("name-input").onchange = nameValidator;

document.getElementById("author-input").onchange = authorValidator;

document.getElementById("file-input").onchange = fileValidator;


