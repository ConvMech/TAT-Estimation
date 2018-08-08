# Python Imports
import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
from sqlalchemy import *
import os
# Repo Imports
import settings
from utilities.db_interactions import DB_interactions
import sys

def main():
    # Redshift
    redshift_url = "{d}+{driver}://{u}:{p}@{h}:{port}/{db}".format(d=settings.target_database['dialect'],
                                                                   driver=settings.target_database['drivername'],
                                                                   u=settings.target_database['username'],
                                                                   p=settings.target_database['password'],
                                                                   h=settings.target_database['host'],
                                                                   port=settings.target_database['port'],
                                                                   db=settings.target_database['database'])
    print(redshift_url)
    #ssl_args = {'sslmode': 'verify-full',
    #            'sslrootcert': '/Users/pratikramdasi/redshift-data-warehouse/root.crt'}

    engine_redshift = create_engine(redshift_url, connect_args={'sslmode':'require'}, echo=True)#, connect_args=ssl_args)

    DB = DB_interactions(engine=engine_redshift)

    sql = '''
        unload ('
            SELECT 
              * 
            FROM public.orders
            WHERE order_created_at >= \\'2018-08-04 00:00:00\\'
        ')
        to 's3://files.development.hover.to/tommy_tat_data/orders_after_2018-08-04_puborders_'
        ACCESS_KEY_ID '{aws_key}'
        SECRET_ACCESS_KEY '{aws_secret}'
        parallel off gzip
    '''

    sql = sql.format(aws_key=os.environ["AWS_ACCESS_KEY_ID"], aws_secret=os.environ["AWS_SECRET_ACCESS_KEY"])

    df = DB.execute_sql(sql=sql)


if __name__ == '__main__':
    out_folder_path = sys.argv[1]
    print(out_folder_path)
    print(os.environ["AWS_ACCESS_KEY_ID"],os.environ["AWS_SECRET_ACCESS_KEY"])
    main()
