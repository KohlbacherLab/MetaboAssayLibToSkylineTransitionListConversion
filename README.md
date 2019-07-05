# MetaboAssayLibToSkylineTransitionListConversion
Conversion of OpenMS AssayGeneratorMetabo Assay Library to Skyline Transitions List

Usage: parseMetaboAssayLibToSkylineTransitionList.py [OPTIONS]

Options:
  -in, --openmslib PATH    Input assay library from
                           OpenMS::AssayGeneratorMetbo (.tsv,.traML,.pqp)
  -out, --skylinelib PATH  Output skyline transition list (.tsv)
  -rtw, --rtwindow FLOAT   Set precursor retention time window (e.g. 0.6 min);
                           default (0.0) - column will be dropped
  --help                   Show this message and exit.


For question on how to use the utility please have a look at the 
conversion\_test, which can be used as utility test and an example.  
