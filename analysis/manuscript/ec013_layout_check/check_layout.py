"""Data-driven check of the EC013 channel-to-shank layout (assumed: E1-E8 shank 1, ..., E57-E64 shank 8, E65 aux).
Sites on one shank are 20 um apart, so their LFPs correlate much more strongly than sites on different shanks."""
import numpy as np, scipy.io as sio, json, sys
from scipy.signal import butter, sosfiltfilt
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import squareform
out = sys.argv[2]
m = sio.loadmat(sys.argv[1], variable_names=['F', 'ChannelFlag'])
F = m['F'][:64]; fs = 1250.0
flag = m['ChannelFlag'].ravel()[:64]
res = {}
for name, band in [('broadband_1_300', (1, 300)), ('gamma_30_80', (30, 80)), ('theta_6_10', (6, 10))]:
    sos = butter(4, [band[0] / (fs / 2), band[1] / (fs / 2)], 'bandpass', output='sos')
    X = sosfiltfilt(sos, F[:, : int(120 * fs)], axis=1)
    C = np.corrcoef(X)
    blk = np.repeat(np.arange(8), 8)
    within = C[(blk[:, None] == blk[None, :]) & ~np.eye(64, dtype=bool)]
    between = C[blk[:, None] != blk[None, :]]
    D = 1 - np.abs(C); np.fill_diagonal(D, 0)
    lab = fcluster(linkage(squareform(D, checks=False), 'average'), 8, 'maxclust')
    # purity: fraction of channels whose cluster's majority block equals their own block
    pur = np.mean([np.bincount(blk[lab == lab[i]]).argmax() == blk[i] for i in range(64)])
    # nearest-neighbour test: for each channel, is its most-correlated other channel on the same assumed shank?
    Cn = C.copy(); np.fill_diagonal(Cn, -np.inf)
    nn_same = np.mean(blk[Cn.argmax(1)] == blk)
    res[name] = dict(mean_within=float(within.mean()), mean_between=float(between.mean()),
                     cluster_purity=float(pur), nearest_neighbour_same_shank=float(nn_same),
                     cluster_labels=lab.tolist())
    np.savetxt(f'{out}/corr_{name}.csv', C, delimiter=',', fmt='%.4f')
res['channel_flags_E1_E64'] = flag.tolist()
res['segment_s'] = 120
json.dump(res, open(f'{out}/layout_check.json', 'w'), indent=1)
for k, v in res.items():
    if isinstance(v, dict):
        print(k, {a: (round(b, 3) if isinstance(b, float) else '') for a, b in v.items() if a != 'cluster_labels'})
        print('  clusters by assumed shank:', [sorted(set(v['cluster_labels'][s*8:(s+1)*8])) for s in range(8)])
