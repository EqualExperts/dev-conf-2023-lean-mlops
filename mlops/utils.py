import duckdb
import logging

FORMAT = '%(asctime)s %(clientip)-15s %(user)-8s %(message)s'
logging.basicConfig(format=FORMAT)


def get_logger(name: str)->logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger



class DuckDBUtils(object):

    def __init__(self, con: duckdb.DuckDBPyConnection):
        self._conn = con

    def profile(self, rel_name):
        if not self._conn:
            raise ValueError("Connection to DB no longer active")
        schema = rel_name.split(".")[0]
        table = rel_name.split(".")[1]
        summary = self._conn.sql(f"""
                                    with col_summary as (
                                        select
                                            column_name,
                                            data_type,
                                            ordinal_position
                                        from information_schema.columns
                                        where table_schema = '{schema}' and table_name = '{table}'
                                    ),
                                    unpivoted as (
                                        select * from {rel_name} unpivot(
                                            col_value
                                            for column_name in (columns(*)) )
                                    ),

                                    record_count as (select count(*) as n_records from {rel_name} ),

                                    completeness as (
                                        select
                                            column_name,
                                            count(col_value) as n_records
                                        from unpivoted
                                        group by column_name
                                    )

                                    select
                                        s.column_name,
                                        s.data_type,
                                        s.ordinal_position,
                                        round(c.n_records/r.n_records, 3) as completeness

                                    from col_summary s
                                    join completeness c
                                    on s.column_name = c.column_name
                                    cross join record_count r


                                """)
        return summary
