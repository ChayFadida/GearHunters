import logo from './logo.svg';
import './App.css';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom"
import { Component } from 'react';
import { AppProvider } from './AppContext';
import { Navbar } from './components/navbar';
import { Shop } from './pages/shop/shop';

function App() {
  const routes = {
    apiRoute: 'http://0.0.0.0:8000',
    backendRoute: 'http://0.0.0.0:8001',
  };
  return (
    <div className="App">
      <AppProvider routes={routes}>
        <Router>
          <Navbar />
          <Routes>
            <Route path="/" element={<Shop />}/>
            <Route path="/cart"/>
          </Routes>
        </Router>
      </AppProvider>
    </div>
  );
}

export default App;
