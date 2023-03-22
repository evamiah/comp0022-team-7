# comp0022-team-7
## Before building
The application makes use of a TMDb API key for some features. Instructions to obtain a key can be found at https://developers.themoviedb.org/3/getting-started/introduction

Please add a config.py file in app/scripts and add a tmdb_key value before building.

app/scripts/config.py should look like :
```python
tmdb_key = "YOUR KEY"
```
# docker-compose
In the directory, run 
```bash
docker-compose up --build
```

After the container is container is created, visit localhost:5000 to view the web application.

***IMPORTANT:*** please allow approximately 15 minutes for all the data to load at the first request. This applies for the first ever build.
