# OTUS-Social-Network

Запустить проект можно, используя команду `docker compose up` в корне проекта.

Для тестов можно использовать postman коллекцию `Otus Social Network` из корня проекта.

## ДЗ: Индексы и оптимизация запросов

В данной домашней работе требовалось проверить и улучшить производительность эндпоинта поиска пользователя по имени и фамилии.

Тестовые данные генерировались с использованием библиотеки mimesis ([скрипт](backend/scripts/gen_1kk_random_users.py)).

Нагрузочное тестирование производилось при помощи JMeter ([конфигурация](jmeter/user_search.jmx)) в 1/10/100 потоков в течение 60 секунд для каждого числа потоков.

Далее представлены графики latency и throughput до и после добавления индекса (кликабельные).

Метрика|До индексов|После индексов
-|-|-
Active Threads Over Time|![Active Threads Over Time](images/hw2/active_threads_before.png)|![Active Threads Over Time](images/hw2/active_threads_after.png)
Response Times Over Time|![Response Times Over Time](images/hw2/response_times_before.png)|![Response Times Over Time](images/hw2/response_times_after.png)
Transactions per Second|![Transactions per Second](images/hw2/rps_before.png)|![Transactions per Second](images/hw2/rps_after.png)

Из графиков видно, что удалось улучшить latency и throughput на порядок.

Запрос на создание индексов:
```sql
CREATE INDEX users_lower_first_name_collate_c_idx ON users(lower(first_name) COLLATE "C");
CREATE INDEX users_lower_second_name_collate_c_idx ON users(lower(second_name) COLLATE "C");
```

Explain запроса на поиск после создания индексов:
```sql
Limit  (cost=241.30..241.36 rows=25 width=1279) (actual time=1.481..1.484 rows=22 loops=1)
  ->  Sort  (cost=241.30..241.36 rows=25 width=1279) (actual time=1.481..1.482 rows=22 loops=1)
        Sort Key: id
        Sort Method: quicksort  Memory: 64kB
        ->  Bitmap Heap Scan on users  (cost=141.11..240.72 rows=25 width=1279) (actual time=1.321..1.461 rows=22 loops=1)
              Filter: ((lower(first_name) ~~ 'ана%'::text) AND (lower(second_name) ~~ 'бор%'::text))
              Heap Blocks: exact=22
              ->  BitmapAnd  (cost=141.11..141.11 rows=25 width=0) (actual time=1.205..1.205 rows=0 loops=1)
                    ->  Bitmap Index Scan on users_lower_second_name_collate_c_idx  (cost=0.00..70.42 rows=5000 width=0) (actual time=0.553..0.553 rows=4268 loops=1)
                          Index Cond: ((lower(second_name) >= 'бор'::text) AND (lower(second_name) < 'бос'::text))
                    ->  Bitmap Index Scan on users_lower_first_name_collate_c_idx  (cost=0.00..70.42 rows=5000 width=0) (actual time=0.508..0.508 rows=5598 loops=1)
                          Index Cond: ((lower(first_name) >= 'ана'::text) AND (lower(first_name) < 'анб'::text))
Planning Time: 0.533 ms
Execution Time: 1.540 ms
```

Мною были выбраны именно BTree индексы, так как они позволяют быстро искать по префиксу строки.