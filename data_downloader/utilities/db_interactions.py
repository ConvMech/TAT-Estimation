import pandas as pd
from sqlalchemy.sql import text


class DB_interactions:

    def __init__(self, engine):
        self.engine = engine

    def load_data_from_dataframe(self, tablename, df):

        try:
            df.to_sql(tablename, self.engine, if_exists='append', index=False)
            # print "Data Loaded for:", tablename
        except Exception as e:
            print(e.message)
            print "FAILED TO LOAD:", tablename
            print df

    def get_data_from_dataframe(self, sql, parameter_dict):

            # Example SQL and parameter dict
            # d = {"date": d}
            # sql = "SELECT id FROM orders WHERE created_at::DATE = %(date)s"
            df = pd.read_sql(sql, self.engine, params=parameter_dict)
            return df

    def get_data_from_dataframe_no_params(self, sql):

            # Example SQL and parameter dict
            # d = {"date": d}
            # sql = "SELECT id FROM orders WHERE created_at::DATE = %(date)S"
            df = pd.read_sql(sql, self.engine)
            return df

    def execute_sql_with_param(self, sql, params_dict=None):

        # print params_dict
        connection = self.engine.connect()
        connection.execute(sql, **params_dict)
        # result = connection.execute(sql, param)
        # result = connection.execute(sql, **params_dict)
        # print result

        # for row in result:
        #     print row
        #     print("usename:", row['usename'])
        connection.close()

    def execute_sql(self, sql):

        connection = self.engine.connect()
        connection.execute(sql)
        connection.close()

    def execute_sql_autocommit_flag(self, sql):
        connection = self.engine.connect()
        connection.execute(sql.execution_options(autocommit=True))
        connection.close()

