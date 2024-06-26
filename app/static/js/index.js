var baseUrl = 'http://18.213.17.243:8081'

document.addEventListener("DOMContentLoaded", function() {
    fetch(`${baseUrl}/auth/get-products`)
        .then(response => response.json())
        .then(data => {
            const productsContainer = document.getElementById('productContainer');
            data.forEach(product => {
                const productDiv = document.createElement('div');
                productDiv.classList.add('product');
                const img = document.createElement('img');
                img.src = `${baseUrl}/static/clothes/${product.filename}`;
                img.alt = product.name;
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

                productDiv.appendChild(img);
                productDiv.appendChild(h2);
                productDiv.appendChild(pDesc);
                productDiv.appendChild(pPrice);
                productDiv.appendChild(addToCartBtn);
                productsContainer.appendChild(productDiv);
            });
        })
        .catch(error => console.error('Error fetching products:', error));
});