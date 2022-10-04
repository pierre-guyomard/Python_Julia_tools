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

    def process(self) :

        self.dict_fonction = dict()

        sowil = 0

        while sowil <= len(self.fichier) - 1 :

            uruz = sowil

            if self.fichier[uruz].startswith('function') :

                while uruz <= len(self.fichier) - 1 :

                    temp = self.fichier[uruz]

                    #print('')

                    #print(temp)

                    if temp.startswith('function') :

                        temp = temp.strip()

                        temp = temp.split('function')[1]

                        temporary_name = temp.split('(')[0]

                        temporary_name = temporary_name[1:]

                        #print('')

                        #print(temporary_name)

                        self.dict_fonction[temporary_name] = 'function' + temp + ' ; '

                        uruz = uruz + 1

                    elif temp.startswith('\t') :

                        temp = temp.strip()

                        self.dict_fonction[temporary_name] = self.dict_fonction[temporary_name] + temp + ' ; '

                        uruz = uruz + 1

                    else : #temp.startswith('end') :

                        temp = temp.strip()

                        self.dict_fonction[temporary_name] = self.dict_fonction[temporary_name] + temp

                        break

            else :

                pass

            sowil = sowil + 1

        return self.dict_fonction
