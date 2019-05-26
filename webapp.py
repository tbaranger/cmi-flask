import os
from flask import *
import random
import math
import numpy as np

#NE PAS MODIFIER LA LIGNE SUIVANTE
app = Flask(__name__)

app.secret_key = '8zertf6Yr56ZERT5z7412z1rth'

random.seed()

# Data files pour Les Misérables
root = os.path.realpath(os.path.dirname(__file__))
json_path = os.path.join(root, "static/miserables", "miserables.json")
data = json.load(open(json_path))
characters = data["nodes"]
links = data["links"]
NumCharacters = len(characters)

# Page d'accueil
@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

########## Section . Les Misérables ##########
@app.route("/les_miserables_form")
def hello():
    characters_list = []
    for i in characters:
        characters_list.append(i["name"])
    return render_template("form.html",title="Les Misérables",miserables=True,
                           hasError=request.args.get('error'), characters=characters_list)

@app.route("/les_miserables")
def les_miserables():
    characters_list =[]
    for i in characters:
        characters_list.append(i["name"])
    return render_template("les_miserables.html",title="Les Misérables | Les Personnages", miserables=True,
                           number=NumCharacters, characters_list=characters_list)

@app.route("/les_miserables_list_relations")
def list_relations():
    name = request.args.get('name')
    relation = request.args.get('relation')
    relations={}
    k=0
    l=0
    for i in characters:
        if (name == i["name"]):
            for j in links:
                if (j["source"]==k):
                    relations[l] = [characters[j["target"]]["name"],j["value"]]
                    l=l+1
                elif (j["target"]==k):
                    relations[l] = [characters[j["source"]]["name"],j["value"]]
                    l=l+1
        k=k+1
    return render_template("list_relations.html", miserables=True,
                           title=name,name=name,relations=relations)

@app.route("/les_miserables_form_resultat", methods=["POST"])
def after_form():
    charA = request.form["personnage"]
    charB = request.form["relation"]
    entry_is_valid=False
    for i in characters:
        if (i["name"]==charA):
            entry_is_valid=True;
    if(entry_is_valid):
        if (charB==""):
            # Si seul le premier champ est renseigné, on renvoit une page spécifique au personnage en question
            return redirect(url_for('list_relations', miserables=True, name=charA))
        else:
            # Si un autre personnage est renseigné, alors on effectue la recherche de relation et on donne un résultat
            link_exists=False
            k=0
            for i in characters:
                if (charA == i["name"]):
                    for j in links:
                        if (j["source"]==k and characters[j["target"]]["name"]==charB):
                            link_exists=True
                        elif (j["target"]==k and characters[j["source"]]["name"]==charB):
                            link_exists=True
                k=k+1
            return render_template("game_result.html",
                                   title="Les Misérables | Relations entre personnages", miserable=True,
                                   areConnected=link_exists, charA=charA, charB=charB)
    else:
        return redirect(url_for('hello', error="mauvaise_saisie"))

########## Section . Recherche dichotomique ##########
@app.route("/recherche_dichotomique", methods=["GET", "POST"])
def recherche_dichotomique():
    session['min'] = 0
    session['max'] = int(request.form.get('n', 100))
    session['goal'] = random.randint(session['min'],session['max'])
    session['max_attempts'] = math.floor(math.log2(session['max'])+2)
    session['nb_attempts'] = 0
    return render_template("recherche_dichotomique.html", title="Recherche Dichotomique", dicho=True,
                           hasError=request.args.get('error'), top=session['max'], tentatives=session['max_attempts'])

@app.route("/recherche_dichotomique_resultat", methods=["POST"])
def recherche_dichotomique_resultat():
    try:
        value = int(request.form["valeur"])
    except ValueError:
        return redirect(url_for('recherche_dichotomique',
                                error="valeur_incorrecte"))
    if((value >= 0) and (value <= session['max'])):
        while(session['nb_attempts'] < session['max_attempts']-1):
            inferieur=False
            superieur=False
            session['nb_attempts'] = session['nb_attempts'] + 1
            if(value == session['goal']):
                return render_template("recherche_dicho_fin.html", title="Recherche Dichotomique", dicho=True,
                                        win=True, objectif=session['goal'])
            else:
                if(value < session['goal']):
                    inferieur=True
                else:
                    superieur=True
            return render_template("recherche_dichotomique.html", title="Recherche Dichotomique", dicho=True,
                        inferieur=inferieur, superieur=superieur, reste = session['max_attempts'] - session['nb_attempts'],
                        tentatives=session['max_attempts'],valeur=value, top=session['max'])
        if(value == session['goal']):
                return render_template("recherche_dicho_fin.html", title="Recherche Dichotomique", dicho=True,
                                        win=True, objectif=session['goal'])
        else:
            return render_template("recherche_dicho_fin.html", title="Recherche Dichotomique",dicho=True,
                                       win=False, objectif=session['goal'], valeur=value)
    return redirect(url_for('recherche_dichotomique',
                            error="valeur_incorrecte"))

########## Section . Analyse PIX ##########

