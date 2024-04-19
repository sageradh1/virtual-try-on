var baseUrl = 'http://18.213.17.243:8081'

document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');

    form.addEventListener('submit', async function(event) {
        event.preventDefault();

        const formData = new FormData(form);

        try {
            const response = await fetch(`${baseUrl}/auth/login`, {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                // Registration successful
                console.log('Login successful');
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