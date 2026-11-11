from database.distributore_DAO import DistributoreDAO

'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class Model:
    def __init__(self):
        self._distributori = None
        self.load_distributori()

        self.__sequenza_ottima = []
        self.__costo_ottimo = -1

    def load_distributori(self):
        """ Carica tutti i distributori e li setta nella variabile self._distributori """
        self._distributori = DistributoreDAO.get_distributori()

    def get_prezzo_medio(self, mese:int):
        """
        Calcola, per ogni distributore, il prezzo medio al litro per il mese selezionato.
        :param mese: Mese selezionato (un intero da 1 a 12)
        :return: lista di DIZIONARI --> (nome del distributore, media), es. {"nome": Distributore A, "media": 1.789}
        """
        db = DistributoreDAO()
        p = db.prezzi_medi(mese)
        return p

    def get_sequenza_ottima(self, mese:int):
        """
        Calcola la sequenza ottimale di rifornimenti nei primi 7 giorni
        :return: sequenza di nomi distributore ottimale
        :return: costo ottimale (cioè quello minimizzato dalla sequenza scelta)
        """
        self.__sequenza_ottima = []
        self.__costo_ottimo = -1
        prezzi_settimana = self.__get_prezzi_prima_settimana_mese(mese)
        print(prezzi_settimana)
        self.__sequenza_ottima = self.__ricorsione([], 0, None, None, 0, prezzi_settimana)
        print(self.__sequenza_ottima)
        id_to_nome = {distributore.id: distributore.nome for distributore in self._distributori}
        sequenza_nomi = [f"Giorno {giorno}: {id_to_nome[i]}" for giorno, i in enumerate(self.__sequenza_ottima, start=1)]
        return sequenza_nomi, round(self.__costo_ottimo, 2)

    def __ricorsione(self, sequenza_parziale, giorno, ultimo_distributore, altro_distributore, costo_corrente, prezzi_settimana):
        """ Implementa la ricorsione """
        if len(sequenza_parziale) == 7:
            return sequenza_parziale
        else:
            if len(sequenza_parziale) == 0:
                if prezzi_settimana[1][0] <= prezzi_settimana[2][0]:
                    sequenza_parziale.append(1)
                    self.__costo_ottimo += (prezzi_settimana[1][0] * 100)
                    ultimo_distributore = 1
                    altro_distributore = 2
                else:
                    sequenza_parziale.append(2)
                    self.__costo_ottimo += (prezzi_settimana[2][0] * 100)
                    ultimo_distributore = 2
                    altro_distributore = 1
            else:
                print(f"Nuovo distributore: {prezzi_settimana[altro_distributore][giorno] * 100 + 5}")
                print(f"Vecchio Distributore {prezzi_settimana[ultimo_distributore][giorno] * 100}")
                if ((prezzi_settimana[altro_distributore][giorno]*100) + 5) < (prezzi_settimana[ultimo_distributore][giorno]*100):
                    aus = ultimo_distributore
                    ultimo_distributore = altro_distributore
                    altro_distributore = aus
                    sequenza_parziale.append(ultimo_distributore)
                    self.__costo_ottimo += (prezzi_settimana[ultimo_distributore][giorno] * 100) + 5
                else:
                    sequenza_parziale.append(ultimo_distributore)
                    self.__costo_ottimo += (prezzi_settimana[ultimo_distributore][giorno] * 100)

            return self.__ricorsione(sequenza_parziale, giorno+1, ultimo_distributore, altro_distributore, self.__costo_ottimo, prezzi_settimana)



    def __get_prezzi_prima_settimana_mese(self, mese: int):
        """
        Restituisce i prezzi dei primi 7 giorni del mese selezionato per ciascun distributore.
        :return: un dizionario: {id_distributore: [prezzo_giorno1, ..., prezzo_giorno7]}
        """
        DAO = DistributoreDAO()
        dict = DistributoreDAO.get_prezzi_primi_7_giorni(mese)
        return dict
