/*
#	mpsk
#	Beijing University of Technology
#	Copyright 2017
*/

var static_path = "static/"

//  当前设置点
var current_point = 0;
var cords = new Array(
    Array(-1, -1),    //  leye
    Array(-1, -1),    //  reye
    Array(-1, -1),    //  nose
    Array(-1, -1),    //  lmth
    Array(-1, -1)     //  rmth
);

function setsvgHW(id) 
{
    var w = 0;
    var h = 0;
    // 具有较好的通用性
    var real = document.getElementById(id).height || document.getElementById(id).style.height || document.getElementById(id).offsetHeight;
    h = parseInt(real);
    real = document.getElementById(id).width || document.getElementById(id).style.width || document.getElementById(id).offsetWidth;
    w = parseInt(real);
    document.getElementById("asvg").style.width = w;
    document.getElementById("asvg").style.height = h;
}

function hotkeys(keychar)
{
    if(!isNaN(parseInt(keychar,6)))
    {
        if(keychar=='0')
        {
            current_point = 0;
            alert("current point is cleared!");
        }
        current_point = parseInt(keychar, 6);
        //alert(current_point + " is selected!");
        return true;
    }
    switch(keychar)
    {
        case 'C':
        {
            current_point = 0;
            alert("current point is cleared!");
            return true;
        }
        case 'H':
        {
            //  next
            window.location.href = '/help';
            return true;
        }
        case 'B':
        {
            //  barely see
            window.location.href = '';
            return true;
        }
        case 'N':
        {
            //  next
            window.location.href = '';
            return true;
        }
        case ' ':
        {
            //  confirm
            buildSubmit();
            document.getElementById("anno_sub").submit();
            return true;
        }
        case '\r':
        case '\n':
        {
            //  confirm
            buildSubmit();
            document.getElementById("anno_sub").submit();
            return true;
        }
    }
}

//  组装POST
function buildSubmit()
{
    var _str = "";
    for(var i=0; i<cords.length; i++)
    {
        _str += " " + cords[i][0];
        _str += " " + cords[i][1];
    }
    document.getElementById("ctext").value = _str;
    document.getElementById("cname").value = document.getElementById("ranimg").src;
}

//  窗体载入事件
window.onload = function () 
{
    document.getElementById("ahldr").onclick = function (e) {
        //  初始化值
        var e = e || window.event;
        //  鼠标点的坐标
        var scrollX = document.documentElement.scrollLeft || document.body.scrollLeft;
        var scrollY = document.documentElement.scrollTop || document.body.scrollTop;
        var x = e.pageX || e.clientX + scrollX;
        var y = e.pageY || e.clientY + scrollY;
        //  得到具体点
        y = y - 60;
        if(current_point<0 || current_point>5)
        {
            alert("非法输入！");
        }
        else{
            cords[current_point-1][0] = x;
            cords[current_point-1][1] = y;
        }
    }
    //  initiate coords
    setsvgHW("ranimg");
}

//  文档载入
document.onkeydown = function()
{
    var x;
	if(window.event) // IE8 及更早IE版本
	{
		x=event.keyCode;
	}
	else if(event.which) // IE9/Firefox/Chrome/Opera/Safari
	{
		x=event.which;
	}
    keychar=String.fromCharCode(x);
    if(!hotkeys(keychar))
    {
        //  tips
    }
}