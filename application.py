import os
import requests
import json
from flask import Flask, session,render_template,request,redirect,url_for,jsonify,flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")



# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
gr_key=os.getenv("GR_key")

db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():

    if 'email_id' in session:
        if session['email_id']:
            if session['name']:
                message = 'Logged in as %s' % session['name']
                return render_template ("index.html",account_details = message)
        else:
            return render_template("login.html",message="you are not logged in")
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET","POST"])
def register():
    if 'email_id' in session:
        if session['email_id']:
            if session['name']:
                message = 'Logged in as %s' % session['name']
                return render_template ("index.html",message = message)

    if request.method == 'POST':
        try:
            email_id = request.form.get("email_id")
            password = request.form.get("password")
            name = request.form.get("name")
            confirm_password = request.form.get("confirmpassword")

        except ValueError:
            return render_template("register.html",err_msg="email id or password or name is required")
        


        if not len(password)>=6:
            password_length_err_msg = "Password length must be atleast 6 characters"
            error ="PASSWORD_LENGTH_ERROR"
            return render_template("register.html",err_msg=password_length_err_msg,type_err_msg= error,email = email_id,name=name)
        
        #password match

        if password!=confirm_password:
            confirm_password_err_msg = "Password did not match"
            error = 'PASSWORD_NOT_MATCH'
            return render_template("register.html",err_msg=confirm_password_err_msg,type_err_msg= error, email = email_id,name=name)

        if db.execute("select * from users where email_id = :email_id",{"email_id": email_id}).rowcount==0:
        # new user
            db.execute("insert into users(email_id,password,name) values (:email_id,:password, :name)",
            {"email_id":email_id,"password":password,"name":name})
            
            db.commit()
            flash(u'Welcome , You were successfully registered. ')
            session['email_id']=email_id
            session['name']=name
            return redirect(url_for('index'))

        else:
            
            session['email_id']=""
            session['name']=""
            email_address_not_available_err_msg = "Sorry,the email address is already registered!"
            error = 'email_error'
           
            return render_template("register.html",err_msg=email_address_not_available_err_msg,type_err_msg= error)
    else:
        return render_template("register.html")
        

@app.route("/login", methods=["GET","POST"])
def login():
    if 'email_id' in session:
        if session['email_id']:
            if session['name']:
                message = 'Logged in as %s' % session['name']
                return render_template ("index.html",account_details = message)

       
            
    if request.method == 'POST':
        
        email_id = request.form["email_id"]
        password = request.form["password"]
        
        
        users  = db.execute("select email_id,password,name from users where email_id=:email_id",{"email_id": email_id}).fetchall()
        
        if len(users)== 0:
            email_not_found = 'User not found'
            error ="EMAIL_NOT_FOUND"
            return render_template("login.html",err_msg=email_not_found,type_err_msg= error)
        else:
            for u in users:
                if u.email_id == email_id and u.password == password:
                    session['name']= u.name 
                    session['email_id']=u.email_id
                    return redirect(url_for('index'))  
                else:
                    wrong_password = 'Wrong Password'
                    error ="WRONG_PASSWORD"
                    return render_template("login.html",err_msg=wrong_password,type_err_msg= error,email = u.email_id)
    else:

        return render_template("login.html")


@app.route("/verifyaccount",methods=["GET","POST"])
def verifyaccount():
    if 'email_id' in session:
        if session['email_id']:
            if session['name']:
                message = 'Logged in as %s' % session['name']
                return render_template ("index.html",account_details = message)

    if request.method == 'POST':
        try:
            email_id = request.form.get("email_id")
        except ValueError:
            return render_template("oldaccount.html",err_msg="email id is required")

        user  = db.execute("select * from users where email_id=:email_id",{"email_id": email_id}).fetchall()
        if len(user)== 0:
            email_not_found = 'Email address not found'
            error ="EMAIL_NOT_FOUND"
            return render_template("oldaccount.html",err_msg=email_not_found,type_err_msg=error)
        else:
            for u in user:
                if u.email_id==email_id:
                    verification_status = 1
                    flash(u'Account verified sucessfully.')
                    return render_template("change_password.html",email=email_id,verification_status=1)
    else:
        return render_template("oldaccount.html")

