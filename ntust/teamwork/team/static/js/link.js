var strUrl = location.search;
var getSearch, sp;
// var getPara, ParaVal;
// var aryPara = [];

if (strUrl.indexOf("?") != -1) {
	getSearch = strUrl.split("?");
	sp ='&' + getSearch[1];
	// getPara = getSearch[1].split("&");
	// for (i = 0; i < getPara.length; i++) {
	//   ParaVal = getPara[i].split("=");
	//   aryPara.push(ParaVal[0]);
	//   aryPara[ParaVal[0]] = ParaVal[1];
	// }
	// alert(aryPara);
}else{
	sp="";
}

function splink(good){
	var url = 'http://www.wow-woman.com.tw/product/goods_detail.php?goods_id=' + good + sp;
	console.log(url);
	window.open(url,"_blank");
	
	
	
	
	

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
}