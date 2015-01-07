var th = false;
// 单元格转化成文本框 
function changeTotext(obj) { 
    var tdValue = obj.innerText; 
    obj.innerText = ""; 
    var txt = document.createElement("input"); 
    txt.type = "text"; 
    txt.value = tdValue; 
    txt.id = "_text_"; 
    txt.setAttribute("className","text"); 
    obj.appendChild(txt); 
    txt.select();
} 


function cancel(obj) { 
    var txtValue = document.getElementById("_text_").value; 
    obj.innerText = txtValue;
    if (th == true) 
        $.post("/edit", {data: txtValue, row: row, column: col}, function(){});                               //  post !!!!!!!!!!!!!!!!!!!!!!!!! 
    else {
        $.post("#", {value: txtValue}, function(){});
    }
} 


document.onclick = function() { 
    if (event.srcElement.tagName.toLowerCase() == "th") { 
        th = true;
        row = event.srcElement.parentNode.rowIndex;
        col = event.srcElement.cellIndex;
        changeTotext(event.srcElement); 
    } else if (event.srcElement.tagName.toLowerCase() == "h2"){
        th = false;
        changeTotext(event.srcElement);
    }
     
} 
document.onmouseup = function() { 
    if (document.getElementById("_text_") && event.srcElement.id != "_text_") 
    { 
        var obj = document.getElementById("_text_").parentElement; 
        cancel(obj); 

    } 
} 

