document.addEventListener('DOMContentLoaded', () => {

    document.querySelector('#keysForm').onsubmit = () => {

        // Initialize new request
        const request = new XMLHttpRequest();
        // const newChannel = document.querySelector('#newChannel').value;
        // const userName = document.querySelector('#userName').value;

        request.open('POST', '/generate_keys');

        // Callback function for when request completes
        request.onload = () => {
            if(request.status ===200){
                // Extract JSON data from request
                const data = JSON.parse(request.responseText);
                // Update the result div
                if (data.success) {
                    const private_key = data.private_key;
                    const public_key = data.public_key;
                    document.querySelector('#result').innerHTML = 'Keys generated successfuly.';
                    document.querySelector('#private_key').innerHTML = `private key: ${private_key}`;
                    document.querySelector('#public_key').innerHTML =  `public  key: ${public_key}`;

                } else {
                    document.querySelector('#result').innerHTML = 'Try another name.';
                }
            } else{
                console.error('Request failed with status:', request.status);
            }
        };
        // Add data to send with request
        request.send();
        return false;
    };


});
