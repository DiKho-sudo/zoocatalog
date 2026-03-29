import React, { useState, useEffect } from 'react';
import { getBrands, getCategories, getAnimalTypes } from '../services/api';
import './Filters.css';

function Filters({ onFilterChange }) {
  const [brands, setBrands] = useState([]);
  const [categories, setCategories] = useState([]);
  const [animalTypes, setAnimalTypes] = useState([]);
  
  const [filters, setFilters] = useState({
    price_min: '',
    price_max: '',
    brand: '',
    category: '',
    animal_type: '',
    age_group: '',
    is_hypoallergenic: false,
    is_grain_free: false,
  });

  useEffect(() => {
    // Загрузка данных для фильтров
    getBrands().then(res => setBrands(res.data.results || res.data));
    getCategories().then(res => setCategories(res.data.results || res.data));
    getAnimalTypes().then(res => setAnimalTypes(res.data.results || res.data));
  }, []);

  const handleFilterChange = (name, value) => {
    const newFilters = { ...filters, [name]: value };
    setFilters(newFilters);
    onFilterChange(newFilters);
  };

  const handleReset = () => {
    const emptyFilters = {
      price_min: '',
      price_max: '',
      brand: '',
      category: '',
      animal_type: '',
      age_group: '',
      is_hypoallergenic: false,
      is_grain_free: false,
    };
    setFilters(emptyFilters);
    onFilterChange(emptyFilters);
    
    // Сбрасываем все select и input элементы
    document.querySelectorAll('.filters select').forEach(select => {
      select.value = '';
    });
    document.querySelectorAll('.filters input[type="number"]').forEach(input => {
      input.value = '';
    });
    document.querySelectorAll('.filters input[type="checkbox"]').forEach(checkbox => {
      checkbox.checked = false;
    });
  };

  return (
    <div className="filters">
      <div className="filters-header">
        <h3>Фильтры</h3>
        <button onClick={handleReset} className="reset-button">
          Сбросить
        </button>
      </div>

      <div className="filter-group">
        <label>Цена (BYN)</label>
        <div className="price-inputs">
          <input
            type="number"
            placeholder="От"
            value={filters.price_min}
            onChange={(e) => handleFilterChange('price_min', e.target.value)}
          />
          <span>—</span>
          <input
            type="number"
            placeholder="До"
            value={filters.price_max}
            onChange={(e) => handleFilterChange('price_max', e.target.value)}
          />
        </div>
      </div>

      <div className="filter-group">
        <label>Тип животного</label>
        <select
          value={filters.animal_type}
          onChange={(e) => handleFilterChange('animal_type', e.target.value)}
        >
          <option value="">Все</option>
          {animalTypes.map(type => (
            <option key={type.id} value={type.id}>{type.name}</option>
          ))}
        </select>
      </div>

      <div className="filter-group">
        <label>Категория</label>
        <select
          value={filters.category}
          onChange={(e) => handleFilterChange('category', e.target.value)}
        >
          <option value="">Все</option>
          {categories.map(cat => (
            <option key={cat.id} value={cat.id}>{cat.name}</option>
          ))}
        </select>
      </div>

      <div className="filter-group">
        <label>Производитель</label>
        <select
          value={filters.brand}
          onChange={(e) => handleFilterChange('brand', e.target.value)}
        >
          <option value="">Все</option>
          {brands.map(brand => (
            <option key={brand.id} value={brand.id}>{brand.name}</option>
          ))}
        </select>
      </div>

      <div className="filter-group">
        <label>Возрастная группа</label>
        <select
          value={filters.age_group}
          onChange={(e) => handleFilterChange('age_group', e.target.value)}
        >
          <option value="">Все</option>
          <option value="puppy">Щенок/Котенок</option>
          <option value="adult">Взрослый</option>
          <option value="senior">Пожилой</option>
          <option value="all">Все возрасты</option>
        </select>
      </div>

      <div className="filter-group">
        <label className="checkbox-label">
          <input
            type="checkbox"
            checked={filters.is_hypoallergenic}
            onChange={(e) => handleFilterChange('is_hypoallergenic', e.target.checked)}
          />
          <span>Гипоаллергенный</span>
        </label>
      </div>

      <div className="filter-group">
        <label className="checkbox-label">
          <input
            type="checkbox"
            checked={filters.is_grain_free}
            onChange={(e) => handleFilterChange('is_grain_free', e.target.checked)}
          />
          <span>Беззерновой</span>
        </label>
      </div>
    </div>
  );
}

export default Filters;



