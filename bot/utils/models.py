from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker



engine = create_engine('sqlite:///mydatabase.db', echo=True)

Base = declarative_base()

class Section(Base):
    __tablename__ = 'sections'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    items = relationship('Item', back_populates='section')

    def __repr__(self):
        return f"<Section(id={self.id}, name='{self.name}')>"
    
class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    photo_path = Column(String, nullable=False)
    section_id = Column(Integer, ForeignKey('sections.id'))
    section = relationship('Section', back_populates='items')

    def __repr__(self):
        return (
            f"<Item(id={self.id}, name='{self.name}', "
            f"description='{self.description}', "
            f"photo_url='{self.photo_path}', section_id={self.section_id})>"
        )

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
