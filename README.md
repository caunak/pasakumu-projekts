🛠️ Meistarklašu reģistrācijas sistēma
Šis ir Flask tīmekļa lietotnes projekts, kas ļauj lietotājiem reģistrēties un pieteikties uz meistarklasēm, bet administratoriem – izveidot jaunas meistarklases.

🔧 Izmantotās tehnoloģijas
Flask – tīmekļa ietvars (web framework)

Flask-Login – lietotāju autentifikācijai

Flask-SQLAlchemy – datubāzes modelēšanai

SQLite – lokālā datubāze

Jinja2 – HTML veidņu dzinējs (template engine)

🗄️ Datubāzes modeļi
Projektā tiek izmantoti trīs galvenie datu modeļi:

User – lietotāji ar id, username, password (šifrēta) un role (user/admin)

Workshop – meistarklases ar title, description, date, capacity

Registration – sasaista lietotājus ar meistarklasēm (user_id, workshop_id)

🔐 Autentifikācija
Lietotājs var reģistrēties, aizpildot formu. Parole tiek šifrēta, izmantojot generate_password_hash().

Pieslēdzoties (login), parole tiek pārbaudīta ar check_password_hash().

Pēc pieslēgšanās lietotājs tiek saglabāts sesijā (login_user()).

🧑‍🏫 Meistarklašu sistēma
Pieslēdzies lietotājs var apskatīt pieejamās meistarklases un pieteikties.

Sistēma pārbauda, vai lietotājs jau ir pieteicies.

Ja nē, reģistrācija tiek pievienota Registration tabulā.

⚙️ Admin funkcionalitāte
Ja lietotājam ir loma admin, viņš var:

Apskatīt visu lietotāju pieteikumus

Izveidot jaunas meistarklases

🚀 Lietošanas instrukcija
Instalē atkarības:

pip install flask flask_sqlalchemy flask_login


Palaid aplikāciju:

python main.py


Atver pārlūkā:

http://localhost:5000


🧪 Noklusējuma admin lietotājs
Lietotājvārds: admin

Parole: admin123
