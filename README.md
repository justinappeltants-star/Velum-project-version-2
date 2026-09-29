L'histoire de la cabane secrète

Imagine que tu veux parler avec tes copains sans que personne d'autre ne puisse écouter, même pas le facteur qui porte tes lettres.

La clé magique : tu inventes une clé secrète, très très longue, avec plein de lettres et de chiffres. Personne ne peut la deviner, même en essayant pendant des millions d'années.
Le cadenas : avant d'envoyer un message, ton ordinateur le met dans une boîte fermée avec un cadenas. Le message devient un charabia du genre « x8Kp2!qZ… ».
Le facteur aveugle : notre serveur est comme un facteur qui ne sait pas lire et n'a jamais la clé. Il prend les boîtes fermées et les distribue aux copains de la cabane, sans savoir ce qu'il y a dedans.
Le déchiffrage : tes copains ont la même clé. Leur ordinateur ouvre la boîte, et le message redevient lisible, seulement chez eux.
La cabane qui disparaît : tu choisis combien de temps la cabane existe (15 minutes, 1 heure, 7 jours…). Quand le temps est fini, pouf ! elle disparaît avec tous les messages. Si personne ne parle pendant 5 minutes (quand tu coches cette option), elle disparaît aussi.
Comment j'ai construit le projet, de A à Z

A. L'idée. Une messagerie sans compte, sans mémoire, où personne ne peut lire les messages, pas même celui qui héberge le site.

B. Le plan. Il faut deux morceaux :

Le visage (index.html) : la page que les gens voient, avec les boutons, l'explication et le chat. C'est aussi là que se fait le chiffrement.
Le cerveau (server.py, en Python) : il crée les salons, passe les messages chiffrés et détruit les salons quand le temps est fini.

C. La clé. Quand quelqu'un crée un salon, son navigateur fabrique 32 octets au hasard. Ça donne le code de 43 caractères. Cette clé reste dans le navigateur et n'est jamais envoyée au serveur.

D. L'adresse du salon. Le serveur doit quand même reconnaître le salon. On lui donne donc une empreinte du code (SHA-256), comme une empreinte de doigt : elle identifie la clé mais ne permet pas de la retrouver.

