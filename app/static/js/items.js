var baseUrl = 'http://18.213.17.243:8081'

document.addEventListener("DOMContentLoaded", function() {

    var userdata = JSON.parse(localStorage.getItem('vto_login'))

    fetch(`${baseUrl}/auth/get-products?gender=${userdata.gender}`)
        .then(response => response.json())
        .then(data => {
            localStorage.setItem('vto_products',JSON.stringify(data))
            const productsContainer = document.getElementById('productContainer');
            data.forEach(product => {
                const productDiv = document.createElement('div');
                productDiv.classList.add('product');
                const productLink = document.createElement('a'); // Creating anchor element
                productLink.href = `product-info?id=${product.id}`; // Assuming this is the product details page
                const img = document.createElement('img');
                img.src = `${baseUrl}/static/clothes/${product.filename}`;
                img.alt = product.name;
                productLink.appendChild(img); // Appending image to anchor element
                const h2 = document.createElement('h2');
                h2.textContent = product.name;
                const pDesc = document.createElement('p');
                pDesc.textContent = `Description of ${product.name}.`;
                const pPrice = document.createElement('p');
                pPrice.textContent = `Price: $10`; // Assuming the price is fixed for now
                const addToCartBtn = document.createElement('a');
                addToCartBtn.href = '#';
                addToCartBtn.classList.add('btn');
                addToCartBtn.textContent = 'Add to Cart';

                productDiv.appendChild(productLink); // Appending anchor element to product div
                productDiv.appendChild(h2);
                productDiv.appendChild(pDesc);
                productDiv.appendChild(pPrice);
                productDiv.appendChild(addToCartBtn);
                productsContainer.appendChild(productDiv);
            });
        })
        .catch(error => console.error('Error fetching products:', error));
    })