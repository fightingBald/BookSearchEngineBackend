**Setting up the project**

Our project will use PostgreSQL as a relational database, Elasticsearch and Django. The simplest way to set up everything is to use Docker.  we will have 3 containers. One for PostgreSQL, one for Elasticsearch and one for Django web application.
1. Download the dataset csv in path at the SearchRngine porject  root dirctory you just cloned

https://drive.google.com/file/d/1vZzlSnYT3yakErkdw8yCoA94omwuVqdS/view?usp=sharing

2. pls have you docker installed and running on your machine, in your docker configuration leave at least 4 GB 

3. cd the project

4. docker-compose up`

5. populate this data into psql database container

`docker-compose run --rm web python manage.py makemigrations`

`#docker-compose run --rm web python manage.py shell`

#Create a model for gutenberg_data.csv

`#>>> from books.models import Book`
`#>>> Book.populate()`

6. index some parts of the data from relational database into Elasticsearch container
`$ docker-compose run --rm web python manage.py search_index --rebuild`