@app.route("/changepassword/<int:verification_status>",methods=["GET","POST"])
def changepassword(verification_status):
    if 'email_id' in session:
        if session['email_id']:
            if session['name']:
                message = 'Logged in as %s' % session['name']
                return render_template ("index.html",account_details = message)

    if request.method == 'POST':
        
        try:
            email_id = request.form.get("email_id")
            new_password = request.form.get("password")
            confirm_password = request.form.get("confirmpassword")

        except ValueError:
            return render_template("change_password.html",err_msg="email id or password is required",verification_status=verification_status)
        
        user = db.execute("select * from users where email_id = :email_id",{"email_id": email_id}).fetchall()

        if len(user) == 0:
            email_not_found = 'Email Address not found'
            error ="EMAIL_NOT_FOUND"
            return render_template("change_password.html",err_msg=email_not_found,type_err_msg= error,verification_status=verification_status)

        if not len(new_password)>=6:
            password_length_err_msg = "Password length must be atleast 6 characters"
            error ="PASSWORD_LENGTH_ERROR"
            return render_template("change_password.html",err_msg=password_length_err_msg,type_err_msg= error,email = email_id,verification_status=verification_status)
        
        if new_password!=confirm_password:
            confirm_password_err_msg = "Password did not match"
            error = 'PASSWORD_NOT_MATCH'
            return render_template("change_password.html",err_msg=confirm_password_err_msg,type_err_msg= error, email = email_id,verification_status=verification_status) 


        
        for u in user:
            if u.email_id == email_id:
               
                db.execute("update  users set password=:password where email_id=:email_id",{"password":new_password,"email_id":email_id})
                db.commit()
                flash(u'Welcome ,You changed your password successfully')
                return render_template("login.html")
    else:
       return render_template("change_password.html")

@app.route("/logout")
def logout():

    session.pop('email_id',None)
    session.pop('name',None)
    flash(u'Logged out successfully')
    return redirect(url_for('index'))

@app.route("/search",methods=["GET","POST"])
def search():
    if 'email_id' in session:
        if session['email_id']:
            if session['name']:
                message = 'Logged in as %s' % session['name']
        else:
            return render_template("login.html",message="you are not logged in")   
    

    
        if request.method == 'POST':
            query = request.form["search"]
            searchby = request.form['searchvia']

            if query == "":
                error ="No results"
                return render_template("index.html",error = error, account_details=message)
        
            else:
                query=query.strip()
                q1 = f"%{query}%".upper()
                search_msg= "Showing results"
                search_msg_no_results =""

                books = db.execute("select isbn,title,author,year from books where upper(isbn) like :isbn or upper(title) like :title or upper(author) like :author ",{"isbn": q1,"title":q1, "author" :q1}).fetchall() 

                if len(books)== 0:
                    search_msg_no_results +='No results found for'
                    q2=""
                    if len(query)>0:
                        q2=query[0]
                        for i in range(1,len(query)):
                            q2+="%"
                        q2 = f"{q2}".upper()

                        books = db.execute("select isbn,title,author,year from books where upper(isbn) like :isbn or upper(title) like :title or upper(author) like :author ",{"isbn": q2,"title":q2, "author" :q2}).fetchall() 
                    
                

                average=[]
                if len(books) == 0:
                    error ="No books found"
                    return render_template("index.html",error=error,account_details=message)
                for b in books:

                    average_rating = db.execute("select cast (avg(rating) AS DECIMAL(10,2)) from reviews where isbn =:isbn", {"isbn":b.isbn}).fetchall()

                    bookname =b.title
                    avg =average_rating[0][0]
                    if avg!=None:
                        average.append(avg)
    
            
                    return render_template("index.html",books=books,account_details=message,search_msg=search_msg,search_msg_no_results=search_msg_no_results,query=query,bookname=bookname)
        else:
            return redirect(url_for('index'))
    else:
        return render_template("login.html",message="you are not logged in")

@app.route("/books/<string:b>/<booksearchby>",methods=["GET"])
def books(b,booksearchby):  
    average = []
    goodreads_avg=[]
    goodreads_numberofrating=[]
    if 'email_id' in session:
        if session['email_id']:
            if session['name']:
                message = 'Logged in as %s' % session['name']
        else:
            return render_template("login.html",message="you are not logged in")

        
        b = f"{b}".upper()
        
        if booksearchby =="title":

            book = db.execute("select isbn,title,author,year from books where upper(title)=:title",{"title":b}).fetchall()
            
        elif booksearchby == "author":
            
            book = db.execute("select isbn,title,author,year from books where upper(author)=:author",{"author":b}).fetchall()
        else:
            return render_template("index.html",search_err= "Internal error",account_details=message)

        if len(book) == 0:
            return render_template("index.html",search_err= "Internal error",account_details=message)
        
        #get reviews for that book
        
        for b in book:
            average_rating = db.execute("select  avg(reviews.rating) as average_score from reviews where isbn =:isbn", {"isbn":b.isbn}).fetchall()
            review = db.execute("select contents, rating,reviews.email_id,name from reviews inner join users on users.email_id=reviews.email_id  where isbn =:isbn ", {"isbn":b.isbn}).fetchall() 
            
            avg = average_rating[0][0]
            
            if avg==None:
                avg=0
            avg=float('%.2f' %(avg))
            average.append(avg)

            #book reads api
            if not os.getenv("GR_key"):
                raise RuntimeError("Good reads key not set")

            gr_key=os.getenv("GR_key")
            response = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": gr_key, "isbns": b.isbn})
            
            
           
            if response.status_code == 200:
                data =response.json()
                goodreads_avg.append(data['books'][0]['average_rating'])
                goodreads_numberofrating.append(data['books'][0] ['work_ratings_count'])
    
        return render_template("book.html",book=book,  booksearchby=booksearchby,review=review,average_rating=average,goodreads_avg=goodreads_avg, goodreads_numberofrating=goodreads_numberofrating,account_details=message)
    else:
        return render_template("login.html",message="you are not logged in")


        

