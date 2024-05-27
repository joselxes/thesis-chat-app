function xorEncryptDecrypt(message,keyString){
    let key = Array.from(keyString);
    let output =[];
    for (let i=0; i<message.length; i++){
        let charCode = message.charCodeAt(i) ^ key[i % key.length].charCodeAt(0) 
        output.push(String.fromCharCode(charCode));
    }
    return output.join("");
}

function getCurrentTime() {
    const currentDate = new Date();
    const year = currentDate.getFullYear();
    const month = (currentDate.getMonth() + 1).toString().padStart(2, '0');
    const day = currentDate.getDate().toString().padStart(2, '0');
    const hours = currentDate.getHours().toString().padStart(2, '0');
    const minutes = currentDate.getMinutes().toString().padStart(2, '0');
    const seconds = currentDate.getSeconds().toString().padStart(2, '0');
    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
  }
  function changeColor(user) {
    // select a user
    var h1 = document.getElementById("signedUser");
    var currentUser = h1.innerHTML;

    // Select the <ul> element
    var ul = document.getElementById("messages");

    // Select all <li> elements within the <ul>
    var liElements = ul.querySelectorAll("li");

    // Loop through each <li> element
    liElements.forEach(function(liElement) {
        // Select the <span> element inside the <li>
        var spanElement = liElement.querySelector("span.time-right");

        // Get the text content of the <span> element
        var spanTextContent = spanElement.textContent;

        // Check if the spanTextContent includes currentUser
        if (spanTextContent.includes(user)) {
            // Select the <div> element inside the <li>
            var divElement = liElement.querySelector("div.mensajes");

            // Add a class to the selected <div> element
            divElement.classList.add("darker");
        }
        else{
            // Select the <div> element inside the <li>
            var divElement = liElement.querySelector("div.mensajes");

            // Add a class to the selected <div> element
            divElement.classList.add("clear");            
        }
    });
}

  

document.addEventListener('DOMContentLoaded', () => {
    var vara=null;
    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    // document.querySelector('#yes').disabled = true;
    // document.querySelector('#task').onkeyup = ()=>{
    //
    // }
//
    // When connected, configure buttons
    socket.on('connect', () => {
        if(document.querySelector('#forma')!==null) {
            // Each button should emit a "submit vote" event
            document.querySelector('#forma').onsubmit = () => {
                // const request = new XMLHttpRequest();
                const content = document.querySelector('#mensaje').value;
                
                const username = document.querySelector('#yes').dataset.user;
                const channelid = document.querySelector('#yes').dataset.channelid;
                const cipherContent =xorEncryptDecrypt( content,sessionStorage.getItem(channelid));

                const currentTime = getCurrentTime();

                // const nombreCanal = document.querySelector('#nombreCanal').innerHTML;
                vara=channelid;
                socket.emit('submit mss', {'channelid':channelid,
                'content': cipherContent,
                'username':username,
                'currentTime':currentTime});
 

                return false;
            };
        }
    });

    // When a new vote is announced, add to the unordered list
    socket.on('announce mensaje', data => {
        const li = document.createElement('li');
        const div =document.createElement('div');
        const p =document.createElement('p');
        const span =document.createElement('span');
        const img =document.createElement('img');
        p.setAttribute('type', 'sub');
        p.setAttribute('name', 'btn');

        
        div.classList.add('mensajes');

        span.classList.add('time-right');
        div.appendChild(img);
        div.appendChild(p);
        div.appendChild(span);    
        li.appendChild(div)

        if (vara==`${data.newMessage.channelid}`){

            const decipherContent =xorEncryptDecrypt(data.newMessage.content ,sessionStorage.getItem(data.newMessage.channelid));
            // console.log(data.newMessage.channelid)
            // console.log(typeof(data.newMessage.channelid))
            // console.log(sessionStorage.getItem(data.newMessage.channelid))
            // console.log(typeof(sessionStorage.getItem(data.newMessage.channelid)))
            // console.log(data.newMessage.content)
            // console.log(typeof(data.newMessage.content))
            // console.log(xorEncryptDecrypt(data.newMessage.content ,sessionStorage.getItem(data.newMessage.channelid)))
            // console.log(type(xorEncryptDecrypt(data.newMessage.content ,sessionStorage.getItem(data.newMessage.channelid))))
            p.textContent = `${data.newMessage.content}`;
            p.textContent = decipherContent;
            // p.textContent = `${data.newMessage.content}`;
            span.textContent = `${data.newMessage.currentTime} by ${data.newMessage.username}`;
            var h1 = document.getElementById("signedUser");
            var currentUser = h1.innerHTML;
            if (currentUser.includes(data.newMessage.username)) {
                console.log('verdaderpo')
                li.classList.add("darker");            
                img.src='/static/imagenes/bandmember.jpg';
            }
            else{
                li.classList.add("clear");
                img.src='/static/imagenes/avatar_g2.jpg';
            }
            document.querySelector('#messages').append(li);
            document.querySelector('#mensaje').value="";

        }
    

    });
    

});

