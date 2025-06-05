# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 10:27:17 2024

@author: shender
"""

initial_ratings = {'AUA': 200,'CBRD': 300,'CBRD(B)': 40,'CBB': 400,'CBB(B)': 40,
                   'ChCRD': 250,'CGRD': 50,'CRD': 450,'CRD(B)': 100,'CWB': 425,
                   'DDD': 250,'DMRD': 80,'DGC': 1000,'DIS': 450,'FCF': 100,'MCM': 900,
                   'PHH': 250,'PHH(B)': 150,'PIT': 300,'PIT(B)': 40,'PSOD': 350,
                   'RCR': 425,'SDA': 650,'SDA(B)': 120,'SLGK': 1200,'SLGK(B)': 180,
                   'TMP': 140,'TRD': 50,'TMRD': 300, 'WURD': 50000,
                   
                   'BBRD': 600,'CTB': 250,'DHR': 200,'KMRD': 450,'MRD': 600,'MRD(B)': 100, 'NDT': 600,
                   'ORD': 300, 'PAN': 250,'RDNA': 500, 'SDRD': 500, 'SWS': 250, 'TIL': 500,'TNF': 600,
                   'TNF(B)': 100,'RDT': 800,'WRD': 264,
                   '15RRD': 50000
                   }


team_names = {
    'AUA': 'Austin Anarchy',
    'CBRD': 'Casco Bay Roller Derby',
    'CBRD(B)': 'Casco Bay (B)',
    'CBB': 'Chicago Bruise Brothers',
    'CBB(B)': 'Chicago (B)',
#hiatus    'CCH': 'Capital City Hooligans',
    'ChCRD': 'Chinook City Roller Derby',
    'CGRD': 'Cleveland Guardians Roller Derby',
#hiatus    'COL': 'Collision Roller Derby',
    'CRD': 'Concussion Roller Derby',
    'CRD(B)': 'Concussion Roller Derby (B)',
    'CWB': 'Carolina Wreckingballs',
    'DDD': 'Dallas Derby Devils',    
    'DMRD': 'Detroit Men\'s Roller Derby',
    'DGC': 'Denver Ground Control',
    'DIS': 'Disorder',
    'FCF': 'Flour City Roller Derby',
    'MCM': 'Magic City Misfits',
    'PHH': 'Philadelphia Hooligans',
    'PHH(B)': 'Philadelphia Shenanigans (B)',
    'PIT': 'Pittsburgh Roller Derby',
    'PIT(B)': 'Pittsburgh ZomBees (B)',
    'PSOD': 'Puget Sound Outcast Derby',
    'RCR': 'Race City Rebels',
    'SDA': 'San Diego Aftershocks',
    'SDA(B)': 'San Diego Tremors (B)',
    'SLGK': 'St. Louis Gatekeepers',
    'SLGK(B)': 'St. Louis B-Keepers (B)',
    'TMP': 'Tampa Roller Derby',
    'TRD': 'Terminus Roller Derby',
    'TMRD': 'Toronto Men\'s Roller Derby',
    'WURD': 'Wisconsin United Roller Derby',
    
    'BBRD': 'Borderland Bandits Roller Derby',
    'CTB': 'Crash Test Brummies',
    'DHR': 'DHR Men\'s Roller Derby',
    'KMRD': 'Kent Men\'s Roller Derby',
    'MRD': 'Manchester Roller Derby',
    'MRD(B)': 'Manchester Roller Derby (B)',
    'NDT': 'Nordicks de Touraine',
    'ORD': 'Orcet Roller Derby',
    'PAN': 'Panam Squad',
    'RDNA': 'Roller Derby Nantes Atlantique',
    'RDT': 'Roller Derby Toulouse',
    'SDRD': 'Southern Discomfort Roller Derby',
    'SWS': 'South Wales Silures',
    'TIL': 'The Inhuman League',
    'TNF': 'Tyne and Fear Roller Derby',
    'TNF(B)': 'Tyne and Fear (B)',
    'WRD': 'Wirral Roller Derby',
    
    '15RRD': '15 Ronins Roller Derby',
}

gamecount_active = {key: 0 for key in team_names}

team_gp_dict = {key: [] for key in team_names}
