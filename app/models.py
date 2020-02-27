# -*- coding: utf-8 -*-
"""
description: models and database session object
"""

from sqlalchemy import create_engine, func, Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship, scoped_session, sessionmaker, joinedload

from app.settings import DB_URI

Base = declarative_base()

Session = sessionmaker(autocommit=False,
                       autoflush=False,
                       bind=create_engine(DB_URI))

db_session = scoped_session(Session)


class TimestampMixin(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)
    created = Column(TIMESTAMP, nullable=False, server_default=func.now())

    @classmethod
    def get_or_create(cls, **kwargs):
        instance = db_session.query(cls).filter_by(**kwargs).first()
        if instance:
            return instance
        else:
            instance = cls(**kwargs)
            db_session.add(instance)
            db_session.commit()
            return instance

    def as_dict(self):
        return {
            c.name: getattr(self, c.name)
            for c in self.__table__.columns
        }


class URL(TimestampMixin, Base):
    url = Column(String(2000))

    texts = relationship("Text")
    images = relationship("Image")

    @classmethod
    def save_images(cls, url, images):
        url_obj = cls.get_or_create(url=url)
        db_session.add_all([Image(url=url_obj, **kwargs) for kwargs in images])
        db_session.commit()

    @classmethod
    def save_text(cls, url, text):
        url_obj = cls.get_or_create(url=url)
        db_session.add(Text(url=url_obj, text=text))
        db_session.commit()

    @classmethod
    def as_dict(cls, url):
        data = db_session.query(cls).options(joinedload('images')).options(joinedload('texts')).filter_by(
            url=url).one_or_none()
        if data:
            url_dict = super().as_dict(data)
            images = {'images': [i.as_dict() for i in data.images]}
            texts = {'texts': [t.as_dict() for t in data.texts]}

            serialized_data = {
                **url_dict,
                **images,
                **texts
            }

            return serialized_data


class Text(TimestampMixin, Base):
    text = Column(String)

    url_id = Column(Integer, ForeignKey('url.id'))
    url = relationship("URL", back_populates="texts")


class Image(TimestampMixin, Base):
    name = Column(String)
    md5 = Column(
        String(32),
        index=True,
    )

    url_id = Column(Integer, ForeignKey('url.id'))
    url = relationship("URL", back_populates="images")
