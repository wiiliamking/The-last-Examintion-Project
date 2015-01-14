 window.onload = function() {
    oks = document.getElementsByClassName("ok");
    /*trs =document.getElementsByTagName("tr");*/
    // for (var i = 0; i < 9; i++) {
    //     oks[i].addEventListener('click', function() {
    //         for (var j = 0; j < 10; j++) {
    //             trs[j].style.display = "none";
    //         }
    //         end = document.getElementById("end");
    //         end.style.display = "block";
    //     });
    // }
    // document.getElementsByClassName("back").addEventListener('click', function() {
    // })
    console.log(document.getElementById("change"));
    document.onclick=function() {
        if (event.srcElement.id == "hid") {
            $("#more").removeClass("hidden");
            event.srcElement.className = event.srcElement.className + " hidden";
        }
        if (event.srcElement.className == "ok") {
            var num = parseInt(event.srcElement.id.split('-')[1]);
            $($("#detail").children()[num]).removeClass("hidden");
        }
        if (event.srcElement.className == "back") {
            $(event.srcElement.parentNode).addClass("hidden");
        }
    }
 }