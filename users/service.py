import random
from django.utils import timezone

from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives

from threading import Thread

from .models import Code, CustomUser


def send_email_letter():
    send_mail(
        subject='Test Message',
        message='test message',
        from_email='djamolovramazon90@gmail.com',
        recipient_list=['djamolovramazon90@gmail.com'],
        html_message="""
            <main>
                <h1>Hush kelibsiz Oqila </h1>
            </main>
        """
    )


def send_email_file_and_text():
    path = 'file.pdf'
    email = EmailMessage(
        subject='Hush kelibsiz Oqila',
        body='test message',
        from_email='djamolovramazon90@gmail.com',
        to=['djamolovramazon90@gmail.com'],
    )

    with open(path, 'rb') as f:
        email.attach(filename=path, content=f.read(), mimetype='application/pdf')
        email.send()


def send_email_multiAlternatives():
    subject = 'Hush kelibsiz Ramazon'
    body = 'test bu body text '
    from_email = 'djamolovramazon90@gmail.com'
    to = ['djamolovramazon90@gmail.com']
    html_c = """<main>    html       <h1>Hush kelibsiz Ramazon </h1>             </main>"""

    email = EmailMultiAlternatives(
        subject=subject,
        body=body,
        from_email=from_email,
        to=to,
    )

    email.attach_alternative(html_c, 'text/html')
    with open('file.pdf', 'rb') as f:
        email.attach(filename='file.pdf', content=f.read(), mimetype="application/pdf")
    email.send()


def send_email_alternative2(to, user1):
    reset_link = 'http://127.0.0.1:8000/restore_password/'
    subject = 'Forget password'
    from_email = 'djamolovramazon90@gmail.com'
    to = [to]
    text_content = 'test'
    code = code_generate()
    print(type(str(user1)), "mening emaildagi user1 ")
    time = timezone.now()

    # user = user1
    # print(user)
    Code.objects.create(code_number=code, user=user1)

    html_c = f"""
    <main>
        <h1>Salom, {user1}!</h1>
         <h2> {code}</h2>
        <p>Sizning hisobingiz uchun parolni tiklash so‘rovi qabul qilindi.</p>
        <p>Agar bu so‘rovni siz bajargan bo‘lsangiz, davom etish uchun quyidagi tugmani bosing.</p>
        <a href="{reset_link}" style="display: inline-block; padding: 10px 20px; margin-top: 10px; background-color: #007bff; color: white; text-decoration: none; border-radius: 5px;">Parolni Tiklash</a>
        <p>Agar bu so‘rov sizga tegishli bo‘lmasa, hech qanday harakat qilishingiz shart emas.</p>

        # <h1>time = 12.0<h1>
    </main> 
    """

    email = EmailMultiAlternatives(
        subject, text_content, from_email, to
    )

    email.attach_alternative(html_c, 'text/html')
    email.send()


def send_email_asinc(to, user1):
    thread1 = Thread(target=send_email_alternative2, args=(to, user1))
    thread1.start()


def code_generate():
    code = random.randint(1000, 9999)
    return code
