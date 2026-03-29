import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getProducts, getCategories, getPopularProducts, getRecommendedProducts } from '../services/api';
import ProductCard from '../components/ProductCard';
import './HomePage.css';

const HOME_CATEGORY_ORDER = [
  'suhie-korma',
  'vlazhnye-korma',
  'konservy',
  'amunicija',
  'igrushki',
  'kogteto chki',
  'sredstva-gigieny',
];

function HomePage() {
  const [latestProducts, setLatestProducts] = useState([]);
  const [popularProducts, setPopularProducts] = useState([]);
  const [recommendedProducts, setRecommendedProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      getProducts({ page_size: 8 }),
      getCategories(),
      getPopularProducts(),
      getRecommendedProducts()
    ]).then(([productsRes, categoriesRes, popularRes, recRes]) => {
      setLatestProducts(productsRes.data.results || []);
      const allCats = categoriesRes.data.results || categoriesRes.data || [];
      const ordered = HOME_CATEGORY_ORDER
        .map(slug => allCats.find(c => c.slug === slug))
        .filter(Boolean);
      setCategories(ordered.length > 0 ? ordered : allCats.slice(0, 6));
      setPopularProducts(popularRes.data || []);
      setRecommendedProducts(recRes.data || []);
      setLoading(false);
    }).catch(error => {
      console.error('Error loading data:', error);
      setLoading(false);
    });
  }, []);

  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <p>Загрузка...</p>
      </div>
    );
  }

  return (
    <div className="home-page">
      <section className="hero">
        <div className="container">
          <h1>Добро пожаловать в зоомагазин!</h1>
          <p>Качественные товары для ваших любимых питомцев</p>
          <Link to="/catalog" className="cta-button">
            Перейти в каталог
          </Link>
        </div>
      </section>

      <section className="categories-section">
        <div className="container">
          <h2>Категории товаров</h2>
          <div className="categories-grid">
            {categories.map(category => (
              <Link 
                key={category.id}
                to={`/catalog?category=${category.id}`}
                className="category-card"
              >
                {category.image && (
                  <img 
                    src={`http://${window.location.hostname}:8000${category.image}`}
                    alt={category.name}
                  />
                )}
                <h3>{category.name}</h3>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {recommendedProducts.length > 0 && (
        <section className="products-section recommended-section">
          <div className="container">
            <h2>Рекомендуем для вас</h2>
            <div className="products-grid">
              {recommendedProducts.map(product => (
                <ProductCard key={product.id} product={product} />
              ))}
            </div>
          </div>
        </section>
      )}

      {popularProducts.length > 0 && (
        <section className="products-section popular-section">
          <div className="container">
            <h2>Популярные товары</h2>
            <div className="products-grid">
              {popularProducts.map(product => (
                <ProductCard key={product.id} product={product} />
              ))}
            </div>
          </div>
        </section>
      )}

      <section className="products-section">
        <div className="container">
          <h2>Новые товары</h2>
          <div className="products-grid">
            {latestProducts.map(product => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
          <div className="view-all">
            <Link to="/catalog" className="view-all-button">
              Смотреть все товары
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}

export default HomePage;
