import logo from './logo.svg';
import './App.css';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom"
import { Component } from 'react';
import { AppProvider } from './AppContext';
import { Navbar } from './components/navbar';
import { Shop } from './pages/shop/shop';
import { ShopContextProvider } from './context/shop-context';

function App() {
  console.log("BACKEND_BASE_URL:", process.env.BACKEND_BASE_URL);

  const routes = {
    apiRoute: process.env.REACT_APP_API_BASE_URL || "http://0.0.0.0:8000",
    backendRoute: process.env.REACT_APP_BACKEND_BASE_URL || "http://0.0.0.0:8001",
    
  };
  return (
    <div className="App">
      <ShopContextProvider routes={routes}>
        <AppProvider routes={routes}>
          <Router>
            <Navbar />
            <Routes>
              <Route path="/" element={<Shop />}/>
              <Route path="/cart"/>
            </Routes>
          </Router>
        </AppProvider>
      </ShopContextProvider>
    </div>
  );
}

export default App;
