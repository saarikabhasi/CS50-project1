# CS50 Web Programming with Python and JavaScript

Webpage link: https://courses.edx.org/courses/course-v1:HarvardX+CS50W+Web/course/


## Project 1: Books

Webpage link: https://the-booklover.herokuapp.com/

### Description:

Development of a Book Reviewing website - **'The Book Fair** 

The Book Fair website allows its user register an account, search for a book and look into a book details such as its ISBN, Title, author, published year and publisher information etc. Additionally, It also displays the Book's average rating and comments left by other readers in the Book Fair website and in other third-party website such as **Good Reads and Google Books**. The Book Fair also gives its user a provision to write review and rate the book on the scale of 1-5, which are visible to other users. 


### General information:

1. Pulls book publisher details, description, book cover thumbnail image  from the Google books API.
2. Database setup using Heroku and PostgreSQL.
3. Supports smaller screens.
4. Users can make a API get request to the website by https://the-booklover.herokuapp.com/api/<isbn>.

*Below features are supported by the Book Fair Website:*

#### User Authentication

##### Register

* To view the books in this website, the first user has to create an account. 
  * In order to register user has to fill their name, email id, password. 
     -The website imposes few restrictions for a successful register.
      
         i. All the fields are mandatory
         ii. Password must be of atleast 6 characters and both Password and confirm password must be same.  
         iii. Checks if user has already registered.
         
 * The password is stored in the Database using **Python-werkzeug library for secure user authentication**

##### Login

 * After successfully registering their account, user can signIn with their email id and password to the website.
 
##### Logout:

  * User can logout from their account at any point of their time, but just clicking the Logout button.
  
##### Forgot password/ Change password Feature:
  
  * If user has forgot their password, user can change their password by clicking forgot password option that is displayed in Sign In page on their first failed attempt of login.  
  
##### Verify account (required for changing password):

   * In order to change password, user has to verify their account by providing their name and email id that they have gave while registering their account.
  
##### Change password:

   * On verifying the account successfully user can change their password by providing their email id, new password and confirming the new password.
   
      * The change password follows the same set of password restrictions rules that is used by register page.
      
##### My Reviews:
   * On successful login, user can view their reviews by clicking my review tab on top the webpage.
 
##### Write a review:
 
   * At any given period of time, A user can comment and rate only once for a book.
   * user can not give empty rating and comment.
   * Message is displayed if the user has rated book successfully.
   
##### Search:
   * A Search bar where user can type their query to find a book.
      - user can search by book isbn or title or author or all of the above.
   * Handles Partial, numbers, trailing spaces query.
   * Shows all books that closely matches to the query with respective to isbn , title,  author and year 
     - if query does not closely match with book title, author, isbn or year
      - displays *'search results for'*  and shows all the books whose details closely match query's first letter. 
     - if no book found in Database, then displays *'No books found'*
     
   

### File Specific details:

1. application.py :

   i. Back-end code for the website where the all the features DB queries, api requests,  are made.
      - Developed in Python, flask, sqlalchemy

2. import.py :

   i. Reads a csv file- 'books.csv' that consist of book information and store those information to the table'books'. 

# templates/:

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


# static/css

13. main.css:
   i. Styling format for entire webpage.
      
14. requirements.txt:
   i. Information about the Python packages that are used by the website.


 

### BUILT WITH:

1. Bootstrap (version: 4.5)
2. Microsoft Visual code (version:1.44)
3. Flask (version: 1.1.2)
4. Flask-Session(version: 0.3.2)
5. gunicorn (version: 20.0.4)
6. Jinja2 (version: 2.11.2)
7. psycopg2 (version: 2.8.5)
8. requests (version: 2.23.0)
9. SQLAlchemy(version:1.3.17)
10. Werkzeug(version:1.0.1)
11. Python(version 3.7.3)
12. HTML5
13. Cascading Style Sheets (CSS)



### AUTHOR:
NAIR SAARIKA BHASI