E. Le chiffrement. Chaque message est chiffré avec AES-256-GCM, un cadenas ultra solide. Chaque message a un numéro unique (l'IV), donc deux messages identiques ne donnent jamais le même charabia. Le mode GCM ajoute un sceau anti-triche : si quelqu'un modifie la boîte, elle refuse de s'ouvrir.

F. Le tuyau direct. Les messages voyagent par WebSocket, un tuyau toujours ouvert entre le navigateur et le serveur. C'est ce qui rend le chat instantané.

G. Le minuteur. Le serveur vérifie toutes les 2 secondes si un salon a dépassé son temps (15 min à 7 jours) ou s'il est resté 5 minutes sans message, quand l'option est cochée. Si oui, il le supprime et prévient tout le monde.

H. Les protections. J'ai ajouté des limites : 20 messages par 10 secondes, 50 personnes maximum par salon, pas plus de 10 créations par minute et par personne. Il y a aussi des en-têtes de sécurité qui empêchent d'autres sites d'espionner ou d'intégrer Velum.

I. La mise en ligne. On loue un petit serveur, on achète un nom de domaine, on lance le programme, et Caddy ajoute automatiquement le cadenas HTTPS. Ensuite tout le monde peut y accéder.

Ton texte de présentation (environ 2 minutes)

« Bonjour à tous. Je vais vous présenter Velum.

Velum, c'est une messagerie anonyme, éphémère et chiffrée. Pas de compte, pas d'e-mail, pas d'historique.

Comment ça marche ? Cinq idées.

Un : la clé. Quand je crée un salon, mon navigateur génère un code secret de 256 bits. Ce code ne quitte jamais mon appareil. C'est la seule clé d'entrée.

Deux : le cadenas. Chaque message est chiffré avec AES-256-GCM avant de partir. Ce standard est utilisé par les banques et les gouvernements. Trouver la clé par force brute est impossible en pratique. Et si quelqu'un modifie un message, il est automatiquement rejeté.

Trois : le facteur aveugle. Notre serveur ne voit que du charabia. Il transmet les messages sans pouvoir les lire, parce qu'il n'a jamais la clé. On appelle ça le zéro connaissance.

Quatre : le minuteur. À la création, on choisit la durée du salon : de 15 minutes à 7 jours. On peut aussi activer une destruction après 5 minutes d'inactivité.

Cinq : la disparition. Quand le temps est écoulé, le salon est effacé de la mémoire du serveur, et la clé et les messages sont effacés du navigateur. Rien n'est stocké sur disque, donc il n'y a rien à retrouver ni à voler.

Soyons honnêtes sur les limites. Aucun système n'est parfait à 100 %. Si quelqu'un obtient le code, il peut lire le salon. Une capture d'écran reste possible. Et pour cacher son adresse IP, il faut utiliser Tor ou un VPN.

Velum, c'est donc une cabane secrète numérique : une clé, un cadenas, un facteur qui ne sait pas lire, et un minuteur qui détruit tout. Merci ! »

Pour le retenir facilement

Retiens 5 mots dans l'ordre : Clé → Cadenas → Facteur aveugle → Minuteur → Disparition.

Répète-les en imaginant une cabane : tu fabriques une clé, tu fermes le cadenas, le facteur aveugle passe la boîte, le minuteur sonne, la cabane disparaît. Avec cette image, tu peux improviser chaque partie avec tes propres mots.

Questions probables du public
« Le serveur peut-il lire mes messages ? » Non, il n'a jamais la clé.
« Que se passe-t-il si le serveur est piraté ? » Le pirate ne trouve que du charabia et aucune clé. Le serveur n'écrit rien sur disque, et tout ce qui est en mémoire disparaît au redémarrage.
« Peut-on récupérer un salon détruit ? » Non, c'est voulu.
« Est-ce anonyme à 100 % ? » Le contenu est protégé. Pour cacher l'adresse IP, il faut ajouter Tor.



















L'image à retenir : un jeu multijoueur avec des coffres

Imagine un jeu en ligne où :

ton ordinateur (le navigateur) verrouille chaque message dans un coffre ;
le serveur est un robot livreur qui transporte les coffres sans pouvoir les ouvrir ;
un chronomètre détruit la salle de jeu quand le temps est fini.

Le projet a 2 cerveaux qui se parlent :

Fichier	Langage	Rôle
index.html	HTML + CSS + JavaScript	Ce que tu vois. C'est aussi lui qui chiffre et déchiffre
server.py	Python	Le robot livreur : il crée les salles, transmet les coffres, détruit les salles

Ajoute à ça 3 petits fichiers pour la mise en ligne : requirements.txt, Dockerfile et README.md.

Pourquoi 2 langages ? Le navigateur ne comprend que HTML/CSS/JavaScript. Python, lui, est parfait pour le serveur. Le HTML dessine la page, le CSS la décore, le JavaScript la fait vivre.

PARTIE 1 : Le serveur (server.py)
1. Les outils importés
python
import asyncio, json, re, time
from fastapi import FastAPI, WebSocket

Comme prendre des outils dans une boîte avant de bricoler :

asyncio : faire plusieurs choses en même temps sans se bloquer ;
json : le format pour envoyer des données ;
re : les « expressions régulières », pour vérifier qu'un texte a la bonne forme ;
time : lire l'heure ;
FastAPI : le framework (kit de construction) qui crée le serveur web.
2. Les règles du jeu (les constantes)
python
TTLS = {900, 1800, 3600, 10800, 86400, 259200, 604800}
IDLE_SECONDS = 300
MAX_USERS = 50

TTLS est la liste des durées autorisées, en secondes (900 s = 15 min, 604800 s = 7 jours). IDLE_SECONDS = 300, c'est 5 minutes d'inactivité. MAX_USERS limite chaque salle à 50 personnes.

3. Le cahier en mémoire
python
rooms: dict = {}

Un dictionnaire Python : un cahier où chaque salle a un nom (son identifiant) et une fiche. Il est en RAM et n'est jamais écrit sur le disque. Quand le serveur s'éteint, la RAM s'efface, donc tout disparaît.

4. La fiche d'une salle (la classe)
python
class Room:
    def __init__(self, ttl, idle):
        self.expires = time.time() + ttl
        self.idle = idle
        self.last = time.time()
        self.socks = set()

Une classe est un moule pour fabriquer des objets. Chaque salle retient :

expires : l'heure de sa destruction (maintenant + la durée choisie) ;
idle : la case « détruire après 5 min d'inactivité » est-elle cochée ? ;
last : l'heure du dernier message ;
socks : la liste des personnes connectées.
5. Envoyer et diffuser
python
async def send(ws, payload): ...
async def broadcast(room, payload):
    await asyncio.gather(*(send(w, payload) for w in list(room.socks)))

send envoie à une personne. broadcast envoie à tout le monde dans la salle, en même temps, grâce à asyncio.gather. Le mot async veut dire « je peux attendre sans bloquer les autres », et await veut dire « j'attends ici que ce soit fini ».

6. Le démolisseur
python
async def destroy(rid, reason):
    room = rooms.pop(rid, None)
    ...
    await w.close(4000)

rooms.pop retire la salle du cahier. Ensuite le serveur prévient chaque personne (« salle détruite ») et ferme sa connexion.

7. Le gardien qui surveille le temps
python
async def reaper():
    while True:
        await asyncio.sleep(2)
        ...
        if now >= r.expires: destroy(...)
        elif r.idle and now - r.last >= IDLE_SECONDS: destroy(...)

Reaper veut dire « faucheur ». C'est une boucle infinie (while True) qui, toutes les 2 secondes (asyncio.sleep(2)), regarde chaque salle et se demande si son temps est fini ou si elle est restée 5 minutes sans message. Si oui, il la détruit. Il est lancé au démarrage avec asyncio.create_task(reaper()) dans la fonction lifespan.

8. Les portes du serveur (les routes)

Un serveur a des « portes » (des adresses), et chacune fait une chose :

Décorateur	Adresse	Ce que ça fait
@app.get("/")	/	Donne la page index.html
@app.post("/api/rooms")	/api/rooms	Crée une salle
@app.websocket("/ws/{rid}")	/ws/...	Ouvre le tuyau de discussion

La création vérifie plein de choses avant d'accepter :

python
class NewRoom(BaseModel):
    id: str
    ttl: int
    idle: bool = False

BaseModel (de Pydantic) contrôle automatiquement le format des données reçues. Ensuite le code refuse si l'identifiant n'a pas la bonne forme (ID_RE.match), si la durée n'est pas dans TTLS, ou si la personne crée trop de salles (erreur 429, « trop de demandes »).

9. Le WebSocket, le tuyau magique

Normalement, un site web fonctionne par questions et réponses : tu demandes, le serveur répond, puis la connexion se ferme. Un WebSocket garde le tuyau ouvert en permanence dans les deux sens, comme un appel téléphonique. C'est ce qui rend le chat instantané.

python
await ws.accept()
room.socks.add(ws)
while True:
    data = await ws.receive_text()
    room.last = now
    await broadcast(room, {"type": "msg", "d": data})
accept() accepte la connexion ;
on ajoute la personne à la salle ;
la boucle attend un message (receive_text) ;
elle note l'heure (room.last), ce qui remet à zéro le compte des 5 minutes ;
elle rediffuse le coffre chiffré à tous (broadcast).

Le serveur ne fait jamais decrypt, ne lit jamais data et ne le stocke pas.

10. Les gardes du corps

Pour éviter que des méchants abusent du site :

Anti-spam : 20 messages maximum par 10 secondes (bucket) ;
Taille limite : MAX_MSG = 16384 caractères ;
Contrôle d'origine : on vérifie l'en-tête origin, pour qu'un autre site ne puisse pas se brancher en douce ;
En-têtes de sécurité (security_headers), dont le Content-Security-Policy, qui interdit à la page de charger des scripts venus d'ailleurs.
PARTIE 2 : La page (index.html)
1. Les trois couches
HTML : le squelette (<button>, <select>, <input>…) ;
CSS : la déco. Le mode sombre vient des variables --bg, --ac… ;
JavaScript : le cerveau, dans la balise <script>.
2. Fabriquer la clé
js
const rnd = n => crypto.getRandomValues(new Uint8Array(n));
await setup(b64(rnd(32)));

crypto.getRandomValues est le générateur de vrai hasard cryptographique du navigateur. rnd(32) produit 32 octets, soit 32 × 8 = 256 bits. b64(...) les transforme en texte lisible, le fameux code de 43 caractères.

3. Préparer le cadenas
js
S.key = await crypto.subtle.importKey('raw', raw, 'AES-GCM', false, ['encrypt','decrypt']);
S.id  = hex(await crypto.subtle.digest('SHA-256', te.encode('velum-id:'+code)));
crypto.subtle est la boîte à outils de cryptographie intégrée au navigateur. Personne n'a réinventé le chiffrement : on utilise l'outil officiel, testé par des experts ;
importKey transforme nos octets en clé AES-GCM utilisable ;
digest('SHA-256', ...) calcule l'empreinte du code, qui devient l'identifiant de la salle. Cette empreinte va au serveur, mais elle est à sens unique : impossible d'en retrouver la clé.
4. Chiffrer un message
js
async function enc(o){
  const iv = rnd(12);
  const ct = await crypto.subtle.encrypt(
    {name:'AES-GCM', iv, additionalData: te.encode(S.id)}, S.key, te.encode(JSON.stringify(o)));
  ...
}
JSON.stringify transforme le message (pseudo + texte) en texte ;
te.encode (TextEncoder) le transforme en octets ;
on crée un IV (vecteur d'initialisation) de 12 octets au hasard, unique pour chaque message : même phrase deux fois donne deux charabias différents ;
crypto.subtle.encrypt chiffre le tout en AES-GCM ;
additionalData lie le message à cette salle précise : un coffre copié dans une autre salle ne s'ouvre pas ;
on colle l'IV devant le message chiffré, puis on envoie.

Déchiffrer (dec) fait l'inverse avec crypto.subtle.decrypt. Si quelqu'un a modifié un seul octet, GCM le détecte et une erreur est lancée : le message est ignoré (« Message illisible ou falsifié »).

5. Parler au serveur
js
fetch('/api/rooms', {method:'POST', body: JSON.stringify({...})})
ws = new WebSocket('wss://' + location.host + '/ws/' + S.id);
ws.onmessage = ...
ws.send(await enc({...}))
fetch fait une requête classique pour créer la salle ;
new WebSocket ouvre le tuyau permanent (wss:// signifie WebSocket sécurisé) ;
ws.onmessage réagit quand un message arrive : info, count (nombre de participants), msg ou destroyed ;
ws.send envoie le coffre déjà chiffré.
6. Le compte à rebours
js
setInterval(tick, 1000);

setInterval appelle la fonction tick chaque seconde. Elle met à jour le temps restant affiché en haut. Le vrai chef reste le serveur : le compte à rebours de la page n'est qu'un affichage.

7. Les protections dans la page
Anti-XSS : on affiche les messages avec textContent et jamais innerHTML. Si quelqu'un envoie du code malveillant, il s'affiche comme du texte inoffensif ;
history.replaceState efface le code de la barre d'adresse après l'entrée dans le salon ;
Le code après le # de l'URL n'est jamais envoyé au serveur : c'est une règle des navigateurs. C'est pour ça que le lien d'invitation est site.com/#CODE ;
À la destruction, la fonction destroyed() fait S={} et vide les messages (textContent=''). La clé est effacée.
PARTIE 3 : Les fichiers de mise en ligne
requirements.txt : la liste de courses Python (fastapi, uvicorn). On l'installe avec pip install -r requirements.txt ;
uvicorn : le moteur qui fait tourner server.py (uvicorn server:app). L'option --no-access-log désactive les journaux de visites pour ne garder aucune trace ;
Dockerfile : la recette pour emballer le projet dans un conteneur qui marche partout ;
systemd : garde le serveur allumé et le relance s'il plante ;
Caddy : ajoute le cadenas HTTPS automatiquement, et relaie aussi les WebSockets ;
ufw : le pare-feu, qui ne laisse ouverts que les ports 22, 80 et 443 ;
DNS, enregistrement A : l'annuaire qui relie ton nom de domaine à l'adresse IP du serveur.
Ton texte de présentation (environ 3 minutes)

« Bonjour ! Je vais vous expliquer comment j'ai construit Velum, une messagerie anonyme et chiffrée.

Le projet tient en deux fichiers. D'un côté index.html, la page que vous voyez, écrite en HTML, CSS et JavaScript. De l'autre server.py, le serveur, écrit en Python avec le framework FastAPI.

Première étape, la clé. Avec crypto.getRandomValues, le navigateur génère 256 bits aléatoires. C'est le code secret. Il ne quitte jamais l'appareil.

Deuxième étape, le chiffrement. J'utilise crypto.subtle, la boîte à outils cryptographique du navigateur, avec l'algorithme AES-256-GCM. Chaque message a un IV unique et un sceau d'intégrité : si on le modifie, il est rejeté.

Troisième étape, l'identifiant. Avec SHA-256, je calcule une empreinte à sens unique du code. Le serveur ne connaît que cette empreinte, jamais la clé.

Quatrième étape, le serveur. Il a trois portes : GET / pour la page, POST /api/rooms pour créer un salon, et un WebSocket pour discuter en temps réel. Il reçoit un message chiffré et le rediffuse à tout le monde avec la fonction broadcast, sans jamais le lire ni le stocker.

Cinquième étape, le minuteur. Une boucle appelée reaper tourne toutes les 2 secondes. Elle supprime les salons dont la durée est finie, ou qui ont 5 minutes d'inactivité quand l'option est activée. Tout vit en RAM : au redémarrage, tout disparaît.

Sixième étape, les protections. Anti-spam, limite de taille, contrôle d'origine, en-têtes de sécurité, et affichage avec textContent pour bloquer les injections de code.

Dernière étape, la mise en ligne. Un serveur, un nom de domaine, uvicorn pour lancer le programme, systemd pour le garder allumé, et Caddy pour le HTTPS automatique.

Le principe, c'est le zéro connaissance : celui qui transporte les messages ne peut pas les lire. Merci ! »

Comment le retenir : la phrase code

« C.I.S.T.E.R.M. » ne marche pas ? Retiens plutôt 5 verbes dans l'ordre :

Générer → Chiffrer → Envoyer → Diffuser → Détruire

Générer la clé (getRandomValues) ;
Chiffrer le message (AES-GCM) ;
Envoyer dans le tuyau (WebSocket) ;
Diffuser aux autres (broadcast) ;
Détruire au bout du temps (reaper).
Questions techniques probables
« Pourquoi Python ? » Il est lisible et rapide à écrire, et FastAPI gère très bien les WebSockets.
« Pourquoi pas une base de données ? » Ce qui n'est jamais écrit sur disque ne peut pas être volé plus tard. La RAM s'efface toute seule.
« Pourquoi chiffrer dans le navigateur et pas sur le serveur ? » Si le serveur chiffrait, il verrait la clé. Ici, seul l'appareil des utilisateurs la connaît.
« Pourquoi HTTPS est-il obligatoire ? » crypto.subtle ne fonctionne que dans un contexte sécurisé (HTTPS ou localhost).
« Pourquoi un seul worker ? » Les salons sont dans la mémoire d'un seul processus. Avec plusieurs workers, chacun aurait son propre cahier.
« Quelle est la faiblesse principale ? » Le code JavaScript vient du serveur : un serveur piraté pourrait servir une page piégée. C'est pour ça qu'il vaut mieux héberger Velum soi-même.
