from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import ForeignKey, String, BIGINT, TIMESTAMP, DateTime, BOOLEAN

class Base(DeclarativeBase):
    pass



class User(Base):
    __tablename__ = 'user'
    user_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(255), nullable=True)
    last_name: Mapped[str] = mapped_column(String(200), nullable=True)
    username: Mapped[str] = mapped_column(String(255), nullable=True)
    joined_at: Mapped[DateTime] = mapped_column(TIMESTAMP)
    is_admin: Mapped[bool] = mapped_column(BOOLEAN)

    
    
class Category(Base):
    __tablename__ = 'category'
    category_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    category_short_name: Mapped[str] = mapped_column(String(255))
    category_name: Mapped[str] = mapped_column(String(255))
    category_description: Mapped[str] = mapped_column(String(255), nullable=True)
    
    
    
    
    
class Subscription(Base):
    __tablename__ = 'subscription'
    user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id'), primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('category.category_id'), primary_key=True)
    


class Subscriber(Base):
    __tablename__ = 'subscriber'
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(String(255), nullable=True)
    date: Mapped[DateTime] = mapped_column(TIMESTAMP) 
    



class Bot_message(Base):
    __tablename__ = 'bot_message'
    message_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('user.user_id'))
    date_send: Mapped[DateTime] = mapped_column(TIMESTAMP)
    message_text: Mapped[str] = mapped_column(String, nullable=True)
    
    
class User_message(Base):
    __tablename__ = 'user_message'
    response_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('user.user_id'))
    date_send: Mapped[DateTime] = mapped_column(TIMESTAMP)
    response_text: Mapped[str] = mapped_column(String, nullable=True)
    


class Menu(Base):
    __tablename__ = 'menu'
    menu_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    dte: Mapped[DateTime] = mapped_column(TIMESTAMP)
    menu_text: Mapped[str] = mapped_column(String, nullable=True)
    menu_link: Mapped[str] = mapped_column(String, nullable=True)
    menu_image_path: Mapped[str] = mapped_column(String, nullable=True)
    menu_image_hash: Mapped[str] = mapped_column(String, nullable=True)


    
    
class Menu_review(Base):
    __tablename__ = 'menu_review'
    review_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    dttm: Mapped[DateTime] = mapped_column(TIMESTAMP)
    review_text: Mapped[str] = mapped_column(String, nullable=True)
    
    
    
    
    
    
    
    
    
