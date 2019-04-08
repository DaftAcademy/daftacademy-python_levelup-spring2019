# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, Table, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Artist(Base):
    __tablename__ = 'artist'

    artist_id = Column(Integer, primary_key=True, server_default=text("nextval('artist_artist_id_seq'::regclass)"))
    name = Column(String(120))


class Employee(Base):
    __tablename__ = 'employee'

    employee_id = Column(Integer, primary_key=True, server_default=text("nextval('employee_employee_id_seq'::regclass)"))
    last_name = Column(String(20), nullable=False)
    first_name = Column(String(20), nullable=False)
    title = Column(String(30))
    reports_to = Column(ForeignKey('employee.employee_id'), index=True)
    birth_date = Column(DateTime)
    hire_date = Column(DateTime)
    address = Column(String(70))
    city = Column(String(40))
    state = Column(String(40))
    country = Column(String(40))
    postal_code = Column(String(10))
    phone = Column(String(24))
    fax = Column(String(24))
    email = Column(String(60))

    parent = relationship('Employee', remote_side=[employee_id])


class Genre(Base):
    __tablename__ = 'genre'

    genre_id = Column(Integer, primary_key=True, server_default=text("nextval('genre_genre_id_seq'::regclass)"))
    name = Column(String(120))


class MediaType(Base):
    __tablename__ = 'media_type'

    media_type_id = Column(Integer, primary_key=True, server_default=text("nextval('mediatype_mediatype_id_seq'::regclass)"))
    name = Column(String(120))


class Playlist(Base):
    __tablename__ = 'playlist'

    playlist_id = Column(Integer, primary_key=True, server_default=text("nextval('playlist_playlist_id_seq'::regclass)"))
    name = Column(String(120))

    tracks = relationship('Track', secondary='playlist_track')


class Album(Base):
    __tablename__ = 'album'

    album_id = Column(Integer, primary_key=True, server_default=text("nextval('album_album_id_seq'::regclass)"))
    title = Column(String(160), nullable=False)
    artist_id = Column(ForeignKey('artist.artist_id'), nullable=False, index=True)

    artist = relationship('Artist')


class Customer(Base):
    __tablename__ = 'customer'

    customer_id = Column(Integer, primary_key=True, server_default=text("nextval('customer_customer_id_seq'::regclass)"))
    first_name = Column(String(40), nullable=False)
    last_name = Column(String(20), nullable=False)
    company = Column(String(80))
    address = Column(String(70))
    city = Column(String(40))
    state = Column(String(40))
    country = Column(String(40))
    postal_code = Column(String(10))
    phone = Column(String(24))
    fax = Column(String(24))
    email = Column(String(60), nullable=False)
    support_rep_id = Column(ForeignKey('employee.employee_id'), index=True)

    support_rep = relationship('Employee')


class Invoice(Base):
    __tablename__ = 'invoice'

    invoice_id = Column(Integer, primary_key=True, server_default=text("nextval('invoice_invoice_id_seq'::regclass)"))
    customer_id = Column(ForeignKey('customer.customer_id'), nullable=False, index=True)
    invoice_date = Column(DateTime, nullable=False)
    billing_address = Column(String(70))
    billing_city = Column(String(40))
    billing_state = Column(String(40))
    billing_country = Column(String(40))
    billing_postal_code = Column(String(10))
    total = Column(Numeric(10, 2), nullable=False)

    customer = relationship('Customer')


class Track(Base):
    __tablename__ = 'track'

    track_id = Column(Integer, primary_key=True, server_default=text("nextval('track_track_id_seq'::regclass)"))
    name = Column(String(200), nullable=False)
    album_id = Column(ForeignKey('album.album_id'), index=True)
    media_type_id = Column(ForeignKey('media_type.media_type_id'), nullable=False, index=True)
    genre_id = Column(ForeignKey('genre.genre_id'), index=True)
    composer = Column(String(220))
    milliseconds = Column(Integer, nullable=False)
    bytes = Column(Integer)
    unit_price = Column(Numeric(10, 2), nullable=False)

    album = relationship('Album')
    genre = relationship('Genre')
    media_type = relationship('MediaType')


class InvoiceLine(Base):
    __tablename__ = 'invoice_line'

    invoice_line_id = Column(Integer, primary_key=True, server_default=text("nextval('invoiceline_invoiceline_id_seq'::regclass)"))
    invoice_id = Column(ForeignKey('invoice.invoice_id'), nullable=False, index=True)
    track_id = Column(ForeignKey('track.track_id'), nullable=False, index=True)
    unit_price = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False)

    invoice = relationship('Invoice')
    track = relationship('Track')


t_playlist_track = Table(
    'playlist_track', metadata,
    Column('playlist_id', ForeignKey('playlist.playlist_id'), primary_key=True, nullable=False),
    Column('track_id', ForeignKey('track.track_id'), primary_key=True, nullable=False, index=True)
)
