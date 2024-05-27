function xorEncryptDecrypt(message,keyString){
  let key = Array.from(keyString);
  let output =[];
  for (let i=0; i<message,length; i++){
      let charCode = message.charCodeAt(i) ^ key[i % key.length].charCodeAt(0) 
      output.push(String.fromCharCode(charCode));
  }
  return output.join("");
}

document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    // document.querySelector('#yes').disabled = true;
    // document.querySelector('#task').onkeyup = ()=>{
    //
    // }
//
    // When connected, configure buttons
    socket.on('connect', () => {

        // Each button should emit a "submit vote" event
        document.querySelector('#canalForma').onsubmit = () => {
                // const request = new XMLHttpRequest();
                const newChannel = document.querySelector('#newChannel').value;
                socket.emit('submit newChannel', {'newChannel': newChannel});
                return false;
            };

    });

    // When a new vote is announced, add to the unordered list
    socket.on('announce newChannel', data => {
        const flag= `${data.success}`;
        alert(flag);
        if (data["success"] === 0) {
          const li = document.createElement('button');
          li.innerHTML = `${data.success}: ${data.newChannel}`;
        } else {
          const li = document.createElement('button');
          li.innerHTML = `${data.success}: jajaja`;
        }
        // const li = document.createElement('button');
        // li.innerHTML = `${data.success}: ${data.newChannel}`;
        document.querySelector('#canales').append(li);
        document.querySelector('#newChannel').value="";
    });
});
