document.addEventListener('DOMContentLoaded', () => {
    if(document.querySelector('#canalForma')!==null){ 
        document.querySelector('#canalForma').onsubmit = () => {

            // Initialize new request
            const request = new XMLHttpRequest();
            const newChannel = document.querySelector('#newChannel').value;
            // const userName = document.querySelector('#userName').value;

            request.open('POST', '/newChannels');

            // Callback function for when request completes
            request.onload = () => {

                // Extract JSON data from request
                const data = JSON.parse(request.responseText);

                // Update the result div
                if (data.success) {
                    const channel = `${data.newChannel}`
                    const li = document.createElement('li');
                    const forma = document.createElement('form');
                    const boton = document.createElement('button');
                    li.appendChild(forma);
                    forma.appendChild(boton);
                    forma.action='/chatList/'+channel+'';
                    boton.innerHTML = `${channel}`;
                    document.querySelector('#canales').append(li);
                    document.querySelector('#newChannel').value="";
                    document.querySelector('#result').innerHTML = 'successful.';

                }
                else {
                    document.querySelector('#result').innerHTML = 'Try another name.';
                }
            }

            // Add data to send with request
            const data = new FormData();
            data.append('newChannel', newChannel);
            // data.append('userName', userName);
            // Send request
            request.send(data);
            return false;
        };
    }    
});
