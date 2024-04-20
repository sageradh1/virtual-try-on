var baseUrl = 'http://18.213.17.243:8081'

document.addEventListener("DOMContentLoaded", function() {
    // Retrieve product ID from the URL
    const urlParams = new URLSearchParams(window.location.search);
    const productId = urlParams.get('id');

    // Retrieve product data from localStorage
    const productData = JSON.parse(localStorage.getItem('vto_products'));

    // Find the product with the matching ID
    const product = productData.find(product => product.id.toString() === productId);

    // Check if the product is found
    if (product) {
        // Update the product image source
        const productImage = document.querySelector('img');
        productImage.src = `${baseUrl}/static/clothes/${product.filename}`; // Replace 'your-server.com' with your server URL

        // Update the product name
        const productName = document.getElementById('productName');
        productName.textContent = product.name;

        // Update other product details as needed
        // For example, you can update description, price, etc.
    } else {
        console.error('Product not found');
    }
    store_images()
});

function store_images() {
    var userdata = JSON.parse(localStorage.getItem('vto_login'))
    fetch(`${baseUrl}/auth/get-generated-images?username=${userdata.username}`)
        .then(response => response.json())
        .then(data => {
            // Store the images in localStorage
            localStorage.setItem('vto_generated', JSON.stringify(data));
            console.log('Images stored in vto_generated:', data);
        })
        .catch(error => console.error('Error fetching generated images:', error));
}