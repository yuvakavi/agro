import streamlit as st
from supabase import create_client, Client
import os

def get_supabase_client() -> Client:
    """Create and return Supabase client"""
    try:
        url = st.secrets["supabase_url"]
        key = st.secrets["supabase_key"]
        supabase: Client = create_client(url, key)
        return supabase
    except Exception as e:
        st.error(f"❌ Supabase client creation failed: {e}")
        return None

def setup_database():
    """Create users table in Supabase using SQL"""
    try:
        supabase = get_supabase_client()
        if not supabase:
            return False
        
        # Execute raw SQL to create table
        result = supabase.rpc('exec_sql', {
            'sql': '''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT NOW()
            );
            '''
        }).execute()
        
        st.success("✅ Database setup completed!")
        return True
        
    except Exception as e:
        # If RPC doesn't work, the table might already exist
        st.info("ℹ️ Database table setup - table may already exist")
        return True

def register_user(name, password):
    """Register a new user using Supabase"""
    if not name or not password:
        st.error("❌ Name and password are required")
        return False
        
    if len(password) < 6:
        st.error("❌ Password must be at least 6 characters")
        return False
        
    try:
        supabase = get_supabase_client()
        if not supabase:
            return False
        
        # Insert user into Supabase
        data = {
            "name": name.strip(),
            "password": password,
            "created_at": "now()"
        }
        
        result = supabase.table("users").insert(data).execute()
        
        if result.data:
            st.success(f"✅ User '{name}' registered successfully!")
            return True
        else:
            st.error("❌ Registration failed")
            return False
            
    except Exception as e:
        if "duplicate key" in str(e).lower():
            st.error(f"❌ User '{name}' already exists!")
        else:
            st.error(f"❌ Registration failed: {e}")
        return False

def validate_login(name, password):
    """Validate user login using Supabase"""
    if not name or not password:
        return None
        
    try:
        supabase = get_supabase_client()
        if not supabase:
            return None
        
        # Query user from Supabase with correct syntax
        result = supabase.table("users") \
            .select("id", "name") \
            .eq("name", name.strip()) \
            .eq("password", password) \
            .execute()
        
        if result.data and len(result.data) > 0:
            user_data = result.data[0]
            return user_data
        else:
            st.error("❌ Invalid username or password")
            return None
            
    except Exception as e:
        st.error(f"❌ Login validation error: {e}")
        return None

def get_user_count():
    """Get total number of registered users"""
    try:
        supabase = get_supabase_client()
        if not supabase:
            return 0
        
        result = supabase.table("users").select("id", count="exact").execute()
        return result.count if result.count else 0
        
    except Exception:
        return 0

def get_all_users():
    """Get all users (admin function)"""
    try:
        supabase = get_supabase_client()
        if not supabase:
            return []
        
        result = supabase.table("users").select("id, name, created_at").execute()
        return result.data if result.data else []
        
    except Exception:
        return []

def test_supabase_connection():
    """Test Supabase connection"""
    try:
        supabase = get_supabase_client()
        if not supabase:
            st.error("❌ Failed to create Supabase client!")
            return False
        
        # Test connection by querying users table
        result = supabase.table("users").select("count", count="exact").execute()
        
        st.success("✅ Supabase connection successful!")
        st.info(f"👥 Total users in database: {result.count}")
        return True
        
    except Exception as e:
        st.error(f"❌ Supabase connection test failed: {e}")
        return False

# Auto-setup database
if __name__ != "__main__":
    setup_database()







