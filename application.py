import os
import requests
import json
import xmltodict
from flask import Flask, session,render_template,request,redirect,url_for,jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from markupsafe import escape

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")
if not os.getenv("GR_key"):
    raise RuntimeError("Good reads key not set")
    

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
key = os.getenv("GR_key")
db = scoped_session(sessionmaker(bind=engine))



@app.route("/")
def index():

    if 'email_id' in session:
        if session['email_id']:
            message = 'Logged in as %s' % session['email_id']
            return render_template ("index.html",message = message)
        else:
            return render_template("login.html",message="you are not logged in")
    else:
        return render_template("login.html",message="you are not logged in")


@app.route("/register", methods=["GET","POST"])
def register():
    if 'email_id' in session:
        if session['email_id']:
            message = 'Logged in as %s' % session['email_id']
            return render_template ("index.html",message = message)

    if request.method == 'POST':
        session['email_id'] = request.form.get("email_id")
        try:
            email_id = request.form.get("email_id")
            password = request.form.get("password")
            name = request.form.get("name")
        except ValueError:
            return render_template("register.html",err_msg="email id or password or name is required")

        if db.execute("select * from users where email_id = :email_id",{"email_id": email_id}).rowcount==0:
        # new user
            db.execute("insert into users(email_id,password,name) values (:email_id,:password, :name)",
            {"email_id":email_id,"password":password,"name":name})
            
            db.commit()
            return redirect(url_for('index'))
        else:
            err_msg = "Sorry,the email address is already registered!"
            session['email_id']=""
            return render_template("register.html",err_msg=err_msg)
    else:
        return render_template("register.html")
        

@app.route("/login", methods=["GET","POST"])
def login():
    if 'email_id' in session:
        if session['email_id']:
            message = 'Logged in as %s' % session['email_id']
            return render_template ("index.html",message = message)

       
            
    if request.method == 'POST':
        session['email_id'] = request.form["email_id"]
        try:
            email_id = request.form["email_id"]
            password = request.form["password"]

        except ValueError:
            return render_template("login.html", err_msg="email id and password is required to login")
        
        user = db.execute("select email_id,password,name from users where email_id=:email_id and password=:password",
        {"email_id": email_id,"password":password}).fetchall()

    
        if len(user) == 0:
            session['email_id']=""
            return render_template("login.html",err_msg="Wrong email id or password!")
        else:     
            for u in user:
                message = 'Logged in as %s' % u.name
                return redirect(url_for('index'))  
    else:

        return render_template("login.html")
    


@app.route("/logout")
def logout():

    session.pop('email_id',None)

    return redirect(url_for('index'))

@app.route("/search",methods=["GET","POST"])
def search():
    if 'email_id' in session:
        if session['email_id']:
            message = 'Logged in as %s' % session['email_id']
        else:
            return render_template("login.html",message="you are not logged in")   
    

    
        if request.method == 'POST':
            query = request.form["search"]
            searchby = request.form['searchvia']

            if query == "":
                return render_template("index.html",search_err="No results",message=message)
        
            else:
                q = f"%{query}%".upper()

                books = db.execute("select isbn,title,author,year from books where upper(isbn) like :isbn or upper(title) like :title or upper(author) like :author ",{"isbn": q,"title":q, "author" :q}).fetchall() 

                average=[]
                if len(books) == 0:
                    return render_template("index.html",search_err_message="No results",message=message)
                for b in books:

                    average_rating = db.execute("select cast (avg(rating) AS DECIMAL(10,2)) from reviews where isbn =:isbn", {"isbn":b.isbn}).fetchall()
 

                    avg =average_rating[0][0]
                    if avg!=None:
                        average.append(avg)
       
                
                return render_template("index.html",books=books,reviews = review,message=message)
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
            message = 'Logged in as %s' % session['email_id']
        else:
            return render_template("login.html",message="you are not logged in")


        b = f"{b}".upper()
        if booksearchby =="title":

            book = db.execute("select isbn,title,author,year from books where upper(title)=:title",{"title":b}).fetchall()
           
        elif booksearchby == "author":
            
            book = db.execute("select isbn,title,author,year from books where upper(author)=:author",{"author":b}).fetchall()
        else:
            return render_template("index.html",search_err= "Internal error",message=message)

        if len(book) == 0:
            return render_template("index.html",search_err= "Internal error",message=message)
        
        #get reviews for that book
        
        for b in book:

           
            
            average_rating = db.execute("select  avg(reviews.rating) as average_score from reviews where isbn =:isbn", {"isbn":b.isbn}).fetchall()
            review = db.execute("select contents, rating,email_id from reviews where isbn =:isbn", {"isbn":b.isbn}).fetchall() 
            
            avg = average_rating[0][0]
            
            if avg==None:
                avg=0
            avg=float('%.2f' %(avg))
            

      
            average.append(avg)
            #book reads api
            response = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": key, "isbns": b.isbn})
            data =response.json()
           
            if response.status_code != 200:
                raise Exception("ERROR: API request unsuccessful.")
            else:
                goodreads_avg.append(data['books'][0]['average_rating'])
                goodreads_numberofrating.append(data['books'][0] ['work_ratings_count'])
        return render_template("book.html",book =book,booksearchby=booksearchby,review=review,average_rating=average,goodreads_avg=goodreads_avg, goodreads_numberofrating=goodreads_numberofrating,message=message)
    else:
        return render_template("login.html",message="you are not logged in")


@app.route("/review/<string:isbn>",methods=["GET","POST"])
def review(isbn):
    if 'email_id' in session:
        if session['email_id']:
            user_email = session['email_id']
            message = 'Logged in as %s' % user_email
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
                    return render_template("book.html",review_sucess = "you have sucessfully submitted your review")
                

                else:
                    
                    if allreviews["review"] != "":
                        
                        rev= db.execute("insert into reviews(contents,isbn,email_id) values (:contents,:isbn,:email_id)",{"contents":allreviews["review"],"isbn":isbn,"email_id":user_email})
                        
                        db.commit()
                        return render_template("book.html",review_sucess = "you have sucessfully submitted your review")
                    else:
                        return render_template("book.html",bookerr = "Validation required",message =message)
            else:
                return render_template("book.html", reviewerr = "You already gave a review")
        else:
            return render_template("login.html",message= " please create an account first")
    else: 
        return render_template("login.html",message="you are not logged in")


@app.route("/api/<isbn>",methods=["GET"])
def book_api(isbn):
    book =db.execute("select count(reviews.email_id) as review_count,books.isbn,title,author,year,avg(reviews.rating) as average_score from books inner join reviews on books.isbn=reviews.isbn where books.isbn=:isbn group by books.isbn,title,author,year",{"isbn":isbn}).fetchone()
    
    if book == None:
        return jsonify({"error": "Invalid isbn number", "status_code":404}),404
    rating=dict(book.items())
    rating['average_score'] =float('%.2f' %(rating['average_score']))
    return jsonify(rating)
    
    
    
    