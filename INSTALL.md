# Install Enterprise Records Mall

## 1. Download & Install Requirements

Begin by cloning the Enterprise Records Mall repository and installing its dependencies:

```bash
git clone https://github.com/badr-azeez/Enterprise-Records-Mall.git
cd Enterprise-Records-Mall
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
```


## 2. Super User
**DEFAULT**

USERNAME = 'admin'

PASSWORD = 'password'

To edit the default admin credentials, navigate to the file "administrator/management/commands/createadmin.py" and modify the following lines:
```python
user = User.objects.create_superuser('admin', 'admin@domain.com', 'password',first_name="admin site")
```

## 3. Make Migrations and Create Admin User

```bash
python manage.py migrate
python manage.py createadmin
```

## 4. Run Enterprise Records Mall

After installing the necessary dependencies, you can run the Enterprise Records Mall server:

```bash
python manage.py runserver
```

