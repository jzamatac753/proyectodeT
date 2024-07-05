import pytest

from models.entities.User import User
from scrypts.serviciosExt import *
from scrypts.serviciosNLP import *


@pytest.mark.parametrize(
        "password",
    [
        ("12345678"),
        ("abcdefgh"),
        ("ABCDEFGH"),
        ("a2#D"),
    ]
)
def testCheckPassword(password):
    aux = User.generate_password(password)
    assert True == User.check_password(aux, password)

def testCheckPasswordNot():
    aux = User.generate_password("contrasenha")
    assert False == User.check_password(aux, "password")
    
def testResourceExtraction():
    assert None != extraccionRecursosEntregados("https://classroom.google.com/u/0/c/NDg4NjMzOTA4NjQy/a/NTQ4MzIyMzYxMDg1/details?hl=es")

def testCommentsExtraction():
    assert None != extraccionComentariosClases("https://classroom.google.com/u/0/c/NDg4NjMzOTA4NjQy/a/NTQ4MzIyMzYxMDg1/details?hl=es")

@pytest.mark.parametrize(
        "url_doc",
    [
        ('https://drive.google.com/file/d/1LqE1yxAFWo2yaPTgXczRIabZBQ61qMu6/view?hl=es'),
    ]
)
def testResourceDocPower(url_doc):
    assert None != text_power_point(url_doc)

@pytest.mark.parametrize(
        "url_docs",
    [
        (['https://drive.google.com/file/d/1LqE1yxAFWo2yaPTgXczRIabZBQ61qMu6/view?hl=es']),
    ]
)
def testContentSimple(url_docs):
    row_list = []
    diccionario_aux = {} 
    assert None != generacioncontenido_palabrassimples(row_list, diccionario_aux, url_docs)


@pytest.mark.parametrize(
        "url_docs",
    [
        (['https://drive.google.com/file/d/1LqE1yxAFWo2yaPTgXczRIabZBQ61qMu6/view?hl=es']),
    ]
)
def testContentCompuest(url_docs):
    row_list_simp = []
    diccionario_aux_simples = {}
    assert None != generacioncontenido_palabrascompuestas(row_list_simp, diccionario_aux_simples, url_docs)