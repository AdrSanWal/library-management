# library-management

This is a project to practice django and learn how to use Vue.js.

I'm not a professional programmer and everything here has been done from scratch and researched on my own, so if you see something that could be improved, let me know. All constructive criticism is welcome

Instructions:
=

1º Clone the repository to a folder:

    git clone https://github.com/AdrSanWal/library-management.git


2º Run docker-compose:

  In the path 'folder/library' execute

    docker-compose up -d

3º Populate the database with some test examples:

    docker exec django-library python3 library/manage.py loaddata initial_data.json


3º Access page:

    localhost:8000

<br>

<strong>Clarifications:</strong>

Tests can be run from library with:

    FIXME: python3 manage.py test
    
There is a simple admin page created, to enter you have to create a superuser::

    python3 manage.py createsuperuser


=
When deleting data I have taken the following considerations:

<ol>

 <li>Books:
    
  <ul>

   <li>When deleting a book, the author will be kept in the database, since there may or may not be more books by the same author, and if there aren't, they could be included in the future.</li>

   <li>The categories are kept for the same reason.</li>
   
  </ul>
 </li>
 <br>
 <li>Author:
    
  <ul>

   <li>In principle, the only reason that occurs to me to eliminate an author from the database is that there are no longer any books by him, so when an author is eliminated, his books will be eliminated from the database.</li>
        
   <li>In case of deleting an author and when deleting all his books some category no longer had representation, it would be kept in case it was necessary in the future.</li>
 
  </ul>
 </li>
 <br>
 <li>Category:
  <ul>
    <li>When deleting a category, it will be deleted from the books that had it associated, in case a book only had this category it would be null.</li>
  </ul>
 </li>

 <br>

 <li>Source isbn validation (in spanish) (https://www.isbn-international.org/es/content/%C2%BFqu%C3%A9-es-un-isbn):

Each ISBN is made up of 5 elements separated from each other by a space or hyphen. Three of the five elements can vary in length:

  <ul>
   <li>Prefix Element – ​​Can only be 978 or 979. Always 3 digits long.</li>

   <li>Registration Group Element – ​​identifies a particular country, geographic region, or language area that participates in the ISBN system. This element can be between 1 and 5 digits in length.</li>

   <li>Headline element – ​​identifies a particular publisher or imprint. It can be up to 7 digits long.</li>

   <li>Publication element – ​​identifies a certain edition and format of a certain title. It can be up to 6 digits long.</li>
    
   <li>Check Digit – is always a single digit validated using a modulo 11 based calculation.</li>
   <br>

Only 13-digit isbn have been used for simplicity

With these premises valid examples would be: 978-12-0687-657-3, 979-24788-86-98-7
  </ul>
 </li>
</ol>


Pending tasks:
<ul>
    <li>Finish editing forms</li>
    <li>Deleting books with modal window</li>
    <li>User registration and login</li>
</ul>