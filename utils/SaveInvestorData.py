import psycopg2
from utils.DBparams import db_params


def SaveInvestorData(
    first_name,
    last_name,
    date_of_birth,
    nationality,
    sex,
    proof_of_id_number,
    email
):
    """
    Saves investor data to the PPMAndSubs.Investors table.
    """

    connection = None

    try:
        connection = psycopg2.connect(**db_params)

        with connection.cursor() as cursor:
            sql = '''
                INSERT INTO "PPMAndSubs"."Investors"
                (
                    first_name,
                    last_name,
                    date_of_birth,
                    nationality,
                    sex,
                    proof_of_id_number,
                    email
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            '''

            cursor.execute(
                sql,
                (
                    first_name,
                    last_name,
                    date_of_birth,
                    nationality,
                    sex,
                    proof_of_id_number,
                    email
                )
            )

        connection.commit()

    except Exception:
        if connection:
            connection.rollback()
        raise

    finally:
        if connection:
            connection.close()
