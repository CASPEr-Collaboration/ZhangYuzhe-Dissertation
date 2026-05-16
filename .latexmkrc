# Latexmk configuration for dissertation
# Run from project root: latexmk tex/main.tex

$pdf_mode = 1;
$pdflatex = 'pdflatex %O %S';
$biber = 'biber %O %B';

# Keep generated files in tex/ directory
$out_dir = 'tex';
$aux_dir = 'tex';
