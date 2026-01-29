from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class DailyReport(Base):
    __tablename__ = 'daily_reports'
    
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    partner_name = Column(String)
    
    # Internal Data (Our Ad Server)
    internal_imps = Column(Integer)
    internal_rev = Column(Float)
    
    # External Data (Their SSP)
    external_imps = Column(Integer)
    external_rev = Column(Float)
    
    # Calculated Fields
    discrepancy_imps = Column(Float) # % difference
    discrepancy_rev = Column(Float)  # % difference
