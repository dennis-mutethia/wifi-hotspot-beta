var base = 'http://185.203.117.51';
var site = 'nairobi';
var station = 'muthiga_inn';
var videoCount = 3;
var imageCount = 10;
var account = 0;
var adphone = document.getElementById("adphone");
var notice = document.getElementById("notice");
var notice2 = document.getElementById("notice2");
var adconnect = document.getElementById("adconnectbutton");
var advideo = document.getElementById("advideo");
var source = document.createElement('source');
advideo.appendChild(source);
setVideo();
setImages();

//adconnect.style.visibility = 'visible';
document.onclick = function() { 
    advideo.play();    
};

function setVideo(){
    let max = videoCount - 1;
    let pos = Math.floor(Math.random() * (max + 1));
    let src = 'content/vid_'+pos+'.mp4';
    source.setAttribute('src', src);
    source.setAttribute('type', 'video/mp4');
    advideo.load();
    setTimeout(function(){
        adconnect.style.visibility = 'visible';
        notice2.style.visibility = 'hidden';
        connect();
    }, 30000);    
}

function setImages(){
    let max = imageCount - 5;
    let i = Math.floor(Math.random() * (max + 1));
    
    for(let j=0;j<5;j++){
        let src = 'content/img_'+(i+j)+'.jpg';        
        document.getElementById("img"+j).src = src;
        document.getElementById("img"+j).alt = src;
    }    
}

function connect(){
    let phone = adphone.value.trim();
    if(phone.length===10){
       // phone = Math.floor(Math.random() * 1000);// '0723111920';
       // let account = '254'+phone.slice(-9);
        // let account = Math.floor(Math.random() * 1000);
        document.sendin.username.value = account;
        document.sendin.password.value = account;
        setTimeout(function(){
            document.sendin.submit();
        }, 2000);
    }else notice.innerHTML = ('Enter Valid Phone Number');
    return false;
}

adphone.onkeyup = function() {
    let phone = adphone.value.trim();
    if(phone.length===10){
        notice.innerHTML = ('');
        let url = base+':8080/add';
        $.post(url,{
            phone: '254'+phone.slice(-9),
            site: site,
            station: station
        },
        function(data, status){    
            account = data;
        });
    }else notice.innerHTML = ('Enter Valid Phone Number');
};
