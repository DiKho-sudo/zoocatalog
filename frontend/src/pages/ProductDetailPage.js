import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getProductBySlug, trackProductView, getSimilarProducts } from '../services/api';
import ProductCard from '../components/ProductCard';
import './ProductDetailPage.css';

function ProductDetailPage() {
  const { slug } = useParams();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedImage, setSelectedImage] = useState(null);
  const [similarProducts, setSimilarProducts] = useState([]);

  useEffect(() => {
    setLoading(true);
    setSimilarProducts([]);

    getProductBySlug(slug)
      .then(response => {
        setProduct(response.data);
        setSelectedImage(response.data.image);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error loading product:', error);
        setLoading(false);
      });

    trackProductView(slug).catch(() => {});

    getSimilarProducts(slug)
      .then(response => setSimilarProducts(response.data || []))
      .catch(() => {});
  }, [slug]);

  if (loading) {
    return <div className="loading">Загрузка...</div>;
  }

  if (!product) {
    return (
      <div className="product-not-found">
        <h2>Товар не найден</h2>
        <Link to="/catalog">Вернуться в каталог</Link>
      </div>
    );
  }

  const imageUrl = selectedImage || '/placeholder.png';
  const allImages = [
    product.image,
    ...(product.additional_images || []).map(img => img.image)
  ].filter(Boolean);

  const getAgeGroupLabel = (ageGroup) => {
    const labels = {
      'puppy': 'Щенок/Котенок',
      'adult': 'Взрослый',
      'senior': 'Пожилой',
      'all': 'Все возрасты'
    };
    return labels[ageGroup] || ageGroup;
  };

  const getStockStatusLabel = (status) => {
    const labels = {
      'in_stock': 'В наличии',
      'out_of_stock': 'Нет в наличии',
      'pre_order': 'Под заказ'
    };
    return labels[status] || status;
  };

  return (
    <div className="product-detail-page">
      <div className="container">
        <div className="breadcrumbs">
          <Link to="/">Главная</Link> / 
          <Link to="/catalog">Каталог</Link> /
          <Link to={`/catalog?category=${product.category.id}`}>
            {product.category.name}
          </Link> /
          <span>{product.name}</span>
        </div>

        <div className="product-detail">
          <div className="product-gallery">
            <div className="main-image">
              <img src={imageUrl} alt={product.name} />
            </div>
            {allImages.length > 1 && (
              <div className="image-thumbnails">
                {allImages.map((img, index) => (
                  <img
                    key={index}
                    src={img}
                    alt={`${product.name} ${index + 1}`}
                    className={selectedImage === img ? 'active' : ''}
                    onClick={() => setSelectedImage(img)}
                  />
                ))}
              </div>
            )}
          </div>

          <div className="product-info-detail">
            <h1>{product.name}</h1>
            
            <div className="product-meta">
              <span className="brand">Производитель: {product.brand.name}</span>
              {product.brand.country && (
                <span className="country">Страна: {product.brand.country}</span>
              )}
            </div>

            <div className="price-section">
              <div className="price">
                {product.price} BYN
                {product.unit === 'кг' && product.weight && (
                  <span className="price-per-package">
                    за упаковку {product.weight} кг
                  </span>
                )}
              </div>
              <div className={`stock-status ${product.stock_status}`}>
                {getStockStatusLabel(product.stock_status)}
              </div>
            </div>

            <div className="product-characteristics">
              <h3>Характеристики</h3>
              <ul>
                <li>
                  <span>{product.unit === 'кг' || product.unit === 'г' ? 'Вес:' : 'Количество:'}</span>
                  <span>{product.weight} {product.unit || 'шт'}</span>
                </li>
                <li>
                  <span>Тип животного:</span>
                  <span>{product.animal_type.name}</span>
                </li>
                <li>
                  <span>Возрастная группа:</span>
                  <span>{getAgeGroupLabel(product.age_group)}</span>
                </li>
                <li>
                  <span>Категория:</span>
                  <span>{product.category.name}</span>
                </li>
              </ul>

              {(product.is_hypoallergenic || product.is_grain_free) && (
                <div className="special-features">
                  {product.is_hypoallergenic && (
                    <span className="badge">Гипоаллергенный</span>
                  )}
                  {product.is_grain_free && (
                    <span className="badge">Беззерновой</span>
                  )}
                </div>
              )}
            </div>

            {product.brand.website && (
              <a 
                href={product.brand.website}
                target="_blank"
                rel="noopener noreferrer"
                className="brand-website"
              >
                Сайт производителя →
              </a>
            )}
          </div>
        </div>

        <div className="product-description-section">
          <div className="description-block">
            <h2>Описание</h2>
            <p>{product.description}</p>
          </div>

          {product.composition && (
            <div className="composition-block">
              <h2>Состав</h2>
              <p>{product.composition}</p>
            </div>
          )}
        </div>

        {similarProducts.length > 0 && (
          <section className="similar-products-section">
            <h2>Похожие товары</h2>
            <div className="similar-products-grid">
              {similarProducts.map(p => (
                <ProductCard key={p.id} product={p} />
              ))}
            </div>
          </section>
        )}

        <div className="back-to-catalog">
          <Link to="/catalog" className="back-button">
            ← Вернуться в каталог
          </Link>
        </div>
      </div>
    </div>
  );
}

export default ProductDetailPage;
