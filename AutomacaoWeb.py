#!/usr/bin/env python
# coding: utf-8

# !pip install selenium

# Importar o pacote Webdriver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Pegar a cotação do dólar
navegador = webdriver.Chrome()

navegador.get("https://www.google.com/")

navegador.find_element('xpath', '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').send_keys('cotacao dolar')
navegador.find_element('xpath', '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)

cot_dolar = navegador.find_element('xpath', '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute('data-value')

print(cot_dolar)

# Pegar a cotação do euro
navegador.get("https://www.google.com/")

navegador.find_element('xpath', '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys('cotacao euro')
navegador.find_element('xpath', '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)

cot_euro = navegador.find_element('xpath', '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute('data-value')

print(cot_euro)


# Pegar a cotação do ouro
navegador.get('https://www.melhorcambio.com/ouro-hoje')

cot_ouro = navegador.find_element('xpath', '//*[@id="comercial"]').get_attribute('value')
cot_ouro = cot_ouro.replace(',', '.')

print(cot_ouro)

navegador.quit()


# Atualizar a base de dados
import pandas as pd

tabela = pd.read_excel('Produtos.xlsx')
display(tabela)


# Recalcular os preços
# Atualizar as cotações
tabela.loc[tabela["Moeda"] == "Dólar", "Cotação"] = float(cot_dolar)
tabela.loc[tabela["Moeda"] == "Euro", "Cotação"] = float(cot_euro)
tabela.loc[tabela["Moeda"] == "Ouro", "Cotação"] = float(cot_ouro)

tabela["Preço de Compra"] = tabela["Preço Original"] * tabela["Cotação"]

tabela["Preço de Venda"] = tabela["Preço de Compra"] * tabela["Margem"]

display(tabela)

# Exportar a base de dados atualizada
tabela.to_excel("Produtos_Novos.xlsx", index=False)