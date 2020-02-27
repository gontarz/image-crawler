## Image-crawler

### deployment
- make run
- make migrations
- make migrate

### usage
body : {"url":url to crawl or get data}
- POST crawl/image/
- POST crawl/text/
- GET receive/


- GET /task-status/{task_id}/


#### komentarz
Chchiałem stworzyć ciekawe rozwiązanie z wykorzystaniem asyncio.

Plusy:
- Funkcjonalność jest zapewniona
- środowisko stworzone (docker, nginx)
- dodany logger
- baza danych przechowująca historię
- ORM
- kolejka w redis
- zapis zdjęć na podstawie skrótu md5 w celu uniknięcia redundancji
- użyte nowoczesne frameworki
- możliwa skalowalność i dalsza rozbudowa
- małe skomplikowanie

Minusy:
- brak testów
- można było by więcej kodu opisać blokami try except
- brak dokumentacji np swagger
- brak oddzielnych plików ze zmiennymi środowiskowymi (dla danych wrażliwych do alembic, docker-compose, wewnątrz aplikacji)
- można lepiej okodować selectory dla pobierania tekstu z html
- brak crud

Założenie spełniłem minusy wynikają z potrzeby poświęcenia większej ilości czasu projektowi przede wszystkim napisanie testów
oraz rozbudowy aby stworzyć bardziej generyczną aplikację z CRUD dla każdego widoku (na obecną chwilę zasoby zapewniają
tylko funkcjonalności zawarte w zadaniu). Można też dodać więcej możliwości pobierania danych (ftp), informowanie o
statusie zadania(websocket), rozbudowanie bazy danych i zasobów REST.
Jeśli mikrosewis ma pracować aby zapewnić określoną funkcjonalność hermetyzacja kodu
i struktura aplikacji jest wystarczająca aby zapewnić szybkie działanie.

