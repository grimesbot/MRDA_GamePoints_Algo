# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 10:27:17 2024

@author: shender
"""

initial_ratings = {'AUA': 200,'CAB': 300,'CAB(B)': 40,'CBB': 400,'CBB(B)': 40,
                   'CHK': 250,'CLG': 50,'CRD': 450,'CRD(B)': 100,'CWB': 425,
                   'DEM': 80,'DGC': 1000,'DIS': 450,'FLC': 100,'MCM': 900,
                   'PHH': 250,'PHH(B)': 150,'PIT': 300,'PIT(B)': 40,'PSO': 350,
                   'RCR': 425,'SDA': 650,'SDA(B)': 120,'SLG': 1200,'SLG(B)': 180,
                   'TRD': 50,'TOM': 300,'YRD':400,
                   'BOR': 600,'CTB': 250,'DHR': 200,'KEM': 450,'MRD': 600,'MRD(B)': 100, 'PAN': 250,
                   'TIL': 500,'TNF': 600,'TNF(B)': 100,'SWS': 250, 'NDT': 150,'RDT': 200}


team_names = {
    'AUA': 'Austin Anarchy',
    'CAB': 'Casco Bay Roller Derby',
    'CAB(B)': 'Casco Bay (B)',
    'CBB': 'Chicago Bruise Brothers',
    'CBB(B)': 'Chicago (B)',
    'CHK': 'Chinook City Roller Derby',
    'CLG': 'Cleveland Guardian\'s Roller Derby',
    'CRD': 'Concussion Roller Derby',
    'CRD(B)': 'Concussion Roller Derby (B)',
    'CWB': 'Carolina Wreckingballs',
    'DEM': 'Detroit Men\'s Roller Derby',
    'DGC': 'Denver Ground Control',
    'DIS': 'Disorder',
    'FLC': 'Flour City Roller Derby',
    'MCM': 'Magic City Misfits',
    'PHH': 'Philadelphia Hooligans',
    'PHH(B)': 'Philadelphia Shenanigans (B)',
    'PIT': 'Pittsburgh Roller Derby',
    'PIT(B)': 'Pittsburgh ZomBees (B)',
    'PSO': 'Puget Sound Outcast Derby',
    'RCR': 'Race City Rebels',
    'SDA': 'San Diego Aftershocks',
    'SDA(B)': 'San Diego Tremors (B)',
    'SLG': 'St. Louis Gatekeepers',
    'SLG(B)': 'St. Louis B-Keepers (B)',
    'TRD': 'Terminus Roller Derby',
    'TOM': 'Toronto Men\'s Roller Derby',
    'YRD': 'Y\'allhalla Roller Derby',
    'BOR': 'Borderland Bandits Roller Derby',
    'CTB': 'Crash Test Brummies',
    'DHR': 'DHR Men\'s Roller Derby',
    'KEM': 'Kent Men\'s Roller Derby',
    'MRD': 'Manchester Roller Derby',
    'MRD(B)': 'Manchester (B)',
    'NDT': 'Nordicks de Touraine',
    'PAN': 'Panam Squad',
    'RDT': 'Roller Derby Toulouse',
    'TIL': 'The Inhuman League',
    'TNF': 'Tyne and Fear Roller Derby',
    'TNF(B)': 'Tyne and Fear (B)',
    'SWS': 'South Wales Silures',
}

gamecount_active = {key: 0 for key in team_names}

team_gp_dict = {key: [] for key in team_names}
