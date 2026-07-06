from sqlalchemy import Column, Integer, String
from core.db import Base

class EmailLog(Base):
    __tablename__ = "email_logs"

    id = Column(Integer, primary_key=True, index=True)
    to_email = Column(String)
    subject = Column(String)
    status = Column(String)
