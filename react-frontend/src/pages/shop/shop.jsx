import React, { useState, useEffect } from 'react';
import { useAppContext } from '../../AppContext';
import { Product } from "./product"
import "./shop.css";

export const Shop = () => {
    const [products, setProducts] = useState([]);
    const { routes } = useAppContext();

    useEffect(() => {
      fetch(`${routes.backendRoute}/fetch_product`)
          .then(response => response.json())
          .then(data => {
              console.log('Fetched data:', data);
  
              setProducts(data.map(product => ({
                  id: product.id,
                  productName: product.name,
                  price: parseFloat(product.current_price),
                  productImage: `${routes.apiRoute}/products/${product.id}/image`, // Use the image URL from the backend
                })));
          })
          .catch(error => console.error('Error fetching data:', error));
  }, []);

    return (
        <div className='shop'>
            <div className='shopTitle'>
                <h1> GearsHunter</h1>
            </div>
            <div className='products'>
                {products.map(product => (
                    <Product key={product.id} data={product} />
                ))}
            </div>
        </div>
    )
}
