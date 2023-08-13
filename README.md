# SberAfisha-API

<h4>Users</h4>
<b>api/users/auth/token/login/</b> - войти в аккаунт пользователя или получить jwt-токен (POST)<br>
<b>api/users/auth/users/</b> - получить всех пользователей (GET) или создать пользователя (POST)<br>
<b>api/users/auth/users/me/</b> - получить свой профиль (GET)<br>
<b>api/artists/</b> - получить всех артистов (GET) или создать артиста (POST)<br>
<b>api/artists/<int:pk>/</b> - получить артиста (GET) или изменить артиста (PATCH) или удалить артиста (DELETE)<br>
<b>api/artists/manager/my/</b> - получить своего артиста (для менеджера)<br>

<br>

<h4>Events</h4>
<b>api/events/</b> - получить все мероприятия (GET) или создать новое мероприятие (POST)<br>
<b>api/events/int:pk/</b> - получить мероприятие по id (GET) или изменить его (PATCH, DELETE))<br>
<b>api/events/filter/</b> - получить мероприятия по фильтру (GET) (date, category, age_category, published))<br>
<b>api/events/images/create/</b> - создать изображение для мероприятия (POST))<br>
<b>api/events/int:pk/comments/add/</b> - добавить комментарий к мероприятию (PATCH))<br>
<b>api/events/platforms/</b> - получить все площадки (GET))<br>
<b>api/events/platforms/int:pk/</b> - получить площадку по id (GET))<br>
<b>api/events/categories/</b> - получить все категории (GET))<br>
<b>api/events/categories/int:pk/</b> - получить категорию по id (GET))<br>
<b>api/events/int:pk/tickets/create/</b> - забронировать билет на мероприятие (POST))<br>
<b>api/events/tickets/my/</b> - получить мои билеты на мероприятие (GET))<br>
<b>api/events/generate/</b> - спарсить спортивные мероприятия (POST))<br>

<br>

<h4>Routes</h4>
<b>api/routes/</b> - получить все маршруты (GET) или создать новый маршрут (POST))<br>
<b>api/routes/int:pk/</b> - получить маршрут по id (GET) или изменить его (PATCH, DELETE))<br>
<b>api/routes/int:pk/tickets/create/</b> - забронировать билет на маршрут (POST))<br>
<b>api/routes/tickets/my/</b> - получить мои билеты на машруты (GET)
