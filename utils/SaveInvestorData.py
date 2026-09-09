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
    Saves investor data to the PPMAndSubs.Investors table
    and returns the automatically generated investorID.
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
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING "investorID";
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

            investor_id = cursor.fetchone()[0]

        connection.commit()

        return investor_id

    except Exception:
        if connection:
            connection.rollback()
        raise

    finally:
        if connection:
            connection.close()

def SaveUsernameAndPassword(investorID, username, password):
    """
    Saves username and password to the PPMAndSubs.UserIDs table.
    """

    connection = None

    try:
        connection = psycopg2.connect(**db_params)

        with connection.cursor() as cursor:
            sql = '''
                INSERT INTO "PPMAndSubs"."UserIDs"
                (
                    "investorID",
                    user_name,
                    password
                )
                VALUES (%s, %s, %s);
            '''

            cursor.execute(
                sql,
                (
                    investorID,
                    username,
                    password
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