### Informations pix
pix_subdomain_names = ["1.1 Mener une recherche et une veille d’information",
                    "1.2 Gérer des données",
                    "1.3 Traiter des données",
                    "2.1 Interagir",
                    "2.2 Partager et publier",
                    "2.3 Collaborer",
                    "2.4 S'insérer dans le monde numérique",
                    "3.1 Développer des documents textuels",
                    "3.2 Développer des documents multimedia",
                    "3.3 Adapter les documents à leur finalité",
                    "3.4 Programmer",
                    "4.1 Sécuriser l'environnement numérique",
                    "4.2 Protéger les données personnelles et la vie privée",
                    "4.3 Protéger la santé le bien-être et l'environnement",
                    "5.1 Résoudre des problèmes techniques",
                    "5.2 Construire un environnement numérique"]
pix_subdomain_ids = [1.1, 1.2, 1.3, 2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3, 3.4, 4.1, 4.2, 4.3, 5.1, 5.2]
nb_skills = len(pix_subdomain_names)
pix_domain_names = ["1 - Information et données",
                    "2 - Collaboration et communication",
                    "3 - Création de contenu",
                    "4 - Protection et sécurité",
                    "5 - Environnement numérique"]

pix_expectations = [4,4,4,4,4,4,3,4,3,4,3,4,3,3,3,3]

### Fonctions d'analyse PIX ###
def average_domains(results, domain_names, subdomain_names):
    res = []
    for student in results:
        i = 0
        j = 0
        s = []
        while (i<len(domain_names)):
            if (j == len(subdomain_names)):
                break
            k = 0
            sum = 0
            while (j<len(subdomain_names) and (domain_names[i][0] == subdomain_names[j][0])):
                sum += student[j]
                k += 1
                j += 1
            i += 1
            s.append(float(sum/k))
        res.append(s)
    return np.array(res)

def stat_matrix(dataset, labels=None):
    matrix = []
    i=0
    for skill in dataset:
        skill_stats = []
        if (labels):
            skill_stats.append(labels[i])
        skill_stats.append(format(np.average(skill), '0.2f'))
        skill_stats.append(format(np.median(skill), '0.2f'))
        skill_stats.append(format(np.std(skill), '0.2f'))
        skill_stats.append(format(np.percentile(skill, 25), '0.2f'))
        skill_stats.append(format(np.percentile(skill, 75), '0.2f'))
        skill_stats.append(format(np.amin(skill), '0.2f'))
        skill_stats.append(format(np.amax(skill), '0.2f'))
        matrix.append(skill_stats)
        i += 1
    return matrix

def make_csv(matrix, headers=None, separator=',', end_of_line='\n'):
    lines = []
    if (headers):
        lines.append(separator.join(headers))
    for line in matrix:
        lines.append(separator.join(line))
    return end_of_line.join(lines)

def nb_subdomains_failed(student_results):
    failed = 0
    i = 0
    while(i<len(student_results)):
        if(student_results[i] == 0):
            failed += 1
        i += 1
    return failed

def nb_students_failed(results, n=nb_skills):
    nb_students = 0
    for student_results in results:
        if (nb_subdomains_failed(student_results) == n):
            nb_students += 1
    return nb_students

def nb_students_failed_cumul(results, n=nb_skills):
    nb_students = 0
    for student_results in results:
        if (nb_subdomains_failed(student_results) >= n):
            nb_students += 1
    return nb_students

def nb_subdomains_passed(student_results, expectations):
    passed = 0
    i = 0
    while(i<len(student_results)):
        if(student_results[i] >= expectations[i]):
            passed +=  1
        i += 1
    return passed

def nb_students_certified(results, n=nb_skills):
    nb_students = 0
    for student_results in results:
        if (nb_subdomains_passed(student_results, pix_expectations) == n):
            nb_students += 1
    return nb_students

def nb_students_certified_cumul(results, n=nb_skills):
    nb_students = 0
    for student_results in results:
        if (nb_subdomains_passed(student_results, pix_expectations) >= n):
            nb_students += 1
    return nb_students

def nb_failures_subdomains(results, n=0):
	res = np.zeros(nb_skills, dtype=np.int)
	for student in results:
		i = 0
		for level in student:
			if (level == 0):
				if (n):
					if (nb_subdomains_failed(student) == n):
						res[i] += 1
				else :
					res[i] += 1
			i += 1
	return res



# Data PIX

#path_position = "static/pix_data/data_pix_position.csv"
#path_certif = "static/pix_data/data_pix_certif.csv"

path_position = os.path.join(root, "static/pix_data", "data_pix_position.csv")
path_certif = os.path.join(root, "static/pix_data", "data_pix_certif.csv")

pix_position = np.loadtxt(path_position, skiprows=1, delimiter=',')
pix_certif = np.loadtxt(path_certif, skiprows=1, delimiter=',')

pix_position_transposed = pix_position.transpose()
pix_certif_transposed = pix_certif.transpose()

