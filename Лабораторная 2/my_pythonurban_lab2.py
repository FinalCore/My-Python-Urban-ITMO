# -*- coding: utf-8 -*-
"""My PythonUrban_lab2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1AWj6UxaOW1aTTOyArqYkfAQsIcbpyiHp

# Итоговый проект. Улицы. Объекты культурного наследия.
"""

# TODO собрать установку всех необходимых модулей в одном месте
!pip install geopandas 
!pip install mapclassify
!pip install osmnx

# TODO собрать импорты всех модулей в одном месте
import geopandas as gpd
import osmnx as ox
import numpy as np
import pandas as pd

TILES = "CartoDB positron"  # Название подложки для карт

# TODO указать любой район Санкт-Петербург из OSM https://wiki.openstreetmap.org/wiki/RU:%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3/%D0%A0%D0%B0%D0%B9%D0%BE%D0%BD%D1%8B
TERRITORY_NAME = "Калининский район"  # название территории для которой будут строиться слои

# TODO указать ссылку на файл из вашего github репозитория, которая начинается с https://raw.githubusercontent.com/
KGIOP_FILE_URL = "https://raw.githubusercontent.com/FinalCore/My-Python-Urban-ITMO/main/geojson%20%D1%81%D0%BB%D0%BE%D0%B8/kgiop_objects.geojson"  # ссылка на слой с объектами культурного наследия
STREETS_FILE_URL = "https://raw.githubusercontent.com/FinalCore/My-Python-Urban-ITMO/main/geojson%20%D1%81%D0%BB%D0%BE%D0%B8/streets.geojson"  # ссылка на слой с улицами

"""## Территория

### Загрузка территории из OSM (Extract)
"""

# TODO загрузить geodataframe с геометрией для территории TERRITORY_NAME
territory = ox.geocode_to_gdf(TERRITORY_NAME)
territory.explore(tiles = TILES)

"""## Улицы

### Загрузка файла с улицами (Extract)
"""

# TODO отфильтровать улицы по маске геометрии территории полученной ранее
gdf = gpd.read_file(STREETS_FILE_URL, mask = territory)
gdf

gdf.head()

"""### Обработка данных с улицами (Transform)"""

# TODO сгруппировать и объединить геометрии с одинаковыми названиями
gdf["name"].is_unique # Проверка наличия неуникальных названий
gdf = gdf.dissolve(by="name", dropna = 'True')
gdf

"""### Сохранение слоя с улицами (Load)"""

# TODO переименовать столбцы в русские названия, кроме столбца geometry
# После применения метода dissolve столбец name стал индексом, поэтому geometry остался единственным столбцом
# TODO для того чтобы переименовать индекс, нужно обратиться и нему и вызвать от него метод rename (https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Index.rename.html)
print(gdf.index.name) # проверяем текущее название индекса геодатафрейма
gdf.index.rename('Название', inplace= True) # переименовываем индекс геодатафрейма в русскоязычный вариант
gdf.head()

# TODO сохранить слой в географической проекции в формате GeoJSON
gdf.to_crs(4326).to_file('Streets_from Kalininskiy_district.geojson', driver='GeoJSON')

"""## Объекты культурного наследия

### Загрузка объектов культурного наследия (Extract)
"""

# TODO отфильтровать улицы по маске геометрии территории полученной ранее
gdf = gpd.read_file(KGIOP_FILE_URL, mask = territory)
gdf.head()

"""### Обработка объектов культурного наследия (Transform)"""

# TODO добавить два столбца lon и lat, в которых будут долгота и широта 
gdf = gdf.to_crs(4326)
gdf["lon"] = gdf.geometry.x
gdf["lat"] = gdf.geometry.y
gdf.head()

"""### Сохранение слоя с объектами культурного наследия (Load)"""

# TODO переименовать столбцы в русские названия, кроме столбца geometry
rename_columns = {
    "ensemble_name": "Название ансамбля",
    "object_name": "Название объекта",
    "occurrence_time": "Время постройки",
    "object_location": "Расположение объекта",
    "historical_category": "Принадлежность к культурному наследию",
    "normative_act": "Нормативный акт",
    "object_type": "Тип объекта"
}
gdf.rename(columns=rename_columns, inplace=True)
gdf.head()

# TODO сохранить слой в географической проекции в формате GeoJSON
gdf.to_file('Historical buildings_from Kalininskiy_district.geojson', driver='GeoJSON')