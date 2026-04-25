import psycopg2
import psycopg2.extensions


# TODO: add class Connect disconnect methode pour connecet et autre pour le contraire
class ConnectDisconnect():
    def __init__(self, table):

        self.table = table




    def conn_data_base(self):

        self.conn = psycopg2.connect(
            database="sigma",
            user="postgres",
            password="trust",
            host="localhost",
            port='5432'
        )

        self.cursor = self.conn.cursor()
        #print(f"la connection : {self.conn}")
        self.cursor.execute(f'''create table if not exists {self.table}(
                        id SERIAL primary key,
                        tache text,
                        nom_personne character varying(50),
                        etat integer)''')
        #print(f"la connection : {self.table}")


    def disconn_data_base(self):
        self.conn.close()

# TODO: class fonction ajouter tache
class Taches(ConnectDisconnect):
    def __init__(self,table):
        super().__init__(table)
        self.cnn = ConnectDisconnect



    def afficher_taches(self):

# TODO: gestion des excpetion
        try:
            self.cnn.conn_data_base(self)

            cursors = self.conn.cursor()

            #print("la table in task class : ", self.table)

            cursors.execute(f"select * from {self.table}")

            data = cursors.fetchall()

            #verif = self.tache_existe("dodo")

            #print("selection resultat",type(data), " la condition", verif)

            for i,d in enumerate(data):
                #print("i am here")
                print(f"tache {i+1} : {d[1]}, nom concerne : {d[2]}, etat : {d[3]}. ")

        except Exception as e:
            print(e)

        finally:
            self.cnn.disconn_data_base(self)

    def ajouter_tache(self,nv_tache,nv_nom,nv_etat):

        self.nv_tache = nv_tache
        self.nv_nom = nv_nom
        self.nv_etat = nv_etat

        verif = self.tache_existe(self.nv_tache)

        if verif:
            print(f"cette tache {self.nv_tache} existe deja impossible de l'ajouter")

        else:
            try :
                self.cnn.conn_data_base(self)
                self.cursors = self.conn.cursor()
                self.cursors.execute(f'''insert into {self.table}
                                    (tache,nom_personne,etat)
                                     values('{self.nv_tache}','{self.nv_nom}',{self.nv_etat})''')
                self.conn.commit()

            except Exception as e:
                print(e)
            finally:
                self.cnn.disconn_data_base(self)

# TODO: Terminer une tache

    def terminer_tache(self, nom_tache):

        self.nom_tache = nom_tache

        verif = self.tache_existe(self.nom_tache)
        #print(f"verification existe : {verif}")

        if verif:
            try :
                #print(f"cette tache {nom_tache} existe")
                self.cnn.conn_data_base(self)
                cursors = self.conn.cursor()
                cursors.execute(f'''update {self.table} set etat = {1} where tache = '{self.nom_tache}' ''')
                self.conn.commit()

            except Exception as e :
                print(e)

            finally:
                self.cnn.disconn_data_base(self)
        else :
            print(f"cette tache : {self.nom_tache} n'existe pas")

# TODO: supprimer une tache


    def supprimer_tache(self, nom_tache):

        self.nom_tache = nom_tache



        try:
            verif = self.tache_existe(self.nom_tache)
            self.cnn.conn_data_base(self)

            cursors = self.conn.cursor()
            cursors.execute(f'''select etat from {self.table} where tache = '{self.nom_tache}' ''')
            data = cursors.fetchone()

            print(f"l'etat est: {data[0]}")

            etat_a_supprimer = [True if data[0] == 1 else False]

            print(f"Etat de la verification: {verif[0]} etat de la tache:  {etat_a_supprimer[0]} ")

            if verif[0] and etat_a_supprimer[0]:
                print("i am here")
                cursors.execute(f'''delete from {self.table} where tache='{self.nom_tache}' ''')
                self.conn.commit()

            else:
                print(f"la tache {self.nom_tache} n'existe pas pas ou n'est pas encore terminer ")

            # if etat_a_supprimer:
            #
            #
            # else:
            #     print(f"la tache {self.nom_tache} ne peut pas etre supprimer car toujour actif ")

        except Exception as e:
            print(e)

        finally:
            self.cnn.disconn_data_base(self)



# TODO: Verification tache existe

    def tache_existe(self, verification_tache):


        try:
            self.cnn.conn_data_base(self)

            cursors = self.conn.cursor()

            #print("la table in task class : ", self.table)

            cursors.execute(f"select tache from {self.table} where tache = '{verification_tache}' ")
            data = cursors.fetchone()
            val = [True if verification_tache in data else False]

            return val

            # print("selection resultat",type(data), " la condition", verif)
            #
            # for i,d in enumerate(data):
            #     #print("i am here")
            #     print(f"tache {i+1} : {d[1]}, nom concerne : {d[2]}, etat : {d[3]}. ")

        except Exception as e:
            print(e)

        finally:
            self.cnn.disconn_data_base(self)




tbl = "taches"
tch = Taches(tbl)

# tch.ajouter_tache('marcher','Salomom',1)
# tch.ajouter_tache('courir','Daniel',0)
# tch.ajouter_tache('grimper','Julianna',1)
# tch.ajouter_tache('jouer','Marco',0)
# tch.ajouter_tache('manger','Babe',1)


#tch.ajouter_tache('karate','sargon',0)


#tch.terminer_tache('karate')

#tch.afficher_taches()
#tch.supprimer_tache('karate')
#tch.afficher_taches()

q = True

while q :

    read = str(input("""###=======================================================================================================================###
     (A) : Afficher Tache, (J) : aJouter Tache, (T) : Terminer Tache, (S) : Suprimmer Tache, (Q) : Quiter le programme :
     
     """))


    match read :
        case 'A':
            tch.afficher_taches()

        case 'J':
            nv_tache = str(input("donner le nom de la tache : "))
            nv_personne = str(input("donner le nom de la tache : "))

            tch.ajouter_tache(nv_tache,nv_personne,0)

        case 'T':
            nt_tache = str(input("Entrer le nom de la tache pour la terminer : "))

            tch.terminer_tache(nt_tache)

        case 'S':
            sp_tache = str(input("Entrer le nom de la tache a suprimer: "))

            tch.supprimer_tache(sp_tache)

        case 'Q':
            quiter = str(input("Voulez vous vraiment quiter le programme? : "))
            if quiter == 'o':
                q = False

            else :
                q = True

        case _:
            print("veuillez taper une entree valide")


