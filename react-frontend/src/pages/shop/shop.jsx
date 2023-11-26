import React, { useEffect, useState, useContext } from 'react';
import { useAppContext } from '../../AppContext';
import { Product } from './product';
import { fetchProducts } from '../../productService'; // Adjust the path accordingly
import './shop.css';
import ProductContext from '../../context/ProductContext';

export const Shop = () => {
    const products = useContext(ProductContext);
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