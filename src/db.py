#!/usr/bin/env python3
from sqlalchemy import create_engine, String, Column, Integer
from sqlalchemy.ext.declarative import declarative_base

client_types = ['pravnicka_osoba', 'fyzicka_osoba']
Base = declarative_base()

class Client(Base):
    __tablename__ = "klienti"

    id      = Column("klient_id", Integer, primary_key=True)
    name    = Column("knazov", String)
    ico     = Column("kico", String)
    zruseny = Column(String)

class Contact(Base):
    __tablename__ = "klient_kontakt"

    id           = Column("kkontakt_id", Integer)
    client_id    = Column("kklient_id", Integer)
    name         = Column("kkmeno", String)
    phone_number = Column("kktel", String)
    email        = Column("kkemail", String)
