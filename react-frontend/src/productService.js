//productSrvice.js
export const fetchProducts = async (backendRoute, apiRoute) => {
    try {
        const response = await fetch(`${backendRoute}/fetch_product`);
        const data = await response.json();
        return data.map(product => ({
            id: product.id,
            productName: product.name,
            price: parseFloat(product.current_price),
            productImage: `${apiRoute}/products/${product.id}/image`,
        }));
    } catch (error) {
        console.error('Error fetching data:', error);
        return [];
    }
};
