import os
import csv


class PriceMachine():

    def __init__(self):
        self.data = []
        self.result = ''
        self.name_length = 0

    def load_prices(self, file_path='.'):
        '''
            Сканирует указанный каталог. Ищет файлы со словом price в названии.
            В файле ищет столбцы с названием товара, ценой и весом.
            Допустимые названия для столбца с товаром:
                товар
                название
                наименование
                продукт

            Допустимые названия для столбца с ценой:
                розница
                цена

            Допустимые названия для столбца с весом (в кг.)
                вес
                масса
                фасовка
        '''

        if not os.path.exists(file_path):
            raise FileNotFoundError(f'Директория {file_path} не найдена!')

        valid_product = {'товар', 'название', 'наименование', 'продукт'}
        valid_price = {'розница', 'цена'}
        valid_weight = {'вес', 'масса', 'фасовка'}

        '''
            Пороверяем название файлов и разширений необходимых для работы с ними
        '''

        for filename in os.listdir(file_path):
            if 'price' in filename.lower() and filename.endswith('.csv'):
                full_file_path = os.path.join(file_path, filename)

                '''
                    Считываем файл. Находим заголовок и сохраняем в переменную 'headers'
                '''
                with open(full_file_path, encoding='utf-8') as file:
                    reader = csv.reader(file, delimiter=',')
                    headers = next(reader)

                    '''
                        Проверяем заголовки на те, которые нам необходимы
                    '''

                    product_index = self._search_product_price_weight(headers, valid_product)
                    price_index = self._search_product_price_weight(headers, valid_price)
                    weight_index = self._search_product_price_weight(headers, valid_weight)

                    '''
                        Если продукты, цена и вес не пустые, будем считывать колонки и сохранять в данных
                    '''

                    if product_index is not None and price_index is not None and weight_index is not None:
                        for row in reader:
                            try:
                                product = row[product_index].strip()
                                price = float(row[price_index])
                                weight = float(row[weight_index])
                                price_per_kg = price / weight
                                self.data.append({
                                    'product': product,
                                    'price': price,
                                    'weight': weight,
                                    'filename': filename,
                                    'price_per_kg': price_per_kg
                                })
                            except (ValueError, IndexError):
                                continue



    def _search_product_price_weight(self, headers, valid_name):
        '''
            Возвращает номера столбцов
        '''
        for index, header in enumerate(headers):
            if header.lower() in valid_name:
                return index
        return None

    def export_to_html(self, fname='output.html'):
        '''
            Экспорт данных в HTML файл.
        '''

        result = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Позиции продуктов</title>
        </head>
        <body>
            <table>
                <tr>
                    <th>Номер</th>
                    <th>Название</th>
                    <th>Цена</th>
                    <th>Фасовка</th>
                    <th>Файл</th>
                    <th>Цена за кг.</th>
                </tr>
        '''

        for idx, item in enumerate(self.data, start=1):
            result += f'''
                    <tr>
                        <td>{idx}</td>
                        <td>{item['product']}</td>
                        <td>{item['price']}</td>
                        <td>{item['weight']}</td>
                        <td>{item['filename']}</td>
                        <td>{item['price_per_kg']:.2f}</td>
                    </tr>
                '''
        result += '''
            </table>
        </body>
        </html>
        '''

        with open(fname, mode='w', encoding='utf-8') as file:
            file.write(result)


    def find_text(self, text):
        """
            Ищет товары по фрагменту названия и возвращает отсортированный список позиций.
        """

        result = [item for item in self.data if text.lower() in item['product'].lower()]
        sorted_result = sorted(result, key=lambda x: x['price_per_kg'])
        self.result = sorted_result

        print('\n№      Название                цена вес     файл    цена за кг')
        for i, item in enumerate(sorted_result, start=1):
            print(f'{i:<3} {item['product']:<25} {item['price']:<5} {item['weight']:<4} {item['filename']:<10} '
                  f'{item['price_per_kg']:.2f}')

if __name__ =='__main__':

    '''
        Логика работы программы
    '''

    pm = PriceMachine()
    try:
        pm.load_prices()
        print('Вы загрузили данные для обработки!')
    except Exception as e:
        print(f'Ошибка: {e}')
        exit()
    while True:
        query = input(f'Введите текст для поиска или "exit" для выхода:\n').strip()
        if query.lower() == 'exit':
            print('Вы вышли. До свидания!')
            break
        if not query:
            print('Запрос не может быть пустым\n')
            continue
        pm.find_text(query)
    print('Экспорт данных в HTML файл')
    pm.export_to_html()
    print('Экспорт данных завершен! Данные сохранены в файле "output.html".')