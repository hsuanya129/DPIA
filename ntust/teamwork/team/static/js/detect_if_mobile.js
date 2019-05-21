
//Âà§}code
function detectmob() {

if( navigator.userAgent.match(/Android/i)
|| navigator.userAgent.match(/webOS/i)
|| navigator.userAgent.match(/iPhone/i)
|| navigator.userAgent.match(/iPad/i)
|| navigator.userAgent.match(/iPod/i)
|| navigator.userAgent.match(/BlackBerry/i)
|| navigator.userAgent.match(/Windows Phone/i)
){
   // return mobile  true;
     document.location.href="mobile/";
    
  }
else {
   // return   mobile  false;
     // 
  }
}

detectmob();
