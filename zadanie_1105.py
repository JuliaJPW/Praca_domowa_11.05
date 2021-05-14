import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import shapely

gdf = gpd.read_file('PD_STAT_GRID_CELL_2011.shp')
plik = gdf.to_crs("EPSG:4326")

gdw = gpd.read_file('Województwa.shp')
gdw = gdw.to_crs("EPSG:4326")


def mapa(gdf, kolumna, wykres):
    
    gdf.plot(kolumna, legend=True)
    plt.title(wykres)
#podpunkt 3: wyznaczenie cendroid dla poligonów
    gdf['centroid']=gdf.centroid
#podpunkt 4: wyznaczenie regularnej siatki fishnet
    xmin, ymin, xmax, ymax = [13, 48, 25, 56]
    n_cells = 30
    cell_size = (xmax-xmin)/n_cells

    grid_cells = []
    for x0 in np.arange(xmin, xmax+cell_size, cell_size):
        for y0 in np.arange(ymin, ymax+cell_size, cell_size):
            x1 = x0 - cell_size
            y1 = y0 + cell_size
            grid_cells.append(shapely.geometry.box(x0, y0, x1, y1))

    cell = gpd.GeoDataFrame(grid_cells, columns=['geometry'])
    ax = gdf.plot(markersize = 0.1, figsize=(12,8), column = kolumna, cmap="jet")

    plt.autoscale(False)
    cell.plot(ax = ax, facecolor = "none", edgecolor = 'grey')
    ax.axis("off")
    plt.title(wykres)

#podpunkt 6: spatial join    
    merged = gpd.sjoin(gdf, cell, how ='left', op = 'within')
#podpunkt 7: agregacja
    dissolve = merged.dissolve(by = "index_right", aggfunc = "sum")

#podpunkt 8: przypisanie wartoci do oczek siatki   
    if kolumna == 'TOT':
        cell.loc[dissolve.index, kolumna] = dissolve.TOT.values
        maksimum = max(gdf.TOT)
        minimum = min(gdf.TOT)
        
    elif kolumna == 'TOT_0_14':
        cell.loc[dissolve.index, kolumna]=dissolve.TOT_0_14.values
        maksimum = max(gdf.TOT_0_14)
        minimum = min(gdf.TOT_0_14)
                
    elif kolumna == 'TOT_15_64':
        cell.loc[dissolve.index, kolumna]=dissolve.TOT_15_64.values
        maksimum = max(gdf.TOT_15_64)
        minimum = min(gdf.TOT_15_64)
                
    elif kolumna == 'TOT_65__':
        cell.loc[dissolve.index, kolumna]=dissolve.TOT_65__.values
        maksimum = max(gdf.TOT_65__)
        minimum = min(gdf.TOT_65__)
                
    elif kolumna == 'TOT_MALE':
        cell.loc[dissolve.index, kolumna]=dissolve.TOT_MALE.values
        maksimum = max(gdf.TOT_MALE)
        minimum = min(gdf.TOT_MALE)
                
    elif kolumna == 'TOT_FEM':
        cell.loc[dissolve.index, kolumna]=dissolve.TOT_FEMALE.values
        maksimum = max(gdf.TOT_FEMALE)
        minimum = min(gdf.TOT_FEMALE)
                
    elif kolumna == 'MALE_0_14':
        cell.loc[dissolve.index, kolumna]=dissolve.MALE_0_14.values
        maksimum = max(gdf.MALE_0_14)
        minimum = min(gdf.MALE_0_14)
                
    elif kolumna == 'MALE_15_64':
        cell.loc[dissolve.index, kolumna]=dissolve.MALE_15_64.values
        maksimum = max(gdf.MALE_15_64)
        minimum = min(gdf.MALE_15_64)
                
    elif kolumna == 'MALE_65__':
        cell.loc[dissolve.index, kolumna]=dissolve.MALE_65__.values
        maksimum = max(gdf.MALE_65__)
        minimum = min(gdf.MALE_65__)
                
    elif kolumna == 'FEM_0_14':
        cell.loc[dissolve.index, kolumna]=dissolve.FEM_0_14.values
        maksimum = max(gdf.FEM_0_14)
        minimum = min(gdf.FEM_0_14)
        
    elif kolumna == 'FEM_15_64':
        cell.loc[dissolve.index, kolumna]=dissolve.FEM_15_64.values
        maksimum = max(gdf.FEM_15_64)
        minimum = min(gdf.FEM_15_65)
        
    elif kolumna == 'FEM_65__':
        cell.loc[dissolve.index, kolumna]=dissolve.FEM_65__.values
        maksimum = max(gdf.FEM_65__)
        minimum = min(gdf.FEM_65__)
        
    elif kolumna == 'FEM_RATIO':
        cell.loc[dissolve.index, kolumna]=dissolve.FEMFEM_RATIO.values
        maksimum = max(gdf.FEM_RATIO)
        minimum = min(gdf.FEM_RATIO)
        
    else:
        print('Stop')

