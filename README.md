# AI_assistent
## Getting started

### Install Requirements 
```
pip install -r requirements.txt
```

### Before Starting Server, apply migrations and then migrate due to setup db
##### e.g.
```
python manage.py makemigrations
```
```
python manage.py migrate
```

### Start Server
```
python manage.py runserver
```
Now if you go to [http://127.0.0.1:8000](http://127.0.0.1:8000), you'll see the index page of project and then go to API documentation and check all API which is documented.

### Run this project on Docker
First we need to install docker in our local system after that we build the docker image and container.
Doing this we need to run command 
```
docker-compose up
```
If you want to run it in detached mode (in the background), you can use the -d flag:
```
docker-compose up -d
```
If you make any changes to project code or Docker configuration files and want to rebuild the image, you can use:
```
docker-compose up --build
```

### Deploy this project on heroku we need follow the instruction given below
1. Create Heroku Account : https://www.heroku.com/
2. Download and Install Git : https://git-scm.com/downloads
3. Download and Install Heroku CLI : https://devcenter.heroku.com/articles/heroku-cli#download-and-install
4. Open Terminal
5. Login into Heroku CLI. Run below command it will open Browser then Click on Login 
    ```javascript
      heroku login 
    ```
6. Create an App using Dashboard or Shell (I am creating using Shell)
    ```javascript
      heroku create heroku_app_name
    ```
    ##### e.g.
    ```javascript
      heroku create Ai_assistent
    ```
7. Set Repo
     ```javascript
      heroku git:remote -a heroku_app_name
      ```
    ##### e.g.
    ```javascript
      heroku git:remote -a Ai_assistent
    ```
8. Now add **Procfile** on repo then use command
9. Run below command
    ```javascript
      git add .
      git commit -m "any comment"
      git push heroku master
    ```

### For CI/CD pipeline
For pipeline we use GitHub Actions and also configure all things which have give in task on this file to use it we need to update the configuration with the server keys and configure on Server then it will works and this file is present on 
```javascript
    .github/workflows/ci-cd.yml
```