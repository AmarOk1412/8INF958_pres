from django.db import models


class Entry(models.Model):
    name = models.CharField(max_length=100)
    mail = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    hashword = models.CharField(max_length=255)
    website = models.CharField(max_length=100)

    def __str__(self):
        str_to_return = '%s %s %s %s %s' % (
            self.name,
            self.mail,
            self.password,
            self.hashword,
            self.website)
        return str_to_return

    def get_all():
        entry = Entry.objects.all()
        return entry

    def get_all_by_entry(self, entry):
        query = list()
        name = self.get_all_by_name(entry)
        mail = self.get_all_by_mail(entry)
        password = self.get_all_by_password(entry)
        hashword = self.get_all_by_hashword(entry)
        website = self.get_all_by_website(entry)
        print(name)
        if name.count() > 0:
            query += list(name)
        if mail.count() > 0:
            query += list(mail)
        if password.count() > 0:
            query += list(password)
        if hashword.count() > 0:
            query += list(hashword)
        if website.count() > 0:
            query += list(website)
        return query

    def get_all_by_name(self, entry):
        query = Entry.objects.filter(name=entry)
        return query

    def get_all_by_mail(self, entry):
        query = Entry.objects.filter(mail=entry)
        return query

    def get_all_by_password(self, entry):
        query = Entry.objects.filter(password=entry)
        return query

    def get_all_by_hashword(self, entry):
        query = Entry.objects.filter(hashword=entry)
        return query

    def get_all_by_website(self, entry):
        query = Entry.objects.filter(website=entry)
        return query
