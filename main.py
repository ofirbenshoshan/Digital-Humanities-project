import time
import os
import subprocess
import shutil
from os import listdir
from os.path import isfile, join

genderMasc = ["לקוחות יקרים", "שומרים על ההנחיות", "לקוח יקר","כמה טוב לראות אתכם שוב", "כיף לראות אתכם", "אורחים יקרים",
              "אורחים/דיירים יקרים","עובד/מבקר יקר", "היי טוב שבאת", "לקוחות נכבדים", "מטופלים יקרים", "התגעגעתם?", "ברוכים הבאים",
              "לָקוֹחוֹת יְקָרִים", "שׁוֹמְרִים עַל הַהַנְחָיוֹת", "לָקוֹחַ יָקָר","כַּמָּה טוֹב לִרְאוֹת אֶתְכֶם שׁוּב", "כֵּיף לִרְאוֹת אִתְּכֶם", "אוֹרְחִים יְקָרִים",
              "אוֹרְחִים/דַּיָּרִים יְקָרִים","עוֹבֵד/מְבַקֵּר יָקָר", "הַי טוֹב שֶׁבָּאתָ", "לָקוֹחוֹת נִכְבָּדִים", "מְטֻפָּלִים יְקָרִים", "הִתְגַּעְגַּעְתֶּם?", "בְּרוּכִים הַבָּאִים"]
genderFem = ["שומרות על ההנחיות", "לקוחה יקרה", "לקוחות יקרות","כמה טוב לראות אתכן שוב", "כיף לראות אתכן", "אורחות יקרות",
             "אורחות/דיירות יקרות","עובדת/מבקרת יקרה", "לקוחות נכבדות", "מטופלות יקרות", "התגעגעתן?", "ברוכות הבאות",
             "שׁוֹמְרוֹת עַל הַהַנְחָיוֹת", "לְקוּחָה יְקָרָה", "לָקוֹחוֹת יְקָרוֹת","כַּמָּה טוֹב לִרְאוֹת אֶתְכֶן שׁוּב", "כֵּיף לִרְאוֹת אֶתְכֶן", "אוָרְחוֹת יְקָרוֹת",
             "אוָרְחוֹת/דַּיָּרוֹת יְקָרוֹת", "עוֹבֶדֶת/מְבַקֶּרֶת יְקָרָה", "לָקוֹחוֹת נִכְבָּדוֹת", "מְטֻפָּלוֹת יְקָרוֹת", "הִתְגַּעְגַּעְתֶּן?", "בְּרוּכוֹת הַבָּאוֹת"]
# gender2 = ["לקוחות יקרים/יקרות", "שומרים/שומרות על ההנחיות", "לקוח/לקוחה יקר", "לקוחות יקרים/יקרות",
#             "כמה טוב לראות אתכם/אתכן שוב", "שימו לב", "כיף לראות אתכם/אתכן", "אורחים/אורחות יקרים", "דיירים/דיירות יקרים",
#             "היי טוב שבאת", "לקוחות נכבדים/נכבדות", "מטופלים יקרים/יקרות", "ברוכים/ברוכות הבאים/הבאות"]
negativAppro = ["בלי", "אי", "ללא", "אין", "אל", "בל", "בלתי", "לא", "לבלתי", "מבלי", "מבלתי",
                "בְּלִי", "אִי", "לְלֹא", "אֵין", "אַל", "בֵּל", "בִּלְתִּי", "לֹא", "לְבִלְתִּי", "מִבְּלִי", "מִבִּלְתִּי"]

def remove_niqqud_from_string(my_string):
    return ''.join(['' if  1456 <= ord(c) <= 1479 else c for c in my_string])

def gender_and_approach(file_path, sep="\t", encoding='utf8'):
    """
    Reads a data file in CoNLL format and check If the reference is in male or female and the approach in positive or negative

    Args:
        file_path (str): Data file path.
        sep (str, optional): Column separator. Defaults to "\t".
        encoding (str): File encoding used when reading the file.
            Defaults to utf8.

    Returns: [g,a]
        g = 1 - if female, 0 - if male, -1 if no gender
        a = 1 - if positive, 0 - if negative

    """
    with open(file_path, encoding='utf8') as f:
            data = f.readlines()
            g = -1
            a = 1
            for line in data:
                words = line.split('\t')
                if 'VERB' in words or 'VB' in words:#found verb
                    if 'Gender=Fem' in words or 'gen=F' in words:
                        g = 1
                    elif 'Gender=Masc' in words or 'gen=M' in words:
                        g = 0
                if g == -1:
                    for w in words:
                        if w in genderFem:
                            g = 1
                        elif w in genderMasc:
                            g = 0
                        if w in negativAppro:
                            a = 0
                else:
                    for w in words:
                        if w in negativAppro:
                            a = 0
    return [g,a]