@app.route("/review/<string:isbn>",methods=["GET","POST"])
def review(isbn):
    if 'email_id' in session:
        if session['email_id']:
            if session['name']:
                user_email=session['email_id']
                message = 'Logged in as %s' % session['name']
        else:
            return render_template("login.html",message="you are not logged in")

        #review =[]
        allreviews = dict()
        value = request.values 
        userReview=request.form['review']
        for item in value.items():
            allreviews[item[0]]=item[1]

        
        key ="'rating'"
        
        if db.execute("select email_id from users where email_id=:email_id",{"email_id":user_email}).rowcount !=0: 
            
            if db.execute("select isbn,email_id from reviews where isbn=:isbn and email_id=:email_id ",{"isbn":isbn,"email_id":user_email}).rowcount == 0:
                #user's first and only review
                if 'rating' in allreviews.keys():
                    rev= db.execute("insert into reviews(contents,rating,isbn,email_id) values (:contents,:rating,:isbn,:email_id)",{"contents":allreviews["review"],"rating":allreviews["rating"],"isbn":isbn,"email_id":user_email})
                    db.commit()
                    return render_template("book.html",review_sucess = "You have sucessfully submitted your review",account_details =message)
                

                else:
                    
                    if allreviews["review"] != "":
                        
                        rev= db.execute("insert into reviews(contents,isbn,email_id) values (:contents,:isbn,:email_id)",{"contents":allreviews["review"],"isbn":isbn,"email_id":user_email})
                        
                        db.commit()
                        return render_template("book.html",review_sucess = "You have sucessfully submitted your review",account_details =message)
                    else:
                        return render_template("book.html",emptyreview = "You cannot give an empty rating and comment",account_details =message)
            else:
                return render_template("book.html", reviewerr = "You already gave a review",account_details =message)
        else:
            return render_template("login.html",message= " please create an account first")
    else: 
        return render_template("login.html",message="you are not logged in")


@app.route("/api/<isbn>",methods=["GET"])
def book_api(isbn):
   
    #book =db.execute("select count(reviews.email_id) as review_count,books.isbn,title,author,year,avg(reviews.rating) as average_score from books inner join reviews on books.isbn=reviews.isbn where books.isbn=:isbn group by books.isbn,title,author,year",{"isbn":isbn}).fetchone()
    book =db.execute("select count(reviews.email_id) as review_count,books.isbn,title,author,year,avg(reviews.rating) as average_score from books left join reviews on books.isbn=reviews.isbn where books.isbn=:isbn group by books.isbn",{"isbn":isbn}).fetchone()
    if book == None:
        return jsonify({"error": "Invalid isbn number", "status_code":404}),404

    rating=dict(book.items())
    if rating['average_score'] != None:
        rating['average_score'] =float('%.2f' %(rating['average_score']))  
    
    if rating['average_score'] == None:
        rating['average_score']=0
    return jsonify(rating)
    
@app.route("/myreviews")
def myreviews():
    if 'email_id' in session:
        if session['email_id']:
            if session['name']:
                user_email=session['email_id']
                message = 'Logged in as %s' % session['name']
        else:
            return render_template("login.html",message="you are not logged in")

        allreviews = db.execute("select reviews.isbn,rating,contents,title from reviews inner join books on books.isbn=reviews.isbn  where email_id=:email_id",{"email_id":user_email}).fetchall()
        if len(allreviews) ==0:
            no_reviews_found_msg = "No reviews found"
            return render_template("myreviews.html", account_details=message,err_msg=no_reviews_found_msg)
        else:
            
           
            return render_template("myreviews.html",reviews=allreviews,account_details=message)
    else: 
        return render_template("login.html",message="you are not logged in")

        
    
    

    
    

