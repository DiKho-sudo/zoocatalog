import React from 'react';
import { Link } from 'react-router-dom';
import './ProductCard.css';

function ProductCard({ product }) {
  // API уже возвращает полный URL, используем его напрямую
  const imageUrl = product.image || '/placeholder.png';
  
  return (
    <Link to={`/product/${product.slug}`} className="product-card">
      <div className="product-image-container">
        <img src={imageUrl} alt={product.name} className="product-image" />
        {product.stock_status === 'out_of_stock' && (
          <div className="out-of-stock-badge">Нет в наличии</div>
        )}
      </div>
      
      <div className="product-info">
        <h3 className="product-name">{product.name}</h3>
        <p className="product-brand">{product.brand_name}</p>
        <p className="product-weight">
          {product.weight} {product.unit || 'шт'}
        </p>
        
        <div className="product-tags">
          {product.is_hypoallergenic && (
            <span className="tag">Гипоаллергенный</span>
          )}
          {product.is_grain_free && (
            <span className="tag">Беззерновой</span>
          )}
        </div>
        
        <div className="product-footer">
          <span className="product-price">{product.price} BYN</span>
          {product.unit === 'кг' && product.weight && (
            <span className="product-price-label">за {product.weight} кг</span>
          )}
        </div>
      </div>
    </Link>
  );
}

export default ProductCard;



