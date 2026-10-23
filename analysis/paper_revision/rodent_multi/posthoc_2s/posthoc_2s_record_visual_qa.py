"""Record manual review of POST HOC contact sheet and representative full figures."""
from pathlib import Path
import json
from datetime import datetime, timezone

out = Path(__file__).resolve().parent
metadata = json.loads((out / 'posthoc_2s_provenance.json').read_text(encoding='utf-8'))
review = {
    'status': 'PASS',
    'analysis_type': metadata['analysis_type'],
    'post_hoc': True,
    'metadata': metadata,
    'reviewed_utc': datetime.now(timezone.utc).isoformat(),
    'contact_sheet': 'posthoc_2s_QA_contact.png',
    'contact_sheet_figure_count': 15,
    'full_figures_reviewed': [
        'posthoc_2s_across_session_comparison.png',
        'posthoc_2s_EC_EC012_fP_hz_run_rest.png',
        'posthoc_2s_inclusion_comparison.png',
        'posthoc_2s_EC_session_differences.png',
    ],
    'checks': [
        'POST HOC labels visible on each scientific figure',
        'Titles, axes, session labels, legends and provenance footers readable',
        'No clipping or overlapping labels requiring correction',
        'Separate prespecified and POST HOC series identifiable',
        'Different eligible-session sets stated on pooled comparison',
    ],
    'visual_corrections_required': False,
}
(out / 'posthoc_2s_visual_QA.json').write_text(json.dumps(review, indent=2), encoding='utf-8')
print('POST HOC visual QA PASS')
