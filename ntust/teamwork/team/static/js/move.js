
var strUrl=location.search;var getSearch,sp;if(strUrl.indexOf("?")!=-1){getSearch=strUrl.split("?");sp='&'+getSearch[1];}else{sp="";}function splink(good){var url='http://www.wow-woman.com.tw/product/goods_detail.php?goods_id='+good+sp;console.log(url);window.open(url,"_blank");}
//alert('isIE11');



//超麻煩循環動畫  泡泡動畫
function A2()
{
	
TweenMax.to($("#slideShow1"), 0, {css:{opacity:1},ease:Expo.easeNone, delay:3, onComplete:B2});
TweenMax.to($("#slideShow2"), 0, {css:{opacity:0},ease:Expo.easeNone});
//alert('isIE11');

}

function B2(){
	
TweenMax.to($("#slideShow1"),0, {css:{opacity:0},ease:Expo.easeNone, delay:3, onComplete:C2});
TweenMax.to($("#slideShow2"), 0, {css:{opacity:0},ease:Expo.easeNone});
//alert('isIE12');

	}		
	
function C2(){
	
TweenMax.to($("#slideShow1"),0, {css:{opacity:0},ease:Expo.easeNone, delay:3, onComplete:A2});
TweenMax.to($("#slideShow2"), 0, {css:{opacity:1},ease:Expo.easeNone});
//alert('isIE13');

	}	
A2();

//超麻煩循環動畫END



//超麻煩循環動畫  泡泡動畫
function _A2()
{
	
TweenMax.to($("#main03_obj"), 1, {css:{top:2446},ease:Expo.easeNone, delay:0});

TweenMax.to($("#main01-obj"), 1, {css:{top:49},ease:Expo.easeNone, delay:0, onComplete:_B2});

}

function _B2(){
	
TweenMax.to($("#main01-obj"),1, {css:{top:44},ease:Expo.easeNone, delay:0, onComplete:_A2})	;
TweenMax.to($("#main03_obj"), 1, {css:{top:2456},ease:Expo.easeNone, delay:0});

	}						
_A2();

//超麻煩循環動畫END



//gotoTop btn


var Z = 0;

function pro1(){  
$("#pro_01").css({ opacity: 0 });
Z=1;

}

function pro2(){  




$("#pro_01").css({ opacity: 1 });
Z=0;
}

function whichOne(){
	
	if(Z==1){splink(517) }
	if(Z==0){splink(519) }
	
	}



function unit1(){  
   jQuery("html,body").animate({scrollTop:700},1000);
   }
   
 function unit2(){  
   jQuery("html,body").animate({scrollTop:2460},1000);
   }