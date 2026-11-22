"""Run project stages in order from any working directory: python run_all.py"""
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parent
for file in ['01_validate_inputs.py','02_build_legacy_panel.py','03_gravity_models.py','04_robustness.py','05_huff_choice.py','06_figures.py','07_geography_audit.py']:
    print('\n'+'='*65+'\nRUNNING '+file,flush=True)
    subprocess.run([sys.executable,str(root/'scripts'/file)],cwd=root,check=True)
print('\nDONE. Review outputs/ and docs/FINAL_RESEARCH_REPORT.md. Results remain provisional.')
