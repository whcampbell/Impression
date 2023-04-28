from django.forms import Form, CharField

class SearchForm(Form) :
    search_query = CharField(label="User, Style, or Medium")