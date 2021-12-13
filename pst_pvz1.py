#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 07:58:34 2021

@author: visk
komandinėje eilutėje galimi du vykdymo variantai

trumpa versija
srun -c 8 -n1 -N1 python3 pst_pvz1.py

ilga versija
srun --cpus-per-task 8 --ntasks 1 --nodes 1  python3 pst_pvz1.py

Pastabos. 
*) --nodes=1 parinktis šiuo atveju nebūtina. Vienas mazgas bus rezervuojamas 
pagal nutylėjimą. 

*) Jei nenurodysite -c=8 (arba --cpus-per-task=8),tai pagal nutylėjimą gausite 
tik vieną branduolį.

*) Dirbant su multiprocess daugiausiai galie imti tiek branduolių, kiek jų
turi rezervuojamas mazgas (VU MIF telkinyje 12); vienoje užduotyje negalima
sujungti kelių mazgų branduolių ir išnaudoti juos multiprocess funkcijose. 
Tam reikia naudoti mpi4py ar kokį nors kitą modulį.
"""
# Pvz. tikslas - pailiustruoti kaip teisingai ir neapsigaunant išnaudoti 
# lygiagretinimo privalumus vieno mazgo rėmuose naudojant srun parinktis.

# Užduotis: reikia apskaičiuoti vektorių 2*range(4xncores), kur ncores - faktiškai
# mazge pasiekiamas branduolių skaičius. 

# Sprendimas.

# modulių importas
import multiprocess as mp
import os

# 1) turimo branduolių skaičiaus nustatymas panaudojant mp funkciją
# -----------------------------------------------------------------------------
ncores = mp.cpu_count()

# kodas gali neveikti visai netikėtose vietose; išbandykite - lokaliai veiks,
# o telkinyje neveiks...
# print(f'branduoliu sk, kuri rodo mp modulis {ncores}')

# tokiais atvejais reiktų bandyti apseiti su paprastesne sintakse
print('branduoliu sk, kuri rodo mp modulis: ' + str(ncores))
# print(ncores)

# os. system vykdo komandinės eilutės kodą, kurį reguliariomis sąlygomis
# rinktume terminale arba shell script'e
os.system("echo branduoliu sk, kuri rodo aplinkos kintamasis: $SLURM_CPUS_ON_NODE")

# Kodėl skiriasi rezultatai? cpu_count rodo kiek iš viso branduolių turi mazgas.
# Tai nereiškia, kad toks branduolių sk. yra pasiekiamas. Pasiekiamas skaičius
# specifikuojamas komandinės eilutės parinktimi -c (arba ilga jos versija
# --cpus-per-task)

# 2) lygiagretinimas
# -----------------------------------------------------------------------------
# išsiaiškinę koks yra faktinis prieinamų branduolių sk. nuskaitoem jo reikšmę
# ir naudojame ją tolimesniuose skaičiavimuose

ncores = int(os.environ['SLURM_CPUS_ON_NODE'])

# gijų (procesų) skaičius = turimam branduolių sk.
pool = mp.Pool(processes=ncores)

# apskaičiuojame padvigubintą vektorių, kurio ilgis lygus 4x(brand. sk.)
m1 = pool.map(lambda x: 2*x,range(ncores*4))

print("Apskaiciuotas vektorius")
print(m1)
