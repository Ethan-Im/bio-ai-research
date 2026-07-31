import sys
from rdkit import Chem
from rdkit.Chem import AllChem
from meeko import MoleculePreparation
from meeko import PDBQTWriterLegacy

def prepare_covalent_ligand_v2(smiles, output_pdbqt):
    print("1. Parsing SMILES and adding hydrogens...")
    mol = Chem.MolFromSmiles(smiles)
    mol = Chem.AddHs(mol)
    
    print("2. Generating 3D conformation (ETKDGv3)...")
    params = AllChem.ETKDGv3()
    params.randomSeed = 42
    AllChem.EmbedMolecule(mol, params)
    
    print("3. Optimizing geometry (MMFF)...")
    AllChem.MMFFOptimizeMolecule(mol, maxIters=200)
    
    print("4. Detecting Acrylamide warhead motif (C=CC(=O)N)...")
    warhead_pattern = Chem.MolFromSmarts("C=CC(=O)N")
    matches = mol.GetSubstructMatches(warhead_pattern)
    
    if not matches:
        print("⚠️ Warning: Acrylamide warhead motif not detected.")
        covalent_atom_index = None
    else:
        # Index of the beta-carbon in acrylamide for covalent bond formation
        covalent_atom_index = matches[0][0]
        print(f"✅ Found warhead motif! Reactive beta-carbon index: {covalent_atom_index}")
        
    print("5. Converting to PDBQT format using updated Meeko Writer API...")
    preparator = MoleculePreparation()
    
    # Configure covalent bond reactive atom for newer Meeko API
    if covalent_atom_index is not None:
        if hasattr(preparator, 'set_covalent_reactive_atom'):
            preparator.set_covalent_reactive_atom(covalent_atom_index)
        elif hasattr(preparator, 'set_covalent'):
            preparator.set_covalent(covalent_atom_index)
        else:
            print("⚠️ Covalent method fallback: passing reactive atom via setup.")
        
    mol_setup_list = preparator.prepare(mol)
    
    # Use PDBQTWriterLegacy to write PDBQT string cleanly
    writer = PDBQTWriterLegacy()
    pdbqt_string, _, _ = writer.write_string(mol_setup_list[0])
    
    with open(output_pdbqt, "w") as f:
        f.write(pdbqt_string)
        
    print(f"🎉 Cleanly generated covalent ligand PDBQT: {output_pdbqt}")

if __name__ == "__main__":
    sample_smiles = "C=CC(=O)NC1=CC=C(NC2=NC=CC(=N2)C3=CN(C)C4=CC=CC=C34)C=C1"
    prepare_covalent_ligand_v2(sample_smiles, "t790m_covalent_candidate.pdbqt")