def read_conll_file(file_path, file_path2, sep="\t", encoding='utf8'):
    """
    Reads a data file in CoNLL format and returns if the analyse is the same

    Args:
        file_path (str): Data file path.
        file_path2 (str): Data file path2.
        sep (str, optional): Column separator. Defaults to "\t".
        encoding (str): File encoding used when reading the file.
            Defaults to utf8.

    Returns: False if the analyse is not the same, and True otherwise

    """
    with open(file_path, encoding='utf8') as f:
        with open(file_path2, encoding='utf8') as f2:
            data = f.readlines()
            data2 = f2.readlines()
            for line, line2 in zip(data, data2):
                words = line.split('\t')
                words2 = line2.split('\t')
                if len(words) > 1 and len(words2) > 1 and remove_niqqud_from_string(words[2]) != words2[2] and not (words[2] == "מַסֵּכָה" and words2[2] == "מסיכה"):
                    print(words[2])
                    print(words2[2])
                    return False
    return True

def tsv_to_txt(name_tsv, name_txt):
    import csv

    # Open tsv and txt files(open txt file in write mode)
    tsv_file = open(name_tsv, encoding="utf8")
    txt_file = open(name_txt, "w", encoding="utf8")

    # Read tsv file and use delimiter as \t. csv.reader
    # function retruns a iterator
    # which is stored in read_csv
    read_tsv = csv.reader(tsv_file, delimiter="\t")

    # write data in txt file line by line
    for row in read_tsv:
        joined_string = "\t".join(row)
        txt_file.writelines(joined_string + '\n')

    # close files
    txt_file.close()

def compar_word(wordyap, worddicta):
    newworddicta = remove_niqqud_from_string(worddicta)
    if newworddicta != wordyap:
        i1 = 0
        i2 = 0
        while i1 < len(wordyap) and i2 < len(newworddicta): # check example like that: wordyap = מותר  newworddicta = מתר
            if wordyap[i1] != newworddicta[i2] and wordyap[i1] != 'י' and wordyap[i1] != 'ו':
                return False
            elif wordyap[i1] != newworddicta[i2] and (wordyap[i1] == 'י' or wordyap[i1] == 'ו'):
                i1+=1
            else:
                i1+=1
                i2+=1
        if i1 < len(wordyap) or i2 < len(newworddicta):
            return False
    return True

def comper_number_of_nodes(content_yap,content_dicta):
    yapwords = content_yap[len(content_yap)-2].split('\t')
    dictawords = content_dicta[len(content_dicta)-2].split('\t')
    print(yapwords)
    print(dictawords)
    if len(dictawords) > 1 and len(yapwords) > 2 and yapwords[1] != dictawords[0]:
        print(yapwords[1])
        print(dictawords[0])
        return False
    return True

def dicta_to_yap(file_dicta_tsv,file_dicta,file_yap_map,file_yap):
    tsv_to_txt(file_dicta_tsv, file_dicta)
    tsv_to_txt(file_yap_map, file_yap)
    with open(file_yap, 'r', encoding="utf8") as fp:
        with open(file_dicta, 'r', encoding="utf8") as fd:
            content_yap = fp.readlines()
            content_dicta = fd.readlines()
            print(content_yap)
            print(content_dicta)
            if not comper_number_of_nodes(content_yap,content_dicta):
                return False
            arr_new_lines = []
            for line in content_yap:
                x = line.split()
                if (len(x) > 4):
                    word = x[2]
                    print(word)
                    c = 0
                    for line2 in content_dicta:
                        if (c < 3):
                            c = c + 1
                            continue
                        s = line2.split()
                        found = 0
                        num = -1
                        for i in s:
                            num+=1
                            if num == 0:
                                continue
                            if (compar_word(word, i) or (i == "מַסֵּכָה" and word == "מסיכה")):
                                found = 1
                                temp = ""
                                for i in range(1, 5):
                                    line = str(line).replace(str(x[i + 1]), str(s[i]))
                                arr_new_lines.append(line)
                                print(line)
                                break
                        if (found):
                            break
    open(file_yap_map, "w").close()
    with open(file_yap_map, 'w', encoding="utf8") as fp:
        fp.writelines(arr_new_lines)
        fp.write("\n")
    return True

