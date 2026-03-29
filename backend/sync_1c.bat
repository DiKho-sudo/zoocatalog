@echo off
chcp 65001 >nul
echo ========================================
echo   Синхронизация с 1С Розница
echo ========================================
echo.

cd /d "%~dp0"

echo [1/2] Обновление цен и остатков...
python manage.py sync_stock_prices "..\остаток_цена.xlsx"

echo.
echo [2/2] Проверка новых товаров...
python manage.py import_from_1c "..\про.xlsx" --update

echo.
echo ========================================
echo   Синхронизация завершена!
echo ========================================
echo.
echo Проверьте результат:
echo   Админка: http://localhost:8000/admin/
echo   Сайт: http://localhost:3000/catalog
echo.
pause

