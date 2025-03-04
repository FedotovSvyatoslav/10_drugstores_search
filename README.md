# 10 Drugstores Search
**[Русский](#russian-version) | [English](#english-version)**

## Russian version
Скрипт для поиска 10 ближайших аптек по заданному адресу с отображением на карте. Проект разработан в рамках учебного курса Яндекс Лицея.

Учебные API-ключи в коде просрочены и оставлены для примера.
### Возможности
- Ввод адреса через аргументы командной строки.
- Поиск ближайших аптек с использованием Яндекс API.
- Вывод списка аптек с расстояниями в консоль.
- Генерация карты с метками аптек (зеленые — ежедневные, синие — с интервалами, серые — без расписания).

### Использование
- Пример: `python drugstores_map.py "Москва, Тверская 1"`
- Результат: Список аптек в консоли и карта в файле `map.png`.

### Особенности
- Интеграция с Яндекс Геокодером и Поиском по организациям.
- Расчет расстояний между точками на основе географических координат.
- Простая реализация в одном файле.
- Учебные API-ключи от Яндекс Лицея (просрочены, для работы нужны новые).

### Структура проекта
- `drugstores_map.py`: Основной скрипт.
- `requirements.txt`: Зависимости.
- `.gitignore`: Исключает `.env` и `map.png`.

### Автор
[Федотов Святослав](https://github.com/FedotovSvyatoslav)

---

## English Version
A script to find the 10 nearest drugstores based on an address and display them on a map. Developed as part of the Yandex Lyceum course.

The API keys in the code are expired educational keys.
### Features
- Address input via command-line arguments.
- Search for nearby drugstores using Yandex API.
- Console output of drugstore list with distances.
- Map generation with markers (green — daily, blue — with intervals, gray — no schedule).

### Usage
- Example: `python drugstores_map.py "Moscow, Tverskaya 1"`
- Output: List of drugstores in the console and a map saved as `map.png`.

### Features
- Integration with Yandex Geocoder and Business Search APIs.
- Distance calculation based on geographic coordinates.
- Simple single-file implementation.
- Educational API keys from Yandex Lyceum (expired; new keys required for use).

### Project Structure
- `drugstores_map.py`: Main script.
- `requirements.txt`: Dependencies.
- `.env.example`: Example API key configuration.
- `.gitignore`: Excludes `.env` and `map.png`.

### Author
[Svyatoslav Fedotov](https://github.com/FedotovSvyatoslav)