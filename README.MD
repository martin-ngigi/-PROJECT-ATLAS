## PROJECT ATLAS
- Create requirements text file
```
pip freeze > requirements.txt
```

- install requirements.txt
```
pip install -r requirements.txt
```
or
```
pip install -r /path/to/requirements.txt
```

- Create Admin
```
python manage.py createsuperuser
```
- Sample Admin credentials
```
username: admin
email: admin@gmail.com
password: 123456
```

- Create App
```
python manage.py startapp application
```

- Activate virtaul Enviroment in Windows
```
.venv\scripts\activate
```
- Activate virtaul Enviroment in Mac
```
source .venv/bin/activate
```


- Run server
```
python manage.py runserver
```

- Make migrations
```
python manage.py makemigrations
```
- Run migrations
```
python manage.py migrate
```

## Climate Data APIS:
- World Banks (Documentation)[https://climateknowledgeportal.worldbank.org/download-data]
- https://pypi.org/project/wbpy/
- (National Center for Environmental Information)[https://www.ncei.noaa.gov/cdo-web/webservices/v2]

## Free weather APIs
```
Visual Crossing	
Tomorrow.io	
Weatherbit
Weatherstack
AccuWeather
```