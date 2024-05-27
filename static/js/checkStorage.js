document.addEventListener('DOMContentLoaded', () => {
    // Check if the variable exists in sessionStorage,if exists send to the server
//     if (sessionStorage.getItem('public_key') !== null) {
//         console.log(1,"if")
//         // The variable exists in sessionStorage
//         document.querySelector('#result').innerHTML = 'You have your keys.';
//         const public_key  = sessionStorage.getItem('public_key');
//         const private_key = sessionStorage.getItem('private_key');

//         // check if the variable does not exist in the server
//         // Send a request to generate the shared key
//         const request = new XMLHttpRequest();
//         request.open('POST', '/generate_keys');
//         request.setRequestHeader('Content-Type', 'application/json'); // Set proper content type
//         request.onload = () => {
//             if (request.status === 200) {
//                 const data = JSON.parse(request.responseText);
//                 if (data.success) {
//                     // Save the shared key in sessionStorage
//                     document.querySelector('#result').innerHTML = 'Keys loaded successfully.';
//                 } else {
//                     document.querySelector('#result').innerHTML = 'Keys have not loaded successfully.';
//                 }
//             } else {
//                 document.querySelector('#result').innerHTML = 'Keys have not loaded successfully.';
//                 console.error('Request failed with status:', request.status);
//             }
//         };

//         // Prepare data to send with the request
//         const data = JSON.stringify({
//             private_key: sessionStorage.getItem('private_key'),
//             public_key: sessionStorage.getItem('public_key'),
//         });
//         // Send the request
//         request.send(data);
        
// // if you don have your keys
//     } else {
    console.log("primerif")
    // The variable does not exist in sessionStorage
    // document.querySelector('#result').innerHTML = 'You do not have your keys.';
    console.log("1")
    const request = new XMLHttpRequest();
    console.log("2")
    request.open('POST', '/generate_keys');
    // Callback function for when request completes
    console.log("3")
    request.onload = () => {
        if(request.status ===200){
            // Extract JSON data from request
            const data = JSON.parse(request.responseText);
            // Update the result div
            if (data.success) {
                sessionStorage.setItem('public_key', data.public_key);
                sessionStorage.setItem('private_key', data.private_key);
                // sessionStorage.setItem('userData', JSON.stringify(userData));
                setTimeout(function() {    
                    document.querySelector('#result').innerHTML = 'Keys generated successfuly.';
                }, 500); 

            } else {
                document.querySelector('#result').innerHTML = 'An unexpected error.';
            }
        } else{
            console.error('Request failed with status:', request.status);
        }
    };
    // Add data to send with request
    request.send();
    // }

    document.querySelector('#closeSession-btn').onsubmit = () => {
        
        // Clear all saved data from sessionStorage
        sessionStorage.clear();
        return true;
    };



});
