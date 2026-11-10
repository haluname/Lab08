from database.DB_connect import DBConnect
from model.distributore_DTO import Distributore

"""
    DISTRIBUTORE DAO
    Gestisce le operazioni di accesso al database.
"""

class DistributoreDAO:
    @staticmethod
    def get_distributori() -> list[Distributore] | None:
        """
        Restituisce tutti i distributori presenti nel database
        :return: lista di tutti i Distributori
        """
        cnx = DBConnect.get_connection()
        result = []

        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = """ SELECT * FROM distributore """
        try:
            cursor.execute(query)
            for row in cursor:
                distributore = Distributore(
                    id=row["id"],
                    nome=row["nome"],
                    indirizzo=row["indirizzo"],
                )
                result.append(distributore)
        except Exception as e:
            print(f"Errore durante la query get_distributori: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()

        return result

    def prezzi_medi(self, mese):
        print(mese)
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """SELECT nome, AVG(prezzo_litro) as media FROM prezzo p 
                    INNER JOIN distributore d ON p.id_distributore = d.id
                    where month(data) = %s
                    GROUP BY id_distributore """

        cursor.execute(query, (mese,))
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data

    def get_prezzi_primi_7_giorni(mese):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
                SELECT prezzo_litro, id_distributore
                FROM prezzo
                WHERE YEAR (data) = 2026
                  AND MONTH (data) = %s
                  AND DAY (data) <= 7
                ORDER BY data ASC, id_distributore ASC
                """

        cursor.execute(query, (mese,))
        results = cursor.fetchall()

        cursor.close()
        conn.close()

        dizionario_prezzi = {}

        for riga in results:
            id_dist = riga['id_distributore']
            prezzo = riga['prezzo_litro']

            if id_dist not in dizionario_prezzi:
                dizionario_prezzi[id_dist] = []

            dizionario_prezzi[id_dist].append(prezzo)

        return dizionario_prezzi
