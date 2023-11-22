import React from 'react';
import { Link } from 'react-router-dom';
import { ShoppingBag } from 'phosphor-react'
import "./navbar.css";
export const Navbar = () => {
    return (
        <div className='navbar'>
            <div>
                <Link to="/"> מוצרים </Link>
                <Link to="/cart"> 
                    <ShoppingBag size={32}/>
                </Link>
            </div>
        </div>
    )
}