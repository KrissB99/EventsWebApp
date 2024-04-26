# Events Web App by Krysia Banaszewska

## Run application

```
docker-compose -f docker-compose.yml up --build
```

## Create database

```
docker-compose exec app flask create-db
```

Additional info:

- You can grant an admin permission by going to users settings and update users info 
(you find settings at the navbar by clicking on user icon on the right hand side)

- Test doesn't work due to lack of time