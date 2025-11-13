from fastapi import FastAPI, Response, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from database import start_db, get_db_connection, encrypt_password
app = FastAPI()
start_db()

class Register (BaseModel):
    username: str
    password: str
    mobile: int

class Login(BaseModel):
    username: str
    password: str

class Update(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    mobile: Optional[int] = None
    
@app.get("/")
async def root():
    return Response(status_code=200)

@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: Register):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id FROM users WHERE username = ?", (user.username,))
        if cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
            )
        
        if len(str(user.mobile)) != 10:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Mobile number must be exactly 10 digits"
            )
        
        encrypted_password = encrypt_password(user.password)
        cursor.execute(
            "INSERT INTO users (username, password, mobile) VALUES (?, ?, ?)",
            (user.username, encrypted_password, user.mobile)
        )
        conn.commit()
        user_id = cursor.lastrowid
        
        cursor.execute("SELECT id, username, mobile FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        return {
            "id": int(row["id"]),
            "username": row["username"],
            "mobile": int(row["mobile"])
        }
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error registering user: {str(e)}"
        )
    finally:
        conn.close()

@app.post("/login", status_code=status.HTTP_200_OK)
async def login(user: Login):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id, username, password, mobile FROM users WHERE username = ?", (user.username,))
        user_data = cursor.fetchone()
        
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )
        
        encrypted_password = encrypt_password(user.password)
        if user_data["password"] != encrypted_password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )
        
        return {
            "id": int(user_data["id"]),
            "username": user_data["username"],
            "mobile": int(user_data["mobile"]),
            "message": "Login successful"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during login: {str(e)}"
        )
    finally:
        conn.close()

@app.get("/users", status_code=status.HTTP_200_OK)
async def get_all_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id, username, mobile FROM users")
        rows = cursor.fetchall()
        
        users = []
        for row in rows:
            users.append({
                "id": int(row["id"]),
                "username": row["username"],
                "mobile": int(row["mobile"])
            })
        
        return {"users": users, "count": len(users)}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching users: {str(e)}"
        )
    finally:
        conn.close()

@app.get("/users/{id}", status_code=status.HTTP_200_OK)
async def get_user(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id, username, mobile FROM users WHERE id = ?", (id,))
        row = cursor.fetchone()
        
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return {
            "id": int(row["id"]),
            "username": row["username"],
            "mobile": int(row["mobile"])
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching user: {str(e)}"
        )
    finally:
        conn.close()

@app.put("/users/{id}", status_code=status.HTTP_200_OK)
async def update_user(id: int, user_update: Update):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id FROM users WHERE id = ?", (id,))
        if not cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        update_fields = []
        update_values = []
        
        if user_update.username is not None and user_update.username != "" and user_update.username != "string":
            cursor.execute("SELECT id FROM users WHERE username = ? AND id != ?", (user_update.username, id))
            if cursor.fetchone():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already exists"
                )
            update_fields.append("username = ?")
            update_values.append(user_update.username)
        
        if user_update.password is not None and user_update.password != "" and user_update.password != "string":
            encrypted_password = encrypt_password(user_update.password)
            update_fields.append("password = ?")
            update_values.append(encrypted_password)
        
        if user_update.mobile is not None and user_update.mobile != 0:
            if len(str(user_update.mobile)) != 10:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Mobile number must be exactly 10 digits"
                )
            update_fields.append("mobile = ?")
            update_values.append(user_update.mobile)
        
        if not update_fields:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields to update"
            )
        
        update_values.append(id)
        query = f"UPDATE users SET {', '.join(update_fields)} WHERE id = ?"
        cursor.execute(query, update_values)
        conn.commit()
        
        cursor.execute("SELECT id, username, mobile FROM users WHERE id = ?", (id,))
        row = cursor.fetchone()
        
        return {
            "id": int(row["id"]),
            "username": row["username"],
            "mobile": int(row["mobile"]),
            "message": "User updated successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating user: {str(e)}"
        )
    finally:
        conn.close()

@app.delete("/users/{id}", status_code=status.HTTP_200_OK)
async def delete_user(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id, username FROM users WHERE id = ?", (id,))
        row = cursor.fetchone()
        
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        cursor.execute("DELETE FROM users WHERE id = ?", (id,))
        conn.commit()
        
        return {
            "message": f"User '{row['username']}' deleted successfully",
            "deleted_id": id
        }
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting user: {str(e)}"
        )
    finally:
        conn.close()