pix_position_domains = average_domains(pix_position, pix_domain_names, pix_subdomain_names)
pix_certif_domains = average_domains(pix_certif, pix_domain_names, pix_subdomain_names)
pix_position_domains_transposed = pix_position_domains.transpose()
pix_certif_domains_transposed = pix_certif_domains.transpose()

# Ces statistiques doivent correspondre à celles de la fonction 'stat_matrix'
statistiques = ['label', 'Moyenne', 'Médiane', 'Écart_type', 'Premier_quartile', 'Troisième_quartile', 'Minimum','Maximum']

# Couleurs utilisées pour les diagrammes circulaires
colorscale = ["#0D1981","#113C99","#1768B0","#1D9AC6","#39C5D0","#55D9CB"]

@app.route('/pix/data_pix.ods')
def pix_dataset():
    return send_from_directory('static/pix_data', 'data_pix.ods')

@app.route('/pix/<source>_subdomains.csv')
def data_subdomains(source):
    if (source not in ['Positionnement', 'Certification']):
        return redirect(url_for('analyse_globale'))

    if (source == 'Positionnement'):
        results = pix_position_transposed
    else:
        results = pix_certif_transposed

    stats = stat_matrix(results, pix_subdomain_names)
    csv = make_csv(stats, statistiques)
    content = make_response(csv)
    content.headers["Content-type"] = "text/csv"
    return content

@app.route('/pix/<source>_domains.csv')
def data_domains(source):
    if (source not in ['Positionnement', 'Certification']):
        return redirect(url_for('analyse_globale'))

    if (source == 'Positionnement'):
        results = pix_position_domains_transposed
    else:
        results = pix_certif_domains_transposed

    stats = stat_matrix(results, pix_domain_names)
    csv = make_csv(stats, statistiques)
    content = make_response(csv)
    content.headers["Content-type"] = "text/csv"
    return content

@app.route('/pix')
def analyse_globale():
    failed_subdomains = nb_failures_subdomains(pix_certif).tolist()
    failed_subdomains_1 = nb_failures_subdomains(pix_certif, 1).tolist()
    failed_subdomains_2 = nb_failures_subdomains(pix_certif, 2).tolist()
    failed_subdomains_3 = nb_failures_subdomains(pix_certif, 3).tolist()
    failed_subdomains_4 = nb_failures_subdomains(pix_certif, 4).tolist()
    stats_position = stat_matrix(pix_position_transposed, pix_subdomain_names)
    stats_certif = stat_matrix(pix_certif_transposed, pix_subdomain_names)
    stats_position_domains = stat_matrix(pix_position_domains_transposed, pix_domain_names)
    stats_certif_domains = stat_matrix(pix_certif_domains_transposed, pix_domain_names)
    certif_vs_expectations = []
    position_vs_expectations = []
    number_of_failures = []
    i = 0
    while(i<=len(pix_subdomain_names)):
        certif_vs_expectations.append(nb_students_certified(pix_certif,i))
        position_vs_expectations.append(nb_students_certified(pix_position,i))
        number_of_failures.append(nb_students_failed(pix_certif, i))
        i += 1
    return render_template("analyse_globale.html", title="Analyse PIX", pix=True,
							failed_subdomains = failed_subdomains,
                            failed_subdomains_1 = failed_subdomains_1,
                            failed_subdomains_2 = failed_subdomains_2,
                            failed_subdomains_3 = failed_subdomains_3,
                            failed_subdomains_4 = failed_subdomains_4,
                            stats_position = stats_position,
                            stats_position_domains = stats_position_domains,
                            stats_certif = stats_certif,
                            stats_certif_domains = stats_certif_domains,
                            expectations = pix_expectations,
                            certif_vs_expectations = certif_vs_expectations,
                            position_vs_expectations = position_vs_expectations,
                            failures = number_of_failures,
                            domain_names = pix_domain_names,
                            subdomain_names = pix_subdomain_names,
                            subdomain_ids = pix_subdomain_ids,
                            statistiques = statistiques)

@app.route('/pix_competences')
def analyse_competences():
    id_subdomain = request.args.get('id', '0')

    if (int(id_subdomain) >= nb_skills):
        return redirect(url_for('analyse_globale'))

    stats_subdomain_positionnement = []
    stats_subdomain_certification = []
    i = 0
    while(i <= 5):
        stats_subdomain_positionnement.append(np.count_nonzero(pix_position_transposed[int(id_subdomain)] == i))
        stats_subdomain_certification.append(np.count_nonzero(pix_certif_transposed[int(id_subdomain)] == i))
        i += 1
    return render_template("analyse_competences.html", title="Analyse PIX | Les Compétences", pix=True,
        subdomain = id_subdomain,
        effectifs_note_positionnement = stats_subdomain_positionnement,
        effectifs_note_certification = stats_subdomain_certification,
        subdomain_names = pix_subdomain_names,
        subdomain_name = pix_subdomain_names[int(id_subdomain)],
        colors = colorscale)

@app.route('/pix_methodologie')
def methodologie():
	return render_template('methodologie.html', title='PIX | Méthodologie', pix=True)

#NE SURTOUT PAS MODIFIER
if __name__ == "__main__":
   app.run(debug=True)
