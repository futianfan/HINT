from rdkit.Chem import Draw
from rdkit.Chem import AllChem, MolToSmiles

# smiles = 'CCOC(=O)[C@H](CCC1=CC=CC=C1)N[C@@H](C)C(=O)N1CCC[C@H]1C(O)=O'
# mol = AllChem.MolFromSmiles(smiles)
# Draw.MolToFile(mol, 'figure/enalapril.png') 



smiles = 'FC(F)(F)C1=CC(=N)NC=C1C1=CC(=NC(=N1)N1CCOCC1)N1CCOCC1'
mol = AllChem.MolFromSmiles(smiles)
Draw.MolToFile(mol, 'figure/placebo.png') 

