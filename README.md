# CAD Penweight Legend Script
<img src="GitHub%20Images/PenweightLegendSnip.png" width="600"/>

A Python script that reads an AutoCAD plot style file (`.ctb`) and generates an AutoLISP routine that draws a visual penweight legend directly in your drawing, one line per ACI color, ordered thinnest to thickest, with color and lineweight labels.

🎥 [Watch a YouTube demo](https://www.youtube.com/watch?v=n-d_RphQaOo)

## How It Works

```
target.ctb  →  AG_ReadCTB.py  →  AG_PenWeightLegend.lsp  →  AutoCAD command: PWL
```

- The Python script parses your `.ctb` file and extracts each ACI color's assigned lineweight.
- It writes an AutoLISP file (`AG_PenWeightLegend.lsp`) with those values baked in.
- You load the LSP in AutoCAD and run command `PWL` to place the legend in the drawing.

## Requirements

- **AutoCAD** (AutoCAD LT, AutoCAD Architecture, etc.)
- **Python 3** no third-party packages needed, only the standard library.
  - Download from [python.org/downloads](https://www.python.org/downloads/)
  - During installation, check **"Add Python to PATH"** so you can run it from any folder.

## Usage

- **Download or clone this repository**

  Keep all files in the same folder.

- **Add your own `target.ctb` plot style file**

  A `.ctb` file is required but not included in this repo. You can use your own (typically found in `C:\Users\<you>\AppData\Roaming\Autodesk\AutoCAD <version>\<year>\<locale>\Plotters\Plot Styles\`) or download the **AIA Standard.ctb** from the [Autodesk support page](https://www.autodesk.com/support/technical/article/caas/sfdcarticles/sfdcarticles/How-to-set-up-AIA-Layer-Standards-in-AutoCAD-LT.html). Place the file in the CADpenweightLegend folder and rename it to `target.ctb`.

- **Run the Python script**

  Open a terminal (Command Prompt or PowerShell), navigate to the folder where you placed CADpenweightLegend folder, and run:

  ```
  cd "C:\path\to\folder"
  python AG_ReadCTB.py
  ```

  This generates `AG_PenWeightLegend.lsp` in the same folder.

- **Load the AutoLISP in AutoCAD**

  In AutoCAD, type `APPLOAD` in the command line, browse to `AG_PenWeightLegend.lsp`, and click **Load**.

  > Alternatively, drag and drop the `.lsp` file directly into the AutoCAD drawing window.

- **Run the command**

  In the AutoCAD command line, type:

  ```
  PWL
  ```

  The legend is drawn at the origin. Run `ZOOM E` to fit it in view.

  Each row shows a line drawn at its plotted lineweight (or color...), with a label displaying the ACI color number and lineweight in inches.

## License

Licensed under the [MIT License](LICENSE).
<br/>
<br/>

---

## Go to [www.LetsBIMtogether.com](https://letsbimtogether.com/ "www.LetsBIMtogether.com") for:

- AutoLisp routines for AutoCAD software

- Revit/CAD Tips & Tricks YouTube channel

- Plugins & scripts for Revit software

- Autodesk Appstore page

- LinkedIn

- GitHub

- Blog
