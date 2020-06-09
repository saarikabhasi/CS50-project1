CS50 Web Programming with Python and JavaScript
Project 0: Homepage
Webpage link: https://the-booklover.herokuapp.com/

Description:

Development of a Book review website 'The Book Fair', which allows a registered user search for a book,leave a review, also view ratings from third party website such as Good Reads and Google Books.

General information:

1. Pulls book publisher details, description, book cover thumbnail image  from the Google books API.
2. Displays information such ratings and number of reviews from Google Books and Good Reads API
3. Database setup using Heroku and PostgreSQL.
4. Media query supporting smaller screens.
5. Users can make a API get request to the website by https://the-booklover.herokuapp.com/api/isbn.




File Specific details:
1. application.py :

   i. Back-end code for the website where the DB queries, api requests are made.
      - Developed in Python, flask, sqlalchemy, werkzeug python library for secure user authentication.

2. import.py :

   i. Reads a csv file- 'books.csv' that consist of book information and store those information to the table'books'. 

templates/:

3. baselayout.html:

   i. Base layout for  register, login , authenticate and passwordchange html files.
    -  flash messages and display logo.

4. layout.html:
    i. Base layout for book,index,message and reviews html files.
    - flash messages,logo and navigation tabs and displays user information.

    
5. login.html:

    i. SignIn page where user can Login to the account. 
    - Requires Email id and Password.
    - Email id must be registered to login.
    - Error messages are displayed if email id is not found in Database 
        - forgot password button is displayed.

6. register.html:

    i. Register page where the user create an account.
      - Requires Name, Email id , password and confirm password . 
      - Requires both password and confirm password to be same.
      - Requires Password length must be atleast 6 characters
      - Error messages are displayed if any of the above requirements are failed. 
      - Error message displayed if email id already registered.

7. authenticate.html:
    i. verify account before changing password.
     - Required Name and email id. 
     - Error messages are displayed if Name or Email id didnot match. 

8. passwordchange.html:
    i. On successful account verification user can change password.
     - Requires Email id , password and confirm password . 
     - Requires Email id to exist in database.
     - Requires both password and confirm password to be same.
     - Requires Password length must be atleast 6 characters.
     - Error messages are displayed if any of the above requirements are failed. 
9. index.html:
    i. Displays user name, nav tabs and logo on top of the page.

    ii. Search bar- where user can type query.
        - can be partial queries with trailing spaces and numbers.

    iii. Radio button to search according to user choice
    - user can search by book isbn or title or author or all of the above.
    iv. On submiting the search button. Any of the below step occurs.
        - displays all the books that closely matches to the query with respective to isbn or title or author
        - if query does not closely match, then displays 'search results for'. 
        - if no book found in Database, then displays 'No books found'

    v. On successful search, displays book title, author, published year and isbn from the database
    - hyperlink on title and author.
        - if user clicks title.
            - displays book details on book.html
        - if user clicks author.
            - displays all the books by the author.
    
10. book.html:
    i. If user clicks title in index.html/search page, the book page display
    - Book name, book image(from Google books API) and author
    - Hyperlink to sections: book overview, book reviews and write a review.
    - Overview section shows:
        - Book isbn
        - publisher(from Google books API)
        - Published year
        - Description (from Google books API)
    - Book reviews (in a CARD):
        - Shows average rating and total number of reviews left by the users.
        - Average rating and total number of reviews from Good reads website and Google books.
        - hyperlink to the search query of each of these website (including our website)
        - Shows the comments,rating and name of users who had left the review.
    - Write a review:
        - A textarea where user can write the review.
        - Rate the book with stars on scale of 1-5.
        - submit button
    - On submiting the submit button, one of below step occurs:
        - application.py checks if the user had already submitted review
        - application.py checks if the user had submitted empty query.
            - Displays error message if any of the above check is failed in message.html.
        - if above check is sucessful, application.py updates the review in DB.
            - Displays success message in message.html.
    ii. If user clicks author in index.html/search page, the book page displays:
    - Book name, book image(from Google books API),author name, published year and isbn.
    - Book reviews (in a CARD):
        - Shows average rating and total number of reviews left by the users.
        - Average rating and total number of reviews from Good reads website and Google books.
        - Hyperlink to the search query of each of these website (including our website)
        - Shows the comments,rating and name of users who had left the review.

11. reviews.html:
    i. User can check all of their reviews in this page.
    ii. Displays:
    - Book title with hyperlink to book.html by title.
    - Rating displayed in star
    - Comments.
12. message.html:
    i. Displays review messages from book page and application.py


static/css

13. main.css:
    i. Styling format for entire webpage.
14. requirements.txt:
    i. Information about the Python packages that are used by the website.


 

BUILT WITH:

Bootstrap (version: 4.5)
Microsoft Visual code (version:1.44)
Flask (version: 1.1.2)
Flask-Session(version: 0.3.2)
gunicorn (version: 20.0.4)
Jinja2 (version: 2.11.2)
psycopg2 (version: 2.8.5)
requests (version: 2.23.0)
SQLAlchemy(version:1.3.17)
Werkzeug(version:1.0.1)
Python(version 3.7.3)
HTML5
Cascading Style Sheets (CSS)



AUTHOR:
NAIR SAARIKA BHASI
