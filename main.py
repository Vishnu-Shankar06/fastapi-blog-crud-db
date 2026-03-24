from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from schemas import PostCreate, PostResponse, PostUpdate
from database import engine, SessionLocal, Base
from models import Post
from sqlalchemy.orm import Session

app = FastAPI()
templates = Jinja2Templates(directory="templates")
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@app.get("/")
def home(request:Request,db:Session=Depends(get_db)):
    posts = db.query(Post).all()

    return templates.TemplateResponse(
        "home.html",{"request":request, "posts":posts})

@app.get("/post/{post_id}")
def part(request:Request, post_id:int,db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id==post_id).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post Not found")
            
    return templates.TemplateResponse(
        "post.html", {"request":request, "post":post})

    

@app.get("/create")
def create_page(request:Request):
    return templates.TemplateResponse(
        "create.html",{"request":request})

@app.post("/create")
def create_post_html(request:Request,title:str=Form(...),
                     content:str=Form(...),db:Session=Depends(get_db)):
    errors = {}
    clean_title = title.strip()
    clean_content = content.strip()

    if not clean_title:
        errors["title"] = "Title cannot be empty"
    elif (len(clean_title)) < 3:
        errors["title"] = "Need more Characters"

    if not clean_content:
        errors["content"] = "Content cannot be empty"
    elif (len(clean_content)) < 7:
        errors["content"] = "Need more Characters"

    if errors:
        return templates.TemplateResponse(
            "create.html",{"request":request,"title":clean_title,
                           "errors":errors,"content":clean_content},
            status_code=400)

    new_post = Post(title=clean_title,content=clean_content)

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return RedirectResponse(url="/", status_code=303)

@app.post("/post/{post_id}/delete")
def delete_post_html(request:Request, post_id:int, db:Session=Depends(get_db)):

    post = db.query(Post).filter(Post.id == post_id).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    db.delete(post)
    db.commit()

    return RedirectResponse(url="/", status_code=303)

@app.get("/post/{post_id}/edit")
def edit_page(request:Request,post_id:int,db:Session=Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return templates.TemplateResponse(
        "edit.html",{"request":request,"post":post})

@app.post("/post/{post_id}/edit")
def edit_post(request:Request,post_id:int,title:str=Form(...),
              content:str=Form(...),db:Session=Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found") 
  
    errors = {}
    clean_title = title.strip()
    clean_content = content.strip()

    if not clean_title:
        errors["title"] = "Title cannot be empty"
    elif (len(clean_title)) < 3:
        errors["title"] = "Need more Characters"

    if not clean_content:
        errors["content"] = "Content cannot be empty"
    elif (len(clean_content)) < 7:
        errors["content"] = "Need more Characters"

    if errors:
        return templates.TemplateResponse(
            "edit.html",{"request":request,"errors":errors,"post":post},
            status_code=400)

    post.title = clean_title
    post.content = clean_content
    db.commit()
    db.refresh(post)

    return RedirectResponse(url="/",status_code=303)

@app.exception_handler(StarletteHTTPException)
def http_exception_handler(request:Request, exc:StarletteHTTPException):
    return templates.TemplateResponse(
        "error.html",{"request":request, "status_code":exc.status_code,"detail":exc.detail},
        status_code=exc.status_code)

@app.exception_handler(RequestValidationError)
def validation_exception_handler(request:Request,exc:RequestValidationError):   
    if request.url.path.startswith("/api"):
        return JSONResponse(status_code=422,
            content={"detail": exc.errors()})

    return templates.TemplateResponse("error.html",
        {"request": request,"status_code": 400,
        "detail": "Invalid Input"},status_code=400)

# API Routes

@app.get("/api/posts", response_model=list[PostResponse])
def get_posts(db:Session=Depends(get_db)):
    return db.query(Post).all()

@app.get("/api/posts/{post_id}", response_model=PostResponse)
def get_post(post_id:int, db:Session=Depends(get_db)):
    post = db.query(Post).filter(Post.id== post_id).first()

    if not post:
        raise HTTPException(status_code=404,detail="Post not found")
    
    return post

@app.post("/api/posts", response_model=PostResponse)
def create_post_api(post:PostCreate, db:Session=Depends(get_db)):
    new_post = Post(title=post.title,
                    content=post.content)

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.put("/api/posts/{post_id}", response_model=PostResponse)
def update_post(post_id:int,updated_post:PostCreate, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    post.title = updated_post.title
    post.content = updated_post.content

    db.commit()
    db.refresh(post)

    return post

@app.patch("/api/posts/{post_id}",response_model=PostResponse)
def patch_post(post_id:int,updated_post:PostUpdate, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id==post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if updated_post.title is not None:
        post.title = updated_post.title

    if updated_post.content is not None:
        post.content = updated_post.content

    db.commit()
    db.refresh(post)

    return post

@app.delete("/api/posts/{post_id}")
def delete_post_api(post_id:int, db: Session = Depends(get_db)):

    post = db.query(Post).filter(Post.id==post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    db.delete(post)
    db.commit()
    return {"message":"Deleted Successfully"}