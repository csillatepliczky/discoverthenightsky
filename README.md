# DISCOVER THE NIGHT SKY
#### Video Demo:  <URL HERE>
#### Website link: http://tcsilla.pythonanywhere.com/

## Description
### About the project
This was my final project to conclude the CS50 Introduction to Computer Sciense course.
I used CSS, HTML, Bootstrap, Javascript, SQLite, Python and the Flask framework for web development.

My final project is a website, where I tried to connect my hobby, the astronomy and astrophotography with programming. Users can find information on the site about the different constellations, like where to find them in the sky, about the mythologies and star lore surrounding them and and about the most spectacular stars and objects in each constellation. I currently uploaded 15 constellations but I plan to extend it with all the 88. Users can also search the deep-sky objects based on different criteria (like visibility, object type or constellation) and register to create their own observation list by selecting the objects they wish to observe.

### HTML pages
I created a HTML page about each constellation, where first a general information and a historical and mythological background can be found about the constellation, then a short description can be read about each notable deep-sky object (i.e. star, galaxy, nebula etc.) in the constellation along with some information regarding the visibility of the object (naked eye, binocular or telescope). These pages can be reached from the Constellation page, where all the constellations are listed in an alphabetical order. Also some general information and description about basic astronomical concepts can be found on the homepage of the website. On the Search page users can search deep-sky objects based on different criteria and if they are logged in, they can add the objects to their observation list on the Observations page.

### Databases
I used three tables for my database:
- the first table contains the information about the deep-sky objects (name, constellation in which the object can be found, coordinates, object type, visibility, difficulty to find in the sky). The primary key is the id for each constellation
- the second table contains the information about the registered users (email, hashed password and user_id for primary key)
- the third table contains the deep-sky objects which the users added their observation lists. Only the names of the objects and the id of the user, who added the object is stored here.

I used SQLite for querying into the databases.

### Documentation 
- https://flask.palletsprojects.com/en/1.1.x/
- https://getbootstrap.com/


### About CS50
CS50 is a openware course from Havard University and taught by David J. Malan

Introduction to the intellectual enterprises of computer science and the art of programming. This course teaches students how to think algorithmically and solve problems efficiently. Topics include abstraction, algorithms, data structures, encapsulation, resource management, security, and software engineering. Languages include C, Python, and SQL plus students’ choice of: HTML, CSS, and JavaScript (for web development).

