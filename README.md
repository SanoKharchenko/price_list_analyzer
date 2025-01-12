# Анализатор прайс-листов
Производит анализ с прайс-листов 

## Описание

* Загружает данные с прайс-листов с именем "price" и расширением .csv в корневой папке
* Производит поиск по названию
* Экспортирует все данные с прайс-листов в файл HTML 

## Пользоваться

* Установить
  ```
  git clone https://github.com/SanoKharchenko/price_list_analyzer
  cd price_list_analyzer
  ```
* Переместить файлы для анали в директорию проекта.
  
  - Файл должен иметь в названии слово "price" и иметь раснирение ".csv"
  - Файл должен содержать допустимые названия для колонок
      * Название товара ('название', 'продукт', 'товар', 'наименование')
      * Цена ('цена', 'розница')
      * Вес ('фасовка', 'масса', 'вес')
* Запустить файл
  ```
  python project.py
  ```
* Ввести запрос для поиска
* Для выхода из поиска ввести 'exit'
* После завершения работы будет создан файл `output.html` в котором сохранены все данные

# Пример

![2025-01-12_16-36-40](https://github.com/user-attachments/assets/59e0284d-555a-4eeb-a53c-acb50ad2ba34)
