function closeMessage(e){
    var target;
    if(!e){
        e = window.event;
    }
    target = e.target || e.scrElement;
    var message = document.querySelector('ul.message');
    message.id = 'close_message';
}

var closeLink = document.querySelector('a.close');
if(closeLink.addEventListener){
    closeLink.addEventListener("click",function(e){
        closeMessage(e);
    },false);
}
else {
    closeLink.attachEvent("onclick",function(e){
        closeMessage(e);
    })
}