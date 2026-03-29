import React, { useState, useEffect } from 'react';
import { getCategories, getAnimalTypes } from '../services/api';
import './CategoryMenu.css';

function CategoryMenu({ onCategorySelect, onAnimalTypeSelect }) {
  const [animalTypes, setAnimalTypes] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selectedAnimal, setSelectedAnimal] = useState(null);
  const [expandedCategories, setExpandedCategories] = useState([]);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [animalsRes, categoriesRes] = await Promise.all([
        getAnimalTypes(),
        getCategories()
      ]);
      setAnimalTypes(animalsRes.data.results || animalsRes.data || []);
      setCategories(categoriesRes.data.results || categoriesRes.data || []);
    } catch (error) {
      console.error('Error loading:', error);
    }
  };

  const handleAnimalClick = (animal) => {
    setSelectedAnimal(animal.id === selectedAnimal ? null : animal.id);
    onAnimalTypeSelect(animal.id === selectedAnimal ? null : animal.id);
  };

  const handleCategoryClick = (category) => {
    onCategorySelect(category.id);
  };

  const toggleCategory = (categoryId) => {
    setExpandedCategories(prev =>
      prev.includes(categoryId)
        ? prev.filter(id => id !== categoryId)
        : [...prev, categoryId]
    );
  };

  // Группируем категории по родителям
  const parentCategories = categories.filter(cat => !cat.parent);
  const childCategories = categories.filter(cat => cat.parent);

  return (
    <div className="category-menu">
      <h3 className="menu-title">Категории товаров</h3>
      
      {/* Типы животных */}
      <div className="animal-types-section">
        <h4 className="section-title">Для кого</h4>
        <div className="animal-types-grid">
          {animalTypes.map(animal => (
            <button
              key={animal.id}
              className={`animal-type-btn ${selectedAnimal === animal.id ? 'active' : ''}`}
              onClick={() => handleAnimalClick(animal)}
            >
              {animal.name}
            </button>
          ))}
        </div>
      </div>

      {/* Категории */}
      <div className="categories-section">
        <h4 className="section-title">Категории</h4>
        {parentCategories.map(parent => {
          const children = childCategories.filter(c => c.parent === parent.id);
          const isExpanded = expandedCategories.includes(parent.id);

          return (
            <div key={parent.id} className="category-group">
              <div className="category-parent">
                <button
                  className="category-parent-btn"
                  onClick={() => handleCategoryClick(parent)}
                >
                  {parent.name}
                </button>
                {children.length > 0 && (
                  <button
                    className="expand-btn"
                    onClick={() => toggleCategory(parent.id)}
                  >
                    {isExpanded ? '−' : '+'}
                  </button>
                )}
              </div>

              {isExpanded && children.length > 0 && (
                <div className="category-children">
                  {children.map(child => (
                    <button
                      key={child.id}
                      className="category-child-btn"
                      onClick={() => handleCategoryClick(child)}
                    >
                      {child.name}
                    </button>
                  ))}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default CategoryMenu;
