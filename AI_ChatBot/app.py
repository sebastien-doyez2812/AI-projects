from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from flask import Flask, request, jsonify
questions = [
    "Quel est ton nom ?", "Comment t'appelles-tu ?", "Qui es-tu ?", 
    "Comment est Seb ?", "Décris-moi ton créateur", "Peux-tu décrire Sébastien ?", 
    "Quelles sont ses compétences ?", "Peux-tu parler de ses projets ?", 
    "Quels projets mène-t-il actuellement ?", "Quels sont ses objectifs de carrière ?", 
    "Comment puis-je contacter Sébastien ?", "Quel est son mail ?", 
    "Sébastien a-t-il un LinkedIn ?", "Quels sont ses projets à long terme ?"
]

reponses = [
    "Je m'appelle CyberSeb, j'ai été conçu par Sébastien Doyez, un ingénieur français spécialisé en IA, robotique et vision par ordinateur. Mon but est de vous décrire Seb et ses projets !",
    "Mon nom est CyberSeb, un assistant virtuel créé par Sébastien Doyez, ingénieur français spécialisé en IA, robotique et vision par ordinateur. Posez-moi toutes vos questions !",
    "Je suis CyberSeb, une IA conçue par Sébastien Doyez. Je suis ici pour répondre à toutes vos questions concernant Seb et ses projets.",
    "Sébastien est un ingénieur français vivant au Canada. Il a découvert le Québec à 22 ans et y vit désormais, travaillant en IA, robotique et vision par ordinateur.",
    "Mon créateur, Sébastien Doyez, est un ingénieur passionné par la technologie, notamment l'intelligence artificielle, la vision par ordinateur et la robotique. Il vit à Montréal, Canada.",
    "Sébastien est un ingénieur français spécialisé en IA, vision par ordinateur et robotique. Il a vécu plusieurs expériences enrichissantes au Canada et continue de se perfectionner dans ces domaines.",
    "Les compétences de Sébastien incluent l'intelligence artificielle, la vision par ordinateur, la robotique, et le développement logiciel.",
    "Sébastien travaille sur des projets variés, incluant des systèmes d'IA pour la reconnaissance d'objets et la création de robots. Il partage tout cela sur son Github.",
    "Actuellement, Seb travaille sur un bras robotique contrôlé par Arduino et une IA qui reconnaît des objets. Il mène aussi des projets pour des startups comme Sami Agtech.",
    "Les objectifs de Sébastien sont de continuer à innover dans le domaine de la robotique et de l'IA, en améliorant ses compétences et en collaborant sur des projets ambitieux.",
    "Vous pouvez contacter Sébastien à l'adresse doyez.sebastien34090@gmail.com ou sur son profil LinkedIn.",
    "L'adresse email de Sébastien est doyez.sebastien34090@gmail.com.",
    "Vous pouvez joindre Sébastien sur LinkedIn via ce lien : https://www.linkedin.com/in/s%C3%A9bastien-doyez-042604252/",
    "À long terme, Sébastien vise à devenir un expert reconnu dans le domaine de l'IA et de la robotique, en menant des projets innovants et ambitieux."
]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(questions)

model = SVC(kernel='linear')
model.fit(X, reponses)

app = Flask(__name__)

@app.route("/get_response",methods = ["POST"])
def get_response():
    data = request.json
    question = data.get("question", "")
    question_vect = vectorizer.transform([question])
    try:
        reponse = model.predict(question_vect)[0]
    except IndexError:
        reponse = "Désolé, je ne connais pas la réponse à cette question. Vous pouvez me poser une autre question sur Sébastien."
    return jsonify({"response": reponse})


if __name__ == "__main__":
    app.run(debug=True)
    