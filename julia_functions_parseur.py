import juliacall
import re



julia = juliacall.Main
julia_eval = juliacall.Main.seval
julia_eval('using Pkg')
julia_eval('using StatsModels')
julia_eval('using GLM')



class julia_parseur :

    def __init__(self, path) :

        self.fichier = open(path, 'r').readlines()
        self.dict_fonction = dict()
        self.dict_commentaires = dict()
        self.liste_noms = list()



    def process(self) :

        sowil = 0

        while sowil <= len(self.fichier) - 1 :

            uruz = sowil

            if self.fichier[uruz].startswith('function') :

                commentaire = list()

                while uruz <= len(self.fichier) - 1 :

                    temp = self.fichier[uruz].split("#")

                    try :
                        commentaire.append(temp[1])
                    except IndexError :
                        pass

                    temp = temp[0]

                    if temp.startswith('function') :

                        temp = temp.strip()
                        temp = temp.split('function')[1]
                        temporary_name = temp.split('(')[0]
                        temporary_name = temporary_name[1:]
                        self.liste_noms.append(temporary_name)
                        self.dict_fonction[temporary_name] = 'function' + temp + ' ; '

                        uruz = uruz + 1



                    elif temp.startswith('\t') :

                        temp = temp.strip()
                        self.dict_fonction[temporary_name] = self.dict_fonction[temporary_name] + temp + ' ; '

                        uruz = uruz + 1



                    else : #temp.startswith('end') :

                        temp = temp.strip()

                        self.dict_fonction[temporary_name] = self.dict_fonction[temporary_name] + temp

                        if len(commentaire) > 0 :
                            if len(commentaire) == 1 :
                                self.dict_commentaires[temporary_name] = "\n" + commentaire[0]
                            elif len(commentaire) == 2 :
                                self.dict_commentaires[temporary_name] = "\n" + commentaire[0] + "\n---------\n" + "\n\n\t" + commentaire[1]
                            elif len(commentaire) > 2 :
                                self.dict_commentaires[temporary_name] = "\n" + commentaire[0] + "\n---------\n" + "\n\n\t".join(commentaire[1:len(commentaire)])
                            else :
                                pass

                        break

            else :

                pass

            sowil = sowil + 1



    def check(self) :

        for k in self.liste_noms :

            if not self.dict_fonction[k].endswith('end') :

                self.dict_fonction[k] = self.dict_fonction[k] + 'end'

        return self.dict_fonction



class julia_regression_vers_py_df : # index0 : ordonnee a l'origine ; index1 : pente

    def __init__(self, julia_regression) :

        self.julia_regression = julia_regression

    def convert(self) :

        self.colnames = list(self.julia_regression.colnms)
        self.rownames = list(self.julia_regression.rownms)
        self.dict_coefficients = dict(zip(self.colnames, [None] * len(self.colnames)))

        sowil = 0

        while sowil <= len(self.colnames) - 1 :

            self.dict_coefficients[self.colnames[sowil]] = list(self.julia_regression.cols[sowil])

            sowil = sowil + 1


        return self
