import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from scripts.kb.se_monitor.hierarchy import build_hierarchy

def main():
    pj_kuda_groups, sls_info, has_alokasi = build_hierarchy()
    
    # Let's find all PMLs and PPLs where nmkec is MEMPAWAH HILIR
    mh_pmls = set()
    mh_ppls = set()
    mh_pml_ppl = {} # pml -> list of ppl
    mh_pml_pj = {} # pml -> pj
    
    for idsls, info in sls_info.items():
        if info.get("kecamatan", "").strip().upper() == "MEMPAWAH HILIR":
            pml = info["pml"]
            ppl = info["ppl"]
            pj = info["pj"]
            
            mh_pmls.add(pml)
            mh_ppls.add(ppl)
            mh_pml_pj[pml] = pj
            mh_pml_ppl.setdefault(pml, set()).add(ppl)
            
    print(f"PMLs in MEMPAWAH HILIR ({len(mh_pmls)}):")
    for pml in sorted(mh_pmls):
        ppl_list = sorted(list(mh_pml_ppl[pml]))
        print(f"- PML: {pml} (PJ-Kuda: {mh_pml_pj[pml]})")
        print(f"  PPLs: {', '.join(ppl_list)}")

if __name__ == "__main__":
    main()
