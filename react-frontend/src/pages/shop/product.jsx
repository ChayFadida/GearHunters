import React, { useContext } from 'react';
import { ShopContext} from "../../context/shop-context"

export const Product = (props) => {
    const { id, productName, price, productImage } = props.data;
    const { selectProduct } = useContext(ShopContext)
    return (
        <div className='product'>

            <img src={productImage} />
            <div className='description'>
                <p>
                    <b> {productName} </b>
                </p>
                <p> ₪{price}</p>
            </div>
            <div>
                <button className="addToCartBttn" onClick={() => selectProduct(id)}> צפה במוצר</button>
            </div>
        </div>
    )
}