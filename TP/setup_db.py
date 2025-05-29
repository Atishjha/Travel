#!/usr/bin/env python3
"""
Database setup script for the Travel Planning App
Run this script to initialize the database with tables
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
import secrets
import os

# Create Flask app instance
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///travel_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.email}>'

# Trip model
class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100))
    start_date = db.Column(db.String(50), nullable=False)
    end_date = db.Column(db.String(50), nullable=False)
    budget = db.Column(db.Float, nullable=False)
    num_people = db.Column(db.Integer, nullable=False)
    interests = db.Column(db.Text)  # Store as comma-separated string
    itinerary = db.Column(db.Text)  # Store the generated itinerary
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Trip {self.destination} for User {self.user_id}>'

def create_database():
    """Create all database tables"""
    with app.app_context():
        # Drop all tables (only for development - removes all data!)
        # db.drop_all()
        
        # Create all tables
        db.create_all()
        
        print("✅ Database tables created successfully!")
        print(f"📁 Database file location: {os.path.abspath('travel_app.db')}")
        
        # Check if tables exist
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"📋 Created tables: {', '.join(tables)}")

def add_sample_data():
    """Add some sample data for testing (optional)"""
    with app.app_context():
        # Check if we already have users
        if User.query.first():
            print("⚠️  Sample data already exists. Skipping...")
            return
        
        # Create a sample user
        sample_user = User(email='test@example.com')
        sample_user.set_password('password123')
        
        db.session.add(sample_user)
        db.session.commit()
        
        print("✅ Sample user created:")
        print("   Email: test@example.com")
        print("   Password: password123")

if __name__ == '__main__':
    print("🚀 Setting up Travel Planning App Database...")
    print("=" * 50)
    
    create_database()
    
    # Uncomment the next line if you want sample data
    # add_sample_data()
    
    print("=" * 50)
    print("✅ Database setup complete!")
    print("\n📝 Next steps:")
    print("1. Set up email environment variables")
    print("2. Run your Flask app: python app.py")