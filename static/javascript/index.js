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
    data = t_div.innerHTML;
    $.post("/edit", {value: txtValue, row: row, col: col, data: data}, function(){}); 

} 


document.onclick = function() { 
    if (event.srcElement.tagName.toLowerCase() == "th") { 
        row = event.srcElement.parentNode.rowIndex;
        var clas = event.srcElement.className;
        if (clas == "classes") col = 0;
        if (clas == "time") col = 1;
        if (clas == "day") col = 2;
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

 window.onload = function() {
    function time(){
        t_div = document.getElementById('showtime');
        var now=new Date()
        /*t_div.innerHTML = now.getFullYear()+"-"+(now.getMonth()+1)+"-"+now.getDate();*/
        if ((now.getMonth() + 1) < 10) {
            t_div.innerHTML = "0" + (now.getMonth()+1) + "-";
        } else {
            t_div.innerHTML = (now.getMonth()+1) + "-";
        }
        if (now.getDate() < 10) {
            t_div.innerHTML = t_div.innerHTML +"0" +  now.getDate();
        } else {
            t_div.innerHTML = t_div.innerHTML +  now.getDate();
        }

        setTimeout(time,1000);
    }
    time();
    oks = document.getElementsByClassName("ok");
    trs =document.getElementsByTagName("tr");
    for (var i = 0; i < 9; i++) {
        oks[i].addEventListener('click', function(event) {
            for (var j = 1; j < 10; j++) {
                trs[j].style.display = "none";
            }
            end = document.getElementById("end");
            end.style.display = "block";
            var srow = event.currentTarget.parentNode.parentNode.rowIndex;
            $("#end form:first-child").attr("action", "/submit" + "/" + srow)
        });
    }


 }