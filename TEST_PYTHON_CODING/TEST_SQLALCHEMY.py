from sqlalchemy import Column, String, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base
Base=declarative_base()
class User(Base):
    __tablename__='user'
    id=Column(String(20),primary_key=True)
    name=Column(String(20))
engine=create_engine('sqlite:////home/pi/Desktop/raspberrycoding/TEST_PYTHON_CODING/TEST_AIO/test.db', echo=False)
DBSession=sessionmaker(bind=engine)
#engine3 = create_engine('mysql+mysqlconnector://root:raspberrypi@localhost:3306/tst')
session=DBSession()
user=session.query(User).filter(User.id=='1').all()
print('type:', type(user))
#print(user.id)
print(list([username.name]for username in user))
#new=User(id='100009',name='dd')

#session.add(new)
#session.commit()

session.close()

