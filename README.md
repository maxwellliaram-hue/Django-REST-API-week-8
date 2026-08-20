# SpendWise Expense Tracker

A polished capstone expense tracker built with Django, Django REST Framework, token authentication, ES Modules, Bootstrap 5, and a responsive custom dashboard.

## Completed feature set

- Secure token-based login with per-user expense ownership
- Create and browse expenses with amount, description, category, and date
- Search descriptions, filter by category, and paginate API results
- Modular front-end logic in `static/budget.js` with exported `calculateTotal()` and `renderExpenses()` functions
- Responsive Bootstrap grid, form, and button utilities combined with the custom SpendWise visual system
- Accessible form labels, validation, focus states, and API error feedback

## Run locally

```powershell
cd django
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/. The API is available at `/api/expenses/` and token login is available at `/api/login/`.

## Publish

The Django dashboard and API must run together, so GitHub Pages alone cannot host the finished authenticated product. Publish the repository source and portfolio documentation on GitHub, then deploy the Django project to a Python-capable host such as Render or Railway. Set `DJANGO_ALLOWED_HOSTS`, `DJANGO_SECRET_KEY`, and the database environment variables in the host dashboard before running `collectstatic` and starting the web service.

For a final review, test the login, add-expense, search, category-filter, pagination, and sign-out flows at narrow mobile and wide desktop widths.

The default database is SQLite so the demo runs immediately. To use PostgreSQL, set `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, and `POSTGRES_PORT` before running migrations.

## API examples

```powershell
$token = (Invoke-RestMethod -Method Post http://127.0.0.1:8000/api/login/ -ContentType 'application/json' -Body '{"username":"alice","password":"pass1234"}').token
$headers = @{ Authorization = "Token $token" }
Invoke-RestMethod http://127.0.0.1:8000/api/expenses/?category=Food^&search=coffee^&ordering=-amount -Headers $headers
```

Every expense query is scoped to the authenticated owner. List responses are paginated with ten entries per page.

## Demo walkthrough

1. Create two users with the Django shell:

	```powershell
	python manage.py shell -c "from django.contrib.auth import get_user_model; User=get_user_model(); User.objects.create_user('alice', password='pass1234'); User.objects.create_user('bob', password='pass1234')"
	```

	The admin at `/admin/` is another option after creating a superuser.
2. Sign in as the first user, add an expense, and show it in the dashboard.
3. Sign out, sign in as the second user, and show that the first user's expense is not returned.
4. Use the category buttons and search field to demonstrate query-string filtering.
