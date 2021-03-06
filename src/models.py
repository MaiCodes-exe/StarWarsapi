from flask_sqlalchemy import SQLAlchemy
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    planets_favorites = relationship('FavoritePlanets', backref='Users', lazy=True)
    people_favorites = relationship('FavoritePeople', backref='Users', lazy=True)

    def __repr__(self):
        return '<Users %r>' % self.id


    @classmethod 
    def get_users(cls,id):
        users = cls.query.get(id)
        return users

    @classmethod
    def get_utl(cls):
        return cls.query.all()

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class People(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(200))
    height= db.Column(db.Integer)
    gender= db.Column(db.String(50))
    birth_year= db.Column(db.Integer)
    people_favorites = relationship('FavoritePeople', backref='People', lazy=True)

    def __repr__(self):
        return '<People %r>' % self.name

    @classmethod 
    def get_people(cls,id):
        people = cls.query.get(id)
        return people

    @classmethod
    def get_peeps(cls):
        return cls.query.all()

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "birth_year": self.birth_year

            # do not serialize the password, its a security breach
        }

class Planets(db.Model):   
    id= Column(Integer, primary_key=True)
    name= Column(String(200))
    climate= Column(String(200))
    terrain= Column(String(200))
    population= Column(Integer)
    planets_favorites = relationship('FavoritePlanets', backref='Planets', lazy=True)


    def __repr__(self):
        return '<Planets %r>' % self.name

    @classmethod 
    def get_by_id(cls,id):
        planet = cls.query.get(id)
        return planet

    @classmethod
    def get_planets(cls):
        return cls.query.all()

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain
            # do not serialize the password, its a security breach
        }

class FavoritePlanets(db.Model):
    id= Column(Integer, primary_key=True)
    name= Column(String(200))
    users_id= Column(Integer, ForeignKey('users.id'))
    planets_id= Column(Integer, ForeignKey('planets.id'))

    def __repr__(self):
        return '<FavoritePlanets %r>' % self.name

    @classmethod 
    def get_fav_planet(cls,id):
        fav_planet = cls.query.get(id)
        return fav_planet


    @classmethod
    def get_fav_planets(cls):
        return cls.query.all()

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "planet_id": self.planets_id,
            "users_id": self.users_id
            # do not serialize the password, its a security breach
        }

class FavoritePeople(db.Model):
    id= Column(Integer, primary_key=True)
    name= Column(String(200))
    users_id= Column(Integer, ForeignKey('users.id'))
    people_id= Column(Integer, ForeignKey('people.id'))

    def __repr__(self):
        return '<FavoritePeople %r>' % self.name

    @classmethod 
    def get_fav_people(cls,id):
        fav_people = cls.query.get(id)
        return fav_people

    @classmethod
    def get_fav_peeps(cls):
        return cls.query.all()

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "users_id": self.users_id
            # do not serialize the password, its a security breach
        }