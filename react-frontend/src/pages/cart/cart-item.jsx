import React, { useContext } from "react";
import { ShopContext } from "../../context/shop-context";
import "./cart.css";

export const CartItem = (props) => {
  const { id, productName, price, productImage } = props.data;
  const { deselectProduct } =
    useContext(ShopContext);

  return (
    <div className="cartItem">
      <img src={productImage} />
      <div className="description">
        <p>
          <b>{productName}</b>
        </p>
        <p>₪{price} מחיר</p>
      </div>
      <div className="countHandler">
          <button onClick={() => deselectProduct(id)}> הסר </button>
      </div>
    </div>
  );
};