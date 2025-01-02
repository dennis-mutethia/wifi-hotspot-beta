$('.notice').html('');
document.stk.phone.focus();
document.stk.phone.value = sessionStorage.getItem("phone");

document.stk.phone.onkeyup = function() {   
    sessionStorage.setItem("phone",document.stk.phone.value);
};

function setAmount(amt){
    document.stk.amount.value = amt;
    sessionStorage.setItem("amount",amt);
}

function connect(){    
    let phone = document.stk.phone.value.trim();
    if(phone.length===10){
        $('.notice').html('');
        document.sendin.username.value = phone;
        document.sendin.password.value = phone;
        document.sendin.submit();
    }else $('.notice').html('Enter Valid Phone Number');
    
    return false;
}
function connect2(){
    let phone = $('#account').val();
    if(phone.length===10){
        $('.notice').html('');
        document.sendin.username.value = phone;
        document.sendin.password.value = phone;
        document.sendin.submit();
    }else $('.notice').html('Enter Valid Phone Number');

    return false;
}

function connect3(){
    let phone = $('#adphone').val();
    if(phone.length===10){
        $('.notice').html('');
        document.sendin.username.value = phone;
        document.sendin.password.value = phone;
        document.sendin.submit();
    }else $('.notice').html('Enter Valid Phone Number');
    
    return false;
}

function sendPush(phone, amount, pushed){
    let url = 'http://multiplespacetechnologies.com/admin/kanyonton/push.php';
    $.post(url,
    {
        phone: '254' + phone,
        amount: amount,        
        account: phone
    },
    function(data, status){
        sessionStorage.setItem("pushed", pushed);
        connect();
    });
}

var submit = function(event) {
    event.preventDefault();
    phone = sessionStorage.getItem("phone").slice(-9)
    amount = sessionStorage.getItem("amount")
    sendPush(phone, amount, 1)
};

function connectDefault(){
    let phone = sessionStorage.getItem("phone").slice(-9)
    let amount = sessionStorage.getItem("amount") !==null ? sessionStorage.getItem("amount") : 20;

    if(!sessionStorage.getItem("pushed")) 
        connect();
    else
        sendPush(phone, amount, 0)
}

var form = document.getElementById("stk");
form.addEventListener("submit", submit, true);

var ad_video = document.getElementById("ad_video");
ad_video.addEventListener("click", () => {
  ad_video.play();
}, { once: true });
document.getElementById("watchad").addEventListener("click", () => {
  ad_video.play();
}, { once: true });
ad_video.onended = function() {
    document.getElementById("adconnectbutton").style.visibility = 'visible';
    document.getElementById("notice2").style.visibility = 'hidden';
};

var adphone = document.getElementById("adphone");
var notice = document.getElementById("notice");
adphone.onkeyup = function() {
    let phone = adphone.value.trim();
    if(phone.length===10){
        notice.innerHTML = ('');
        let url = 'http://multiplespacetechnologies.com/admin/kanyonton/ad.php';
        $.post(url,
        {
            phone: phone,
            amount: 0,        
            account: phone
        },
        function(data, status){
            
        });
    }else notice.innerHTML = ('Enter Valid Phone Number');
};
