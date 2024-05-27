document.addEventListener('DOMContentLoaded', () => {
    var currentUrl = window.location.href;
    var parts = currentUrl.split('/');
    var chatIdSession= parts[parts.length - 1].substring(0,10);


    // Send a request to generate the shared key
    const request = new XMLHttpRequest();
    console.log("ErrorAQUI",chatIdSession)
    if (sessionStorage.getItem(chatIdSession)===null){
        request.open('POST', '/generate_shared_key');
        request.setRequestHeader('Content-Type', 'application/json'); // Set proper content type

        request.onload = () => {
            if (request.status === 200) {
                const data = JSON.parse(request.responseText);
                if (data.shared_key) {
                    // Save the shared key in sessionStorage
                    sessionStorage.setItem(chatIdSession, data.shared_key);
                    document.querySelector('#result').innerHTML = 'Shared key generated successfully.';
                } else {
                    document.querySelector('#result').innerHTML = data.message;
                }
            } else {
                document.querySelector('#result').innerHTML = data.message;
                console.error('Request failed with status:', request.status);
            }
        };

        // Prepare data to send with the request
        const data = JSON.stringify({
            private_key: sessionStorage.getItem('private_key'),
            chatIdSession: chatIdSession
        });

        // Send the request
        request.send(data);}
    
});

// ------------------------------------------------

// document.addEventListener('DOMContentLoaded', () => {
//     var currentUrl = window.location.href;
//     // Split the URL by '/' characters
//     var parts = currentUrl.split('/');

//     // Get the last part of the URL
//     var chatIdSession= parts[parts.length - 1];

//     // Check if the variable exists in sessionStorage
//     if (sessionStorage.getItem(chatIdSession) !== null) {
//         // The variable exists in sessionStorage
//         document.querySelector('#result').innerHTML = 'You do have the shared key.';

//     } else {
//         // The variable does not exist in sessionStorage
//         document.querySelector('#result').innerHTML = 'You do not have your shared key.';

//         const request = new XMLHttpRequest();
//         request.open('POST', '/generate_shared_key');
//         // Callback function for when request completes
//         request.onload = () => {
//             // Extract JSON data from request
//             const data = JSON.parse(request.responseText);
//             // Update the result div
//             if (data.success) {
//                 sessionStorage.setItem(chatIdSession, data.shared_key);
//                 setTimeout(function() {    
//                     document.querySelector('#result').innerHTML = 'Shared key generated successfuly.';
//                 }, 500);

//             } else {
//                 document.querySelector('#result').innerHTML = 'An unexpected error.';
//             }

//         }

//         // Add data to send with request
//         const data = new FormData();
//         data.append('private_key', sessionStorage.getItem('private_key'));
//         data.append('receiver', chatIdSession);
//         // Add data to send with request
//         request.send(data);
//         return true;
//     }
// });
// // ----------------------------------------------