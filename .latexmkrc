# Latexmk configuration for dissertation
# Run from project root: latexmk tex/main.tex

$pdf_mode = 1;
$pdflatex = 'lualatex %O %S';
$latex = 'lualatex %O %S';
$biber = 'biber %O %B';

# Keep generated files in tex/ directory
$out_dir = 'tex';
$aux_dir = 'tex';

# Give LuaLaTeX a writable font cache inside the workspace.
$ENV{'TEXMFCACHE'} = 'tex/.texmfcache';
$ENV{'TEXMFVAR'}   = 'tex/.texmfvar';
