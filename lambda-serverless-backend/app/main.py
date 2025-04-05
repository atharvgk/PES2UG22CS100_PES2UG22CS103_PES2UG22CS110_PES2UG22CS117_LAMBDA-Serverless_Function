from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import engine, SessionLocal
from .models import Base, Function
from .schemas import FunctionCreate
from .crud import create_function, get_function, get_functions, update_function, delete_function

# Create FastAPI app
app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Lambda Serverless API! 🚀"}

# ✅ Create a Function
@app.post("/functions/", response_model=FunctionCreate)
def create_function_endpoint(function: FunctionCreate, db: Session = Depends(get_db)):
    return create_function(db, function)

# ✅ Get All Functions (with optional pagination)
@app.get("/functions/")
def get_all_functions_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_functions(db, skip=skip, limit=limit)

# ✅ Get Function by ID
@app.get("/functions/{function_id}")
def get_function_endpoint(function_id: int, db: Session = Depends(get_db)):
    function = get_function(db, function_id)
    if not function:
        raise HTTPException(status_code=404, detail="Requested function does not exist")
    return function

# ✅ Update a Function
@app.put("/functions/{function_id}")
def update_function_endpoint(function_id: int, function: FunctionCreate, db: Session = Depends(get_db)):
    existing_function = get_function(db, function_id)
    if not existing_function:
        raise HTTPException(status_code=404, detail="Function not found")
    
    for key, value in function.dict().items():
        setattr(existing_function, key, value)
    
    db.commit()
    db.refresh(existing_function)
    return existing_function

# ✅ Delete a Function
@app.delete("/functions/{function_id}")
def delete_function_endpoint(function_id: int, db: Session = Depends(get_db)):
    deleted = delete_function(db, function_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Function not found")
    return {"message": "Function deleted successfully"}