import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import HomePage from './pages/HomePage';
import CatalogPage from './pages/CatalogPage';
import ProductDetailPage from './pages/ProductDetailPage';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Header />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/catalog" element={<CatalogPage />} />
            <Route path="/product/:slug" element={<ProductDetailPage />} />
          </Routes>
        </main>
        <footer className="footer">
          <div className="container">
            <p>&copy; 2025 Зоомагазин. Курсовой проект БГУ ФПМИ</p>
          </div>
        </footer>
      </div>
    </Router>
  );
}

export default App;



