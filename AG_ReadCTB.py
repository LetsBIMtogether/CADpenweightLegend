# -*- coding: utf-8 -*-
"""
AG_ReadCTB.py

Run: python AG_ReadCTB.py

Parses "target.ctb" and generates AG_PenWeightLegend.lsp

Once AG_PenWeightLegend.lsp is generated, load it into AutoCAD and enter the following command: PWL

Replace target.ctb with your own plot style file if needed.
target.ctb is orignally called AIA Standard.ctb downloaded from this link
https://www.autodesk.com/support/technical/article/caas/sfdcarticles/sfdcarticles/How-to-set-up-AIA-Layer-Standards-in-AutoCAD-LT.html

"""
import os, sys, zlib, re

CTB_FILE = "target.ctb"
LSP_FILE = "AG_PenWeightLegend.lsp"

VALID_LW = [0,5,9,13,15,18,20,25,30,35,40,50,53,60,70,80,90,100,106,120,140,158,200,211]

LSP_TEMPLATE = """\
;|------------------------------|;
;|	CAD Penweight Legend Script |;
;|	www.LetsBIMtogether.com  	|;
;|------------------------------|;

; Command: 	PWL
; Note:		Draws one line per ACI color with its assigned lineweight, thinnest to thickest

(defun c:PWL ( / colors sorted i pt1 pt2 ent lw color spacing)

{colors_block}

  ; Sort by lineweight ascending (thinnest first at top)
  (setq sorted (vl-sort colors '(lambda (a b) (< (cdr a) (cdr b)))))

  (setq spacing 5.0)   ; mm between lines - adjust to your drawing units
  (setq i 0)

  (foreach pair sorted
    (setq color (car pair))
    (setq lw    (cdr pair))

    (setq pt1 (list 0.0 (* i (- spacing)) 0.0))
    (setq pt2 (list 200.0 (* i (- spacing)) 0.0))

    ; Draw the line
    (entmake (list
      '(0 . "LINE")
      (cons 10 pt1)
      (cons 11 pt2)
      (cons 62 color)
      (cons 370 lw)
    ))

    ; Add a text label in the same color as the line
    (entmake (list
      '(0 . "TEXT")
      (cons 10 (list 205.0 (* i (- spacing)) 0.0))
      (cons 40 3.0)
	  (cons 1 (strcat "Color " (itoa color)
			"  ~~~~~ " (rtos (/ lw 2540.0) 2 3) (chr 34))) ; (chr 34) returns a string with a quote "
      (cons 62 color)       ; <-- match line color
    ))

    (setq i (1+ i))
  )

  (princ (strcat "\\nDrawn " (itoa (length sorted)) " lines. Run ZOOM E to see them."))
  (princ)
)
"""


def nearest_lw(val):
    return min(VALID_LW, key=lambda x: abs(x - val))


def main():
    folder   = os.path.dirname(os.path.abspath(__file__))
    ctb_path = os.path.join(folder, CTB_FILE)
    lsp_path = os.path.join(folder, LSP_FILE)

    if not os.path.exists(ctb_path):
        print(f"ERROR: Not found: {ctb_path}")
        sys.exit(1)

    # --- Decompress CTB ---------------------------------------------------------
    with open(ctb_path, "rb") as f:
        data = f.read()

    zlib_start = None
    for i in range(len(data) - 1):
        if data[i] == 0x78 and data[i+1] in (0x9C, 0xDA, 0x01, 0x5E):
            zlib_start = i
            break

    if zlib_start is None:
        print("ERROR: Could not find zlib stream in CTB file.")
        sys.exit(1)

    text = zlib.decompress(data[zlib_start:]).decode("latin-1")

    # --- Parse lineweight table -------------------------------------------------
    lw_table = []
    lw_match = re.search(r'custom_lineweight_table\s*\{([^}]*)\}', text, re.DOTALL)
    if lw_match:
        entries = re.findall(r'(\d+)\s*=\s*([\d.]+)', lw_match.group(1))
        lw_table = [float(v) for _, v in sorted(entries, key=lambda x: int(x[0]))]

    if not lw_table:
        print("ERROR: Could not find custom_lineweight_table.")
        sys.exit(1)

    # --- Parse plot_style sub-blocks --------------------------------------------
    ps_match = re.search(r'plot_style\s*\{(.*)\}', text, re.DOTALL)
    if not ps_match:
        print("ERROR: Could not find plot_style block.")
        sys.exit(1)

    ps_body    = ps_match.group(1)
    sub_blocks = re.findall(r'\b(\d+)\s*\{([^}]*)\}', ps_body, re.DOTALL)

    results = []
    for aci_str, block in sub_blocks:
        aci    = int(aci_str)
        name_m = re.search(r'\bname\s*=\s*"?([^\n\r"]+)', block)
        lw_m   = re.search(r'\blineweight\s*=\s*(\d+)', block)

        name    = name_m.group(1).strip() if name_m else f"Color_{aci+1}"
        lw_idx  = int(lw_m.group(1)) if lw_m else 0
        lw_mm   = lw_table[lw_idx - 1] if (lw_idx > 0 and lw_idx <= len(lw_table)) else None
        lw_code = nearest_lw(int(round(lw_mm * 100))) if lw_mm else 0

        results.append((aci + 1, name, lw_mm, lw_code))

    results.sort(key=lambda x: (x[2] if x[2] else 0, x[0]))

    # --- Build colors block -----------------------------------------------------
    lines = ["(setq colors '("]
    for aci, name, lw_mm, lw_code in results:
        lw_in = f"{lw_mm/25.4:.4f}in" if lw_mm else "n/a"
        lines.append(f"  ({aci:<3} . {lw_code:<5}) ; {name:<16} [{lw_in}]")
    lines.append("))")
    colors_block = "\n".join(lines)

    # --- Write LSP --------------------------------------------------------------
    lsp_text = LSP_TEMPLATE.format(colors_block=colors_block)

    with open(lsp_path, "w", encoding="utf-8") as f:
        f.write(lsp_text)

    print(f"Generated {lsp_path} with {len(results)} colors from {CTB_FILE}.")


if __name__ == "__main__":
    main()
