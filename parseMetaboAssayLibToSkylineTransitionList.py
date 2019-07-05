"""
author: Oliver Alka
date: 05.07.2019

Convert the metabolite assay library from OpenMS::AssayGeneratorMetabo [tsv, pqp, traML] to a trasition list for skyline import [tsv].

Description:
1) rename headers
2) remove decoys
3) drop unused columns
4) set product charge to 1
5) use same adducts for product ions as for the precursor
6) recalculate rt in minutes
7) set retentiontime window in min (e.g. 0.6)
8) export

Note: 
25.04.2018
This is the complete list of column names that you can use in small molecule transition lists (Note):
MoleculeGroup, PrecursorName, ProductName, PrecursorFormula, ProductFormula,
PrecursorMz, ProductMz, PrecursorCharge, ProductCharge, PrecursorRT
PrecursorRTWindow, PrecursorCE, PrecursorDT, HighEnergyDTOffset, PrecursorIM
HighEnergyIMOffset, IMUnits, PrecursorCCS, SLens, ConeVoltage
CompensationVoltage, DeclusteringPotential, Note, LabelType, PrecursorAdduct
ProductAdduct, CAS, InChiKey, InChi, HMDB, SMILES
"""

# packages
import os
import tempfile
import click
import pandas as pd
from pyopenms import *

# function to reformat adduct string M+H+ (OpenMS) -> [M+H] (Skyline)
def reformatAdduct(adduct):
    adduct = adduct[:-1]
    adduct = '[' + adduct + ']'
    return adduct

def fillTmpTSVWithValidTargetedExp(openmslib, tmpfile):
    # check file extension, validate, convert to tsv (if necessary)
    filename, extension = os.path.splitext(openmslib)
    targeted_exp = TargetedExperiment()
    
    if extension == '.pqp':
        TransitionPQPFile().convertPQPToTargetedExperiment(openmslib.encode(), targeted_exp, False)
    elif extension == ".traML" or extension == ".TraML" or extension == ".traml":
        TraMLFile().load(openmslib.encode(), targeted_exp)
    else:
        filetype = FileTypes().nameToType('TSV')
        TransitionTSVFile().convertTSVToTargetedExperiment(openmslib.encode(), filetype, targeted_exp)

    # check validity of OpenMS::TargetedExperiment
    TransitionTSVFile().validateTargetedExperiment(targeted_exp)
    TransitionTSVFile().convertTargetedExperimentToTSV(tmpfile.name.encode(), targeted_exp)
    
    return tmpfile

@click.command()
@click.option('--openmslib', '-in', envvar = 'openmslib', multiple = False, type = click.Path(), help = 'Input assay library from OpenMS::AssayGeneratorMetbo (.tsv,.traML,.pqp)')
@click.option('--skylinelib', '-out', envvar = 'skylinelib', multiple = False, type = click.Path(), help = 'Output skyline transition list (.tsv)')
@click.option('--rtwindow', '-rtw', envvar = 'rtwindow', multiple = False, type = float, default = 0.0, help = 'Set precursor retention time window (e.g. 0.6 min); default (0.0) - column will be dropped')

def main(openmslib, skylinelib, rtwindow):

    tmpfile = tempfile.NamedTemporaryFile(suffix='.tsv')
    fillTmpTSVWithValidTargetedExp(openmslib, tmpfile)

    # read input 
    library = pd.read_csv(tmpfile.name, sep='\t')
    
    # rename headers
    library = library.rename(columns={
        'NormalizedRetentionTime': 'PrecursorRT',
        'CompoundName': 'PrecursorName',
        'SumFormula': 'PrecursorFormula',
        'Adducts': 'PrecursorAdduct',
        'Annotation': 'ProductFormula',
        'CollisionEnergy': 'PrecursorCE',
        'TransitionGroupId': 'Note'})
    
    # remove decoys, since there are problems with the import into skyline! 
    indexDecoys = library[ library['Decoy'] == 1 ].index
    
    # delete these row indexes from dataFrame
    library.drop(indexDecoys, inplace=True)
    
    # drop unused columns (from AssayGeneratorMetabo output))
    library = library.drop([
        'LibraryIntensity', 
        'PeptideSequence',
        'ModifiedPeptideSequence',
        'PeptideGroupLabel',
        'ProteinId',
        'UniprotId',
        'GeneName',
        'FragmentType',
        'FragmentSeriesNumber',
        'PrecursorIonMobility',
        'TransitionId',
        'DetectingTransition',
        'IdentifyingTransition',
        'QuantifyingTransition',
        'Decoy',
        'Peptidoforms'
        ], axis=1)
    
    # since currently only charge one features are used in OpenMS
    # the column 'ProductCharge" is set to 1 
    library['ProductCharge'] = 1
    
    # the adducts are represented differently OpenMS: M+H+ , Skyline [M+H]
    # reformat the adduct 
    library['PrecursorAdduct'] = library['PrecursorAdduct'].apply(reformatAdduct)
    
    # copy the precursor adducts into ProductAdduct column for calculation in Skyline
    library['ProductAdduct'] = library['PrecursorAdduct']
    
    # recalulate the rt in minutes
    library['PrecursorRT'] = library['PrecursorRT']/60
   
    # set window for retention time - 40 seconds - need to be a parameter
    if rtwindow != 0.0:
        library['PrecursorRTWindow'] = rtwindow
    
    # export
    library.to_csv(skylinelib, sep='\t', index=False)

    # remove temporary file 
    tmpfile.close()

    print("Export successful")


if __name__ == "__main__":
    main()
