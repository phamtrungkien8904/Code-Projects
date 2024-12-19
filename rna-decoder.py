## RNA decoder ##
# This program decodes a RNA sequence into a protein sequence.

dict_amino = {
    'UUU': 'F', 'UCU': 'S', 'UAU': 'Y', 'UGU': 'C',
    'UUC': 'F', 'UCC': 'S', 'UAC': 'Y', 'UGC': 'C',
    'UUA': 'L', 'UCA': 'S', 'UAA': '*', 'UGA': '*',
    'UUG': 'L', 'UCG': 'S', 'UAG': '*', 'UGG': 'W',
    'CUU': 'L', 'CCU': 'P', 'CAU': 'H', 'CGU': 'R',
    'CUC': 'L', 'CCC': 'P', 'CAC': 'H', 'CGC': 'R',
    'CUA': 'L', 'CCA': 'P', 'CAA': 'Q', 'CGA': 'R',
    'CUG': 'L', 'CCG': 'P', 'CAG': 'Q', 'CGG': 'R',
    'AUU': 'I', 'ACU': 'T', 'AAU': 'N', 'AGU': 'S',
    'AUC': 'I', 'ACC': 'T', 'AAC': 'N', 'AGC': 'S',
    'AUA': 'I', 'ACA': 'T', 'AAA': 'K', 'AGA': 'R',
    'AUG': 'M', 'ACG': 'T', 'AAG': 'K', 'AGG': 'R',
    'GUU': 'V', 'GCU': 'A', 'GAU': 'D', 'GGU': 'G',
    'GUC': 'V', 'GCC': 'A', 'GAC': 'D', 'GGC': 'G',
    'GUA': 'V', 'GCA': 'A', 'GAA': 'E', 'GGA': 'G',
    'GUG': 'V', 'GCG': 'A', 'GAG': 'E', 'GGG': 'G'
} # Dictionary of codons and their corresponding amino acids, '*' represents stop codon


def decode(rna):
    protein = ''
    applied_rna = ''
    start_codon_found = False
    if len(rna) % 3 != 0:
        print("Invalid RNA sequence!")
        protein, applied_rna = None, None
        return protein, applied_rna
    for i in range(0, len(rna), 3):
        codon = rna[i:i+3]
        if not start_codon_found:
            if codon == 'AUG': # Start codon AUG
                start_codon_found = True
                applied_rna += codon
                protein += dict_amino[codon]
            continue
        if dict_amino[codon] == '*':
            applied_rna += codon
            break
        protein += dict_amino[codon]
        applied_rna += codon
    return protein, applied_rna

# Test the functions
rna = 'GUGGCGAUGGCCAUGGCGCCCAGAACUGAGAUCAAUAGUACCCGUAUUAACGGGUGAUGCUGU'
protein, applied_rna = decode(rna)
print(f"Protein: {protein}")
print(f"Applied RNA: {applied_rna}")