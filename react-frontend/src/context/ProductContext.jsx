import React, { createContext, useEffect, useState } from 'react';
import { fetchProducts } from '../productService';

const ProductContext = createContext();

export const ProductProvider = ( props ) => {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    const fetchProductsData = async () => {
      const fetchedProducts = await fetchProducts(props.routes.backendRoute, props.routes.apiRoute);
      setProducts(fetchedProducts);
    };

    fetchProductsData();
  }, []);

  return (
    <ProductContext.Provider value={products}>
      {props.children}
    </ProductContext.Provider>
  );
};

export default ProductContext;