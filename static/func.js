/*
#	mpsk
#	Beijing University of Technology
#	Copyright 2017
*/

var static_path = "static/"
//  当前点

window.onload=function(){
    document.getElementById("ah_1").onclick = function(e) {
        //  初始化值
        var e = e || window.event;
        //  鼠标点的坐标
        var scrollX = document.documentElement.scrollLeft || document.body.scrollLeft;
        var scrollY = document.documentElement.scrollTop || document.body.scrollTop;
        var x = e.pageX || e.clientX + scrollX;
        var y = e.pageY || e.clientY + scrollY;
        //  阻止浏览器默认事件

        alert("x\t"+x+"\ny\t"+y);
    }

}
