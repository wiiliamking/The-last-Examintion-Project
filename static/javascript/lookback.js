 window.onload = function() {
    oks = document.getElementsByClassName("ok");
    /*trs =document.getElementsByTagName("tr");*/
    for (var i = 0; i < 9; i++) {
        oks[i].addEventListener('click', function() {
            /*for (var j = 0; j < 10; j++) {
                trs[j].style.display = "none";
            }
            end = document.getElementById("end");
            end.style.display = "block";*/
        });
    }
    /*document.getElementById("goback").addEventListener('click', function() {
        for (var j = 0; j < 10; j++) {
                trs[j].style.display = "block";
            }
            end = document.getElementById("end");
            end.style.display = "none";
    })*/

 }