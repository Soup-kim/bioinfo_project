#base 수 세기
def count_bases(matches):
    base_counts = {'A': 0, 'C': 0, 'G': 0, 'T': 0}
    
    # matches가 비어있는 경우 처리
    if matches.empty:
        return pd.Series(base_counts)
    
    for match in matches:
        for base in match:
            base_counts[base] += 1
    return pd.Series(base_counts)

base_counts = pileup.groupby('pos')['matches'].apply(count_bases).unstack().fillna(0)
base_counts.head(10)

#ACGT 이외의 알파벳이 나와서 제거
def filter_bases(matches):
    return ''.join(base for base in matches if base in 'ACGT')

pileup['matches'] = pileup['matches'].apply(filter_bases)


# Shannon entropy
import numpy as np

def shannon_entropy(base_counts):
    total_counts = base_counts.sum()
    probs = base_counts / total_counts
    return -np.sum(probs * np.log2(probs))

# 각 position별 Shannon entropy
entropies = base_counts.apply(shannon_entropy, axis=1)
entropies.head(30)

#bedgraph
bedgraph = pd.DataFrame({
    'chrom': 'chr9',
    'start': pileup['pos'] - 1,
    'end': pileup['pos'],
    'entropy': entropies
})

#file 
bedgraph.to_csv('7g_entropy.bedgraph', sep='\t', index=False, header=False)