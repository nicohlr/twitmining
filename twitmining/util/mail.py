import smtplib
import os

def send_mail(email, name, message):

    from_adress = 'twitmining.contact@gmail.com'
    path = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'passwords.txt'))
    for i in range(4):
        path.readline()
    password = path.readline()

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_adress, password)

    # Send the mail
    msg = "Subject: Twitmining Contact\n\nSender mail: {0}\nSender name: {1}\n\nMessage:\n{2}".format(email, name, message).encode('utf-8').strip()
    server.sendmail("nicolas.houlier@grenoble-em.com", "houlier.nicolas@outlook.fr", msg)

    return True