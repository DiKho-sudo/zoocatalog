import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { getProducts } from '../services/api';
import ProductCard from '../components/ProductCard';
import Filters from '../components/Filters';
import CategoryMenu from '../components/CategoryMenu';
import './CatalogPage.css';

function CatalogPage() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [searchParams] = useSearchParams();
  const [filters, setFilters] = useState({});

  useEffect(() => {
    loadProducts();
  }, [filters, currentPage, searchParams]);

  const loadProducts = () => {
    setLoading(true);
    
    const params = {
      page: currentPage,
      ...filters,
    };

    // Добавляем поисковый запрос из URL
    const searchQuery = searchParams.get('search');
    if (searchQuery) {
      params.search = searchQuery;
    }

    // Фильтруем пустые значения
    Object.keys(params).forEach(key => {
      if (params[key] === '' || params[key] === false) {
        delete params[key];
      }
    });

    getProducts(params)
      .then(response => {
        setProducts(response.data.results || []);
        setTotalPages(Math.ceil((response.data.count || 0) / 12));
        setLoading(false);
      })
      .catch(error => {
        console.error('Error loading products:', error);
        setLoading(false);
      });
  };

  const handleFilterChange = (newFilters) => {
    setFilters(newFilters);
    setCurrentPage(1);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handlePageChange = (page) => {
    setCurrentPage(page);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const renderPagination = () => {
    const pages = [];
    const maxPagesToShow = 7;
    
    // Показываем первую страницу
    if (currentPage > 3) {
      pages.push(
        <button key={1} onClick={() => handlePageChange(1)} className="page-button">
          1
        </button>
      );
      if (currentPage > 4) {
        pages.push(<span key="dots1" className="page-dots">...</span>);
      }
    }
    
    // Показываем страницы вокруг текущей
    const startPage = Math.max(1, currentPage - 2);
    const endPage = Math.min(totalPages, currentPage + 2);
    
    for (let i = startPage; i <= endPage; i++) {
      pages.push(
        <button
          key={i}
          onClick={() => handlePageChange(i)}
          className={`page-button ${i === currentPage ? 'active' : ''}`}
        >
          {i}
        </button>
      );
    }
    
    // Показываем последнюю страницу
    if (currentPage < totalPages - 2) {
      if (currentPage < totalPages - 3) {
        pages.push(<span key="dots2" className="page-dots">...</span>);
      }
      pages.push(
        <button key={totalPages} onClick={() => handlePageChange(totalPages)} className="page-button">
          {totalPages}
        </button>
      );
    }
    
    return pages;
  };

  return (
    <div className="catalog-page">
      <div className="container">
        <h1>Каталог товаров</h1>
        
        <div className="catalog-layout">
          <aside className="filters-sidebar">
            <CategoryMenu 
              onCategorySelect={(catId) => handleFilterChange({...filters, category: catId})}
              onAnimalTypeSelect={(typeId) => handleFilterChange({...filters, animal_type: typeId})}
            />
            <Filters onFilterChange={handleFilterChange} />
          </aside>

          <div className="products-area">
            {loading ? (
              <div className="loading">
                <div className="spinner"></div>
                <p>Загрузка товаров...</p>
              </div>
            ) : products.length > 0 ? (
              <>
                <div className="products-grid">
                  {products.map(product => (
                    <ProductCard key={product.id} product={product} />
                  ))}
                </div>

                {totalPages > 1 && (
                  <div className="pagination">
                    <button
                      onClick={() => handlePageChange(currentPage - 1)}
                      disabled={currentPage === 1}
                      className="page-button"
                    >
                      ← Назад
                    </button>
                    {renderPagination()}
                    <button
                      onClick={() => handlePageChange(currentPage + 1)}
                      disabled={currentPage === totalPages}
                      className="page-button"
                    >
                      Вперёд →
                    </button>
                  </div>
                )}
              </>
            ) : (
              <div className="no-products">
                <p>Товары не найдены</p>
                <p>Попробуйте изменить параметры фильтрации</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default CatalogPage;



