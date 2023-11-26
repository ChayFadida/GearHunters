import React, { useEffect, useState } from 'react';
import { useAppContext } from '../../AppContext';
import { Product } from './product';
import { fetchProducts } from '../../productService'; // Adjust the path accordingly
import './shop.css';

export const Shop = () => {
    const [products, setProducts] = useState([]);
    const { routes } = useAppContext();

    useEffect(() => {
        const fetchData = async () => {
            const productsData = await fetchProducts(routes.backendRoute, routes.apiRoute);
            setProducts(productsData);
        };

        fetchData();
    }, [routes.backendRoute, routes.apiRoute]);

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
    );
};