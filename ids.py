# Skriven av Farhad Asadi, november 2021


import os
import hashlib


def find_files(fname): 
    """
    Hitttar alla filer i en map(och submappar) och returnerar dem. 
    t.ex. ["E:/BTH/Python3/test.txt", "E:/BTH/Python3/test_1.txt"] 

    """

    # Kontrollerar om fname är en map (Eller kontrollerar om fname finns)
    if os.path.isdir(fname):
        list_files = os.listdir(fname)
        all_files = list()
        for i in list_files:
            fullpath = os.path.join(fname, i)
            if os.path.isdir(fullpath):
                all_files = all_files + find_files(fullpath)
            else:
                all_files.append(fullpath)
        return all_files
    elif os.path.isfile(fname):
        return list(fname.split(" "))



def generate_md5(fname):
    """
    Funktionen skapar en md5_hash för värje fil som funktionen find_files()
    hittar och returnerar en lista med alla hash data.
    t.ex. ["E:/BTH/Python3/test.txt", "E:/BTH/Python3/test_1.txt"] 
          ["dfdfjhkjhfa1fdsgdg", kjhjdhfi8eseoidfjdf]

    """
    hash_data = [] 
    for i in range(len(fname)):
        with open(fname[i], "rb") as f:
            data = f.read()
            md5 = hashlib.md5()
            md5.update(data)
            md5_hash = md5.hexdigest()
            hash_data.append(md5_hash)
    return hash_data



def create_hashfile(x, y):
    """
    Funktionen tar två parameter x = senaste loggen och y = den nya loggen.
    Funktionen skapar två .txt filer och lägger x i en fil som heter hash_data_1.txt
    och en annan .txt fil som heter hash_data_0.txt.
    """

    # Om hash_data_1.txt och hash_data_0.txt finns så betyder det att vi en ny "senaste loggen"
    # vilket betyder att vi inte behöver hash_data_1.txt längre. Därför tar vi bort hash_data_1.txt
    # och döper hash_data_0.txt till hash_data_1.txt. När vi kör programmet igen då kan vi använda
    # hash_data_1.txt för att jämföra det med den nya hash_loggen som skapas(hash_data_0.txt). 
    if os.path.exists("hash_data_1.txt") and os.path.exists("hash_data_0.txt"):
        os.remove("hash_data_1.txt")
        os.rename("hash_data_0.txt", "hash_data_1.txt")
    i = 1
    while os.path.exists(f"hash_data_{i}.txt"):
        i -= 1
    hash_file = open(f"hash_data_{i}.txt", "a+")
    for i in range(len(x)):
        hash_file.write(x[i])
        hash_file.write("\t")
        hash_file.write(y[i])
        hash_file.write("\n")

    hash_file.close()


def read_file(fname): 
    """
    Funktionen läser fname och returnerar en dictionary med filar och deras md5_hash.
    t.tx. {
           "E:/BTH/Python3/test.txt": "dfdfjhkjhfa1fdsgdg", 
           "E:/BTH/Python3/test_1.txt": "kjhjdhfi8eseoidfjdf",
           "E:/BTH/Python3/test_2.txt": "kkjkjlkjsdf9erer234"
          }

    """
    file = open(fname, "r")
    new_dict = {}
    for line in file:
        key, value = line.split()
        new_dict[key] = value

    return new_dict


def changed_files(old_dict, new_dict):
    """
    Funktionen tar två parameter old_dict = hash_data_1.txt i form av en dictioinary
                            och  new_dict = hash_data_0.txt i form av en dictionary
    Funktionen returnerar en lista med alla filer som har ändrats.
    t.ex. ["E:/BTH/Python3/test.txt", "E:/BTH/Python3/test_1.txt"] 

    """
    changed_list = []
    for i in old_dict.keys():
        if i in new_dict.keys():
            if old_dict[i] not in new_dict.values():
                changed_list.append(i)
    return changed_list


def deleted_files(old_dict, new_dict):
    """
    Funktionen tar två parameter old_dict = hash_data_1.txt i form av en dictioinary
                            och  new_dict = hash_data_0.txt i form av en dictionary
    Funktionen returnerar en lista med alla filer som har tagits bort.
    t.ex. ["E:/BTH/Python3/test.txt", "E:/BTH/Python3/test_1.txt"] 

    """
    removed_files = list(filter(lambda x: x not in new_dict, old_dict))
    return removed_files

def new_files(old_dict, new_dict):
    """
    Funktionen tar två parameter old_dict = hash_data_1.txt i form av en dictioinary
                            och  new_dict = hash_data_0.txt i form av en dictionary
    Funktionen returnerar en lista med alla filer som har skapats.
    t.ex. ["E:/BTH/Python3/test.txt", "E:/BTH/Python3/test_1.txt"] 

    """
    added_files = list(filter(lambda x: x not in old_dict, new_dict))
    return added_files



def main():
    print("Welcome to Intrusion Detection Check")
    
    print("-----------------------------------")
    i = True
    while i:
        # Användaren kan skriva vilken fill de vill försvara
        the_path = input("What folder (path full or relative) do you want to protect?\n")
        print(find_files(the_path))

        # Programmet kollar om the_path är en file eller en map(programmet kollar om filen finns).
        if os.path.isdir(the_path) or os.path.isfile(the_path):
            var_find_files = find_files(the_path)
            var_generate_md5 = generate_md5(var_find_files)
            create_hashfile(var_find_files, var_generate_md5)


            # Kolla om de två filer som ska jämföras finns
            if os.path.exists("hash_data_0.txt") and os.path.exists("hash_data_1.txt"):
                old_file = read_file("hash_data_1.txt")
                new_file = read_file("hash_data_0.txt")


                var_changed_files = changed_files(old_file, new_file)
                var_deleted_files = deleted_files(old_file, new_file)
                var_new_files = new_files(old_file, new_file)


                print("Report")
                print("------")
                if var_changed_files == [] and var_deleted_files == [] and var_new_files == []:
                    print("There where no changes in the folder")
                else:
                    print("WARNING!\n")
                    print("NEW FILES")
                    print("---------")
                    for i in var_new_files:
                        print(i)

                    print("\n")
                    print("CHANGED FILES")
                    print("-------------")
                    for i in var_changed_files:
                        print(i)

                    print("\n")
                    print("REMOVED FILES")
                    print("-------------")
                    for i in var_deleted_files:
                        print(i)

            # Om de två filer inte finns betyder det att vi skapar en logg som kan användas 
            # för att se om filerna har ändras, tagits bort eller skapats
            else:
                print("The program is ready for...") 

            # finish the loop 
            i = False

        # Om the_path inte finns
        else:
            print(the_path, "does not exists! Try again!")
    

# Run the main function
if __name__ == "__main__":
    main()

