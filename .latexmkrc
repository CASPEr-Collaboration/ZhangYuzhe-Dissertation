# Latexmk configuration for dissertation
# Run from project root: latexmk tex/main.tex

$pdf_mode = 1;
$lualatex = 'lualatex -interaction=nonstopmode -halt-on-error %O %S';
$pdflatex = $lualatex;
$latex = $lualatex;
$biber = 'biber %O %B';

# Keep generated files in tex/ directory
$out_dir = 'tex';
$aux_dir = 'tex';

# Give LuaLaTeX a writable font cache inside the workspace.
$ENV{'TEXMFCACHE'} = 'tex/.texmfcache';
$ENV{'TEXMFVAR'}   = 'tex/.texmfvar';
