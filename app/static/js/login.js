var baseUrl = 'http://18.213.17.243:8081'

document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');

    form.addEventListener('submit', async function (event) {
        event.preventDefault();

        const formData = new FormData(form);
        
        try {
            const response = await fetch(`${baseUrl}/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({

                    username: formData.get('username'),
                    password: formData.get('password')


                })
            });
            const data = await response.json();

            if (response.ok) {
                // Registration successful
                localStorage.setItem('vto_login',JSON.stringify(data.data))
                console.log('Login successful', data.data);
                window.location.href = '/auth/protected-route'; // Redirect to homepage or any other page
            } else {
                // Registration failed
                console.error('Login failed');
                const data = await response.json();
                console.error(data.message); // Assuming the API returns an error message
            }
        } catch (error) {
            console.error('Error occurred:', error);
        }
    });
});