#podpunkt 9: wizualizacja        
    ax = cell.plot(column=kolumna, figsize=(10, 8), cmap='viridis', vmax = maksimum, vmin = minimum, edgecolor="grey", legend = True)
    plt.autoscale(False)
    ax.set_axis_off()
    plt.axis('equal')
    plt.title(wykres)
    return()

#praca domowa
#Wyznacz liczbę ludności w siatce dla:

#a) Przedziału wiekowego 0-14
#mapa(plik, 'TOT_0_14', 'wiek_0-14')

#b) Przedziału wiekowego 15-64
#mapa(plik, 'TOT_15_64', 'wiek_15-65')

#c) Przedziału wiekowego >65
#(plik, 'TOT_65__', 'wiek_>65')

#d) Ludności męskiej w przedziałach wiekowych z podpunktów a-c
#mapa(plik, 'MALE_0_14', 'mężczyźni_0-14')
#mapa(plik, 'MALE_15_64', 'mężczyźni_15-65')
#mapa(plik, 'MALE_65__', 'mężczyźnie_>65')

#e) Ludności żeńskiej w przedziałach wiekowych z podpunktów a-c
#mapa(plik, 'FEM_0_14', 'kobiety_0-14')
#mapa(plik, 'FEM_15_64', 'kobiety_15-65')
#mapa(plik, 'FEM_65__', 'kobiety_>65')

#f) Ratio liczby ludności do powierzchni dla danego województwa
#mapa(plik, 'FEM_RATIO', 'ratio w wojewodztwach')

#f) Ratio liczby ludności do powierzchni dla danego województwa
gdf = gpd.read_file('PD_STAT_GRID_CELL_2011.shp')
gdf = gdf.to_crs("EPSG:4326")
gdf.plot("TOT",legend = True)
gdf['centroid'] = gdf.centroid
gdw = gpd.read_file('Województwa.shp')
gdw = gdw.to_crs("EPSG:4326")
gdw.plot(legend=True)
cell = gpd.GeoDataFrame(gdw, columns=['geometry'])
ax = gdf.plot(markersize = .1, figsize=(12, 8), column='FEM_RATIO', cmap='jet')

#podpunkt 6: spatial join    
merged = gpd.sjoin(gdf, cell, how='left', op = 'within')
#podpunkt 7: agregacja
dissolve = merged.dissolve(by="index_right", aggfunc = "sum")
kolumna = 'FEM_RATIO'       
plt.autoscale(False)
cell.plot(ax = ax, facecolor = "none", edgecolor = 'grey')
ax.axis("on")
plt.title('wojewodztwa')
cell.loc[dissolve.index, kolumna]=dissolve.FEM_RATIO.values
maksimum = max(gdf.FEM_RATIO)
minimum = min(gdf.FEM_RATIO)

ax = cell.plot(column=kolumna, figsize=(10, 8), cmap='viridis', vmax = maksimum, vmin = minimum, edgecolor="grey", legend = True)
plt.autoscale(False)
ax.set_axis_off()
plt.axis('equal')
plt.title('podpunkt f')

print('koniec')

























