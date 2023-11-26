import React, { useEffect, useContext, useState } from 'react';
import { ShopContext } from '../../context/shop-context';
import ProductContext from '../../context/ProductContext';
import { CartItem } from './cart-item';
import "./cart.css";

export const Cart = () => {
    const { cartItems } = useContext(ShopContext)
    const products = useContext(ProductContext);
    return (
      <div className="cart">
        <div> 
            <h1>!!המוצרים שנבחרו</h1>
        </div>
        <div className="cart">
          {products.map((product) => {
            // Check if cartItems[product.id] is defined before accessing 'selected'
            if (cartItems[product.id]?.selected !== false) {
              return <CartItem data={product} />;
            }
            // If cartItems[product.id] is undefined or selected is false, don't render anything
            return null;
          })}
        </div>
      </div>
    );
};