from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, DailyReport
import pandas as pd

class DatabaseManager:
    def __init__(self, db_name="adops_data.db"):
        self.engine = create_engine(f'sqlite:///{db_name}')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def save_report(self, df):
        """Saves a merged DataFrame into the database."""
        session = self.Session()
        try:
            # Clear old data for demo purposes (optional)
            session.query(DailyReport).delete()
            
            # Bulk insert
            data_dict = df.to_dict(orient='records')
            session.bulk_insert_mappings(DailyReport, data_dict)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error: {e}")
            return False
        finally:
            session.close()

    def get_all_data(self):
        """Reads data back into a Pandas DataFrame."""
        return pd.read_sql(self.Session().query(DailyReport).statement, self.Session().bind)
