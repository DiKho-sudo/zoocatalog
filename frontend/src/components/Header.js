import React, { useState, useEffect, useRef } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { getProducts } from '../services/api';
import './Header.css';
import './SearchSuggestions.css';

function Header() {
  const [searchQuery, setSearchQuery] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [isSearching, setIsSearching] = useState(false);
  const navigate = useNavigate();
  const searchTimeout = useRef(null);
  const suggestionsRef = useRef(null);

  // Закрытие подсказок при клике вне
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (suggestionsRef.current && !suggestionsRef.current.contains(event.target)) {
        setShowSuggestions(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Debounce для поиска (задержка 500ms)
  useEffect(() => {
    if (searchQuery.length >= 2) {
      setIsSearching(true);
      
      if (searchTimeout.current) {
        clearTimeout(searchTimeout.current);
      }

      searchTimeout.current = setTimeout(() => {
        searchSuggestions(searchQuery);
      }, 500);
    } else {
      setSuggestions([]);
      setShowSuggestions(false);
      setIsSearching(false);
    }

    return () => {
      if (searchTimeout.current) {
        clearTimeout(searchTimeout.current);
      }
    };
  }, [searchQuery]);

  const searchSuggestions = async (query) => {
    try {
      const response = await getProducts({ search: query, page_size: 5 });
      setSuggestions(response.data.results || []);
      setShowSuggestions(true);
      setIsSearching(false);
    } catch (error) {
      console.error('Search error:', error);
      setIsSearching(false);
    }
  };

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/catalog?search=${searchQuery}`);
      setShowSuggestions(false);
    }
  };

  const handleSuggestionClick = (product) => {
    navigate(`/product/${product.slug}`);
    setSearchQuery('');
    setShowSuggestions(false);
  };

  return (
    <header className="header">
      <div className="container">
        <div className="header-content">
          <Link to="/" className="logo">
            <h1>🐾 Зоомагазин</h1>
          </Link>
          
          <div className="search-container" ref={suggestionsRef}>
            <form className="search-form" onSubmit={handleSearch}>
              <input
                type="text"
                placeholder="Поиск товаров..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onFocus={() => suggestions.length > 0 && setShowSuggestions(true)}
                className="search-input"
              />
              <button type="submit" className="search-button">
                {isSearching ? '⏳' : '🔍'}
              </button>
            </form>
            
            {showSuggestions && suggestions.length > 0 && (
              <div className="search-suggestions">
                {suggestions.map(product => (
                  <div
                    key={product.id}
                    className="suggestion-item"
                    onClick={() => handleSuggestionClick(product)}
                  >
                    <div className="suggestion-name">{product.name}</div>
                    <div className="suggestion-price">{product.price} BYN</div>
                  </div>
                ))}
                <div className="suggestion-footer" onClick={handleSearch}>
                  Показать все результаты →
                </div>
              </div>
            )}
          </div>
          
          <nav className="nav">
            <Link to="/" className="nav-link">Главная</Link>
            <Link to="/catalog" className="nav-link">Каталог</Link>
          </nav>
        </div>
      </div>
    </header>
  );
}

export default Header;