def run_yap_on_execl():
    file_yap = "C:\\OFIR\\output.txt"
    file_yap_map = "C:\\OFIR\\output.mapping"
    file_dicta = "C:\\OFIR\\MorphologyResults.ud.txt"
    file_dicta_tsv = "C:\\OFIR\\MorphologyResults.ud.tsv"
    file_name = "C:\\OFIR\\sentences.txt"
    counters = [0,0,0,0,0,0]#[nogender,male,female,negative,positive,wronganalys]
    with open(file_name, 'r', encoding="utf8") as fp:
        content = fp.readlines()
        number_of_sentence = 0
        for s in content:
            print(counters)
            number_of_sentence+=1
            print("***********************{}******************".format(number_of_sentence))
            print(s)
            s1 = s.split()
            with open("C:\\OFIR\\yapproj\\src\\yap\\input.txt", 'w',encoding="utf8") as fp2:
                for line in s1:
                    fp2.write(line)
                    fp2.write("\n")
                fp2.write("\n")

            os.chdir("C:\\OFIR\\yapproj\\src\\yap")
            p = os.system("cmd py -3.7-32 /c yap.exe hebma -raw input.txt -out input.lattice")
            time.sleep(3)
            p = os.system("cmd py -3.7-32 /c yap.exe md -in input.lattice -om output.mapping")
            time.sleep(3)
            p = os.system("cmd py -3.7-32 /c yap.exe dep -inl output.mapping -oc output.conll")
            time.sleep(3)

            original = r'C:\OFIR\yapproj\src\yap\input.txt'
            target = r'C:\OFIR\inputyap.txt'
            shutil.move(original, target)
            original = r'C:\OFIR\yapproj\src\yap\input.lattice'
            target = r'C:\OFIR\inputyap.lattice'
            shutil.move(original, target)
            original = r'C:\OFIR\yapproj\src\yap\output.mapping'
            target = r'C:\OFIR\output.mapping'
            shutil.move(original, target)
            shutil.copyfile(target, r'C:\OFIR\outputyap.mapping')
            original = r'C:\OFIR\yapproj\src\yap\output.conll'
            target = r'C:\OFIR\outputyap.conll'
            shutil.move(original, target)

            args = 'C:\\ti\\lunas2\\python\\Scripts\\python.exe C:\\OFIR\\morpoProj\\dictaAnalyse.py ' + s
            print(args)
            proc = subprocess.Popen(args,
                                    shell=True,
                                    stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE,
                                    )
            proc.wait()
            time.sleep(3)
            original = r'C:\Users\a0491561\Downloads\MorphologyResults.ud.tsv'
            target = r'C:\OFIR\MorphologyResults.ud.tsv'
            shutil.move(original, target)

            numberOfNodes = dicta_to_yap(file_dicta_tsv,file_dicta,file_yap_map,file_yap)
            if not numberOfNodes: # number of nodes doesnt equal , need to check manually
                counters[5]+=1
                new_dir = 'C:\\OFIR\\{}'.format(number_of_sentence)
                os.mkdir(new_dir)
                for f in listdir('C:\\OFIR'):
                    if isfile(join('C:\\OFIR', f)) and "sentences" not in f:
                        original = join('C:\\OFIR', f)
                        target = join(new_dir, f)
                        shutil.move(original, target)
                continue

            original = r'C:\OFIR\output.mapping'
            target = r'C:\OFIR\yapproj\src\yap\output.mapping'
            shutil.move(original, target)

            os.chdir("C:\\OFIR\\yapproj\\src\\yap")
            p = os.system("cmd py -3.7-32 /c yap.exe dep -inl output.mapping -oc output.conll")

            time.sleep(3)
            original = r'C:\OFIR\yapproj\src\yap\output.mapping'
            target = r'C:\OFIR\outputdicta.mapping'
            shutil.move(original, target)
            original = r'C:\OFIR\yapproj\src\yap\output.conll'
            target = r'C:\OFIR\outputdicta.conll'
            shutil.move(original, target)

            #check if column 3 is equal in yap(outputyap.conll) and dicta(outputdicta.conll), if not need to check manually
            if not read_conll_file(r'C:\OFIR\outputdicta.conll', r'C:\OFIR\outputyap.conll'):
                counters[5] += 1
                new_dir = 'C:\\OFIR\\{}'.format(number_of_sentence)
                os.mkdir(new_dir)
                for f in listdir('C:\\OFIR'):
                    if isfile(join('C:\\OFIR', f)) and "sentences" not in f:
                        original = join('C:\\OFIR', f)
                        target = join(new_dir, f)
                        shutil.move(original, target)
                continue

            #same analays - now check: If the reference is in male or female  and positive or negative language
            gYap, aYap = gender_and_approach(r'C:\OFIR\outputyap.conll')
            gDicta, aDicta = gender_and_approach(r'C:\OFIR\outputdicta.conll')
            if gYap == gDicta and aYap == aDicta:
                counters[gYap+1]+=1
                counters[aYap+3]+=1
                #delete files
                for f in listdir('C:\\OFIR'):
                    if isfile(join('C:\\OFIR', f)) and "sentences" not in f:
                        file = join('C:\\OFIR', f)
                        os.remove(file)
            else:#check manually
                counters[5] += 1
                new_dir = 'C:\\OFIR\\{}'.format(number_of_sentence)
                os.mkdir(new_dir)
                for f in listdir('C:\\OFIR'):
                    if isfile(join('C:\\OFIR', f)) and "sentences" not in f:
                        original = join('C:\\OFIR', f)
                        target = join(new_dir, f)
                        shutil.move(original, target)
                continue
    print(counters)
    return counters

def main():
    run_yap_on_execl()
    
if __name__ == '__main__':
    main()

