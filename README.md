# CS50 Web Programming with Python and JavaScript

Webpage link: https://courses.edx.org/courses/course-v1:HarvardX+CS50W+Web/course/


## Project 1: Books

Webpage link: https://the-booklover.herokuapp.com/

### Description:

Development of a Book Reviewing website - **'The Book Fair'** 

The Book Fair website allows its user to register, search for a book, see the book details, and leave comments and rate the book on the scale of 1 to 5 . It also displays the Book's average rating and comments left by other readers in the Book Fair website and pulls Rating information from third-party website such as **Good Reads and Google Books**.  


### General information:

1. Pulls book publisher details, description, book cover thumbnail image  from the Google books API.
2. Database setup using Heroku and PostgreSQL.
3. Supports smaller screens.
4. Users can make a API get request to the website by https://the-booklover.herokuapp.com/api/isbn.
   * isbn is the book isbn number:
       * Example:
            * https://the-booklover.herokuapp.com/api/0380753022 (isbn: 0380753022)


### *File Specific and Feature details:*

### User Authentication 
-------------------------
### File path: templates/:

#### 1. Register(register.html)

* To view the books, the user has to create an account. 
  * In order to register user has to fill their name, email id, password. 
   - The website imposes few restrictions for a successful registration.
      
         i. All the fields are mandatory
         ii. Password must be of atleast 6 characters and both Password and confirm password must be same.  
         iii. Checks if user has already registered.
         
    - Messages are displayed on successful registeration and also if any of above restrictions are failed.
         
 * The password is stored in the Database using **Python-werkzeug library for secure user authentication**

#### 2. Login (login.html)

 * After successfully registering their account, user can Login with their Email id and Password.
 
 * **Forgot password/ Change password feature** 
  
     * User can change their password by clicking forgot password option that is displayed in Sign In page on their first failed attempt of login.  

  
#### 3. Verify account (required for changing password) (authenticate.html)

   * In order to change password, user has to verify their account by providing their name and email id that they have gave while registering their account.
   
   * Messages are displayed if Name and Email id did not match and also, if name or email id is not found in Database.
  
#### 4. Change password:(passwordchange.html)

   * On verifying the account successfully user can change their password by providing their email id, new password and confirming the new password.
   
   * The change password follows the same set of password restrictions rules that is used by register page.
   * Messages are displayed on successful password change, also, if email id is not found in Database and if password did not match.
   
#### 5. baselayout.html:
   * Base layout for templates/ 
        * register.html
        * login.html 
        * authenticate.html 
        * passwordchange.html
        
   * flash messages and displays logo.
      
### Layout details for HTML files after successful Login:
------------------------------------------------------
 #### 6. templates/layout.html:
   * Base layout for templates/
          * book.html
          * index.html
          * message.html
          * reviews.html
    * flash messages, display logo, navigation tab and user information on all pages.  
    
   ***Navigation tab on top all page -(from layout.html)***
   ----------------------------------------------------
   **Home (redirects to *templates/index.html*)**
   
    * Go to search page any point of time.

   **7. My Reviews (redirects to *templates/reviews.html*)**
   
   * On successful login, user can view their reviews by clicking my review tab on top the webpage.
   * Shows all the books rated by the user:
     * Each book has:
       - Book Title, user rating and comments.
    
  **Logout**

   * User can Logout from their account at any point of time, by just clicking the Logout button.
   
   **User details**
 
   * On right side of page shows user name.      
   
### Search a book (templates/index.html)
--------------------------------------------------   

#### 8. Search:
   * A Search bar where user can type their query to find a book.
      - user can search by book isbn or title or author (displayed in a Radio button).
   * Handles Partial, numbers, trailing spaces query.
   
#### 9. Search Results:

   * Shows all books that closely matches to the query with respective to isbn , title,  author and year
   * Shows Book Title, author, published year and Isbn of the book.
   * Hyperlinks to Book Title to see book details
   * Hyperlinks to Book author to see details of all the books written by the author.
   * *Note:
     * if query does not closely match with book title, author, isbn or year
         - displays **'search results for'**  and shows all the books whose details closely match query's first letter. 
         - if no book found in Database, then displays **'No books found'**
     * If user submits empty query, displays **'No Results'**
     
### Show a Book (templates/book.html)
--------------------------------------

#### 10. Based on Book title: (when user clicks on book title on search page)

   * Shows Book Title, Book Thumbnail(from Google Books API),Author.
   * Hyperlinks to navigate within book page.
   * Overview:
     - Shows Book Isbn
     - Publisher details (from Google books API)
     - Published year
     - Description (from Google books API)
     
   * Book reviews (a card):
     - Shows average rating and total number of reviews left by the users in **The Book Fair** .
     - Average rating and total number of reviews from Third-party website **Good Reads** and **Google Books**.
     - Hyperlinks to each of the website.
     - Shows the comments,rating and name of users who had left the review.
     
   * Write a review:
     - A provision for a user to Write a Review and Rate on a scale of 1-5.
     - At any given period of time, A user can comment and rate only once for a book.
     - User can not give empty rating and comment.
     - Message is displayed if the user has rated book successfully.
     
#### 11. Show all books by a author: (when user clicks on book author on search page)
   * Show all the book by the author.
   * Each book has:
      * Book Title, Book Thumbnail(from Google Books API), Author, Book ISBN.
      * Book reviews:
        - Shows average rating and total number of reviews left by the users in **The BOOK FAIR** .
        - Average rating and total number of reviews from Third-party website **Good reads website** and **Google Books**.
        - Hyperlinks to each of the website.
        

### Back-end Flask application using Python:
---------------------------------------------

#### 12. application.py :

   i. Python application where the webpage routing, error handling, user session information, api requests, DB connection, and SQL queries to the databases are made.
      -imports flask, sqlalchemy,requests,json etc.

#### 13. import.py :

   i. Reads a csv file- 'books.csv' that consist of book information and store those information to the table 'books'. 


#### 14. message.html:
   i. Displays review messages from book page and application.py


### Stylesheets:
-----------------

#### 15. static/css/main.css:
    i. Styling format for entire webpage.
      
      
#### 16. requirements.txt:
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

