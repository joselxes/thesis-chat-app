document.addEventListener('DOMContentLoaded', () => {

    // Select all forms with id 'newPriv'
    const forms = document.querySelectorAll('#newPriv');

    // Loop through each form and attach event listener
    forms.forEach(form => {
        form.onsubmit = (event) => {

            event.preventDefault(); // Prevent the form from submitting
            
            // Initialize new request
            const request = new XMLHttpRequest();

            // Get the value of the newChannel input within the form
            const newChannel = form.querySelector('#newChannel').value;

            // Open the request
            request.open('POST', '/newPriv');

            // Callback function for when request completes
            request.onload = () => {
                // Handle response data
                
                // Extract JSON data from request
                const data = JSON.parse(request.responseText);

                // Update the result div
                if (data.success) {
                    var liRemove=form.parentElement;
                    liRemove.remove(); 
                    console.log("data.idChannelaaaaaaaaaaaaaaaaaaaaa")
                    console.log(data.idChannel)
                    console.log(typeof(data.idChannel))
                    const channel = `${data.idChannel}`
                    const toUser = `${data.toUser}`
                    // el creador del canal guarda la clave, 
                    // key se forjo con la clave publica del invitado
                    sessionStorage.setItem(channel,data.key)

                    const li = document.createElement('li');
                    const forma = document.createElement('form');
                    const boton = document.createElement('button');
                    boton.classList.add("chat-btn");
                    li.appendChild(forma);
                    forma.appendChild(boton);
                    forma.action='/chatList/'+channel+'';
                    boton.innerHTML = `${toUser}`;
                    document.querySelector('#oldChats').append(li);
                    // document.querySelector('#newChannel').value="";
                    document.querySelector('#result').innerHTML = 'successful.';

                }
                else {
                    document.querySelector('#result').innerHTML = 'Try another name.';
                }
            };

            // Add data to send with request
            const data = new FormData();
            data.append('newChannel', newChannel);
            // Send request
            request.send(data);

            return false;
        };
    });
});



