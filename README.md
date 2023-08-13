# SberAfisha-API

<h5>Events</h5>
<b>api/events/</b> - получить все мероприятия (GET) или создать новое мероприятие (POST)
<b>api/events/int:pk/</b> - получить мероприятие по id (GET) или изменить его (PATCH, DELETE)
<b>api/events/filter/</b> - получить мероприятия по фильтру (GET) (date, category, age_category, published)
<b>api/events/images/create/</b> - создать изображение для мероприятия (POST)
<b>api/events/int:pk/comments/add/</b> - добавить комментарий к мероприятию (PATCH)
<b>api/events/platforms/</b> - получить все площадки (GET)
<b>api/events/platforms/int:pk/</b> - получить площадку по id (GET)
<b>api/events/categories/</b> - получить все категории (GET)
<b>api/events/categories/int:pk/</b> - получить категорию по id (GET)
<b>api/events/int:pk/tickets/create/</b> - забронировать билет на мероприятие (POST)
<b>api/events/tickets/my/</b> - получить мои билеты на мероприятие (GET)
<b>api/events/generate/</b> - спарсить спортивные мероприятия (POST)

<br>

<h5>Routes</h5>
<b>api/routes/</b> - получить все маршруты (GET) или создать новый маршрут (POST)
<b>api/routes/int:pk/</b> - получить маршрут по id (GET) или изменить его (PATCH, DELETE)
<b>api/routes/int:pk/tickets/create/</b> - забронировать билет на маршрут (POST)
<b>api/routes/tickets/my/</b> - получить мои билеты на машруты (GET)
