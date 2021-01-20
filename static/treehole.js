var isIe=(document.all)?true:false;

//设置select的可见状态
function setSelectState(state)
{
	var objl=document.getElementsByTagName('select');
	for(var i=0;i<objl.length;i++){
		objl[i].style.visibility=state;
	}
}
/*/*************************************************************AJAX 初始化一个xmlhttp对象
function InitAjax()
{
	var ajax=false;
	try {
		ajax = new ActiveXObject("Msxml2.XMLHTTP");
	} catch (e) {
		try {
			ajax = new ActiveXObject("Microsoft.XMLHTTP");
		} catch (E) {
			ajax = false;
		}
	}
	if (!ajax && typeof XMLHttpRequest!='undefined') {
		ajax = new XMLHttpRequest();
	}
	return ajax;
}*/
function vote(id) {
    document.getElementById("vote-"+id).innerHTML=Number(document.getElementById("vote-"+id).innerHTML)+1;
    var img = new Image(); 
	img.src='//shudong.21du.cn/vote/'+id;
}
function kui() {
    var id=document.getElementById("Number").value;
    //var reg=/^[1-9]+[0-9]*$/;
    //reg.test(id)
	if(id){
        window.location.href="/view/" + id";
        //window.location.href="//www.baidu.com/s?wd=" + encodeURIComponent(id) + "%20site%3Ashudong.21du.cn";
		return false;
    }
	window.location.href="//shudong.21du.cn/kui";
}



function sysadmin(ac,id) {
    document.getElementById("info").innerHTML=ac+"执行成功):";
    var img = new Image(); 
	img.src='//shudong.21du.cn/'+ac+'/'+id;
}
