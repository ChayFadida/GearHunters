import React, { createContext, useEffect, useState } from "react";
import { fetchProducts } from "../productService";

export const ShopContext = createContext(null);

export const ShopContextProvider = (props) => {
  const [cartItems, setCartItems] = useState({});
  const [products, setProducts] = useState(props.initialProducts || []);

  useEffect(() => {
    const fetchData = async () => {
      if (props.initialProducts) {
        // Products are already available, no need to fetch again
        return;
      }

      try {
        const productsData = await fetchProducts(
          props.routes.backendRoute,
          props.routes.apiRoute
        );
        setProducts(productsData);

        // Set the default cart based on the fetched products
        let defaultCart = {};
        productsData.forEach((product) => {
          defaultCart[product.id] = {
            selected: false,
          };
        });
        setCartItems(defaultCart);
      } catch (error) {
        console.error("Error fetching products:", error);
      }
    };

    fetchData(); // Fetch data when the component mounts
  }, [props.initialProducts, props.routes.backendRoute, props.routes.apiRoute]);

  const selectProduct = (itemId) => {
    setCartItems((prev) => {
      const updatedCart = {
        ...prev,
        [itemId]: {
          selected: true,
        },
      };

      console.log(`Product with ID ${itemId} selected. Updated Cart:`, updatedCart);

      return updatedCart;
    });
  };

  const deselectProduct = (itemId) => {
    setCartItems((prev) => ({
      ...prev,
      [itemId]: {
        selected: false,
      },
    }));
  };

  const contextValue = {
    cartItems,
    selectProduct,
    deselectProduct,
    products,
  };

  return (
    <ShopContext.Provider value={contextValue}>
      {props.children}
    </ShopContext.Provider>
  );
};
