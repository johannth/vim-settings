"--- PYTHON ---"
au BufRead,BufNewFile *.py,*pyw set shiftwidth=4
au BufRead *.c,*.h set shiftwidth=8
au BufNewFile *.c,*.h set shiftwidth=4

au BufRead,BufNewFile *py,*pyw,*.c,*.h set tabstop=8

au BufRead,BufNewFile *.py,*.pyw set expandtab
au BufRead,BufNewFile *.c,*.h set noexpandtab
au BufRead,BufNewFile Makefile* set noexpandtab

highlight BadWhitespace ctermbg=red guibg=red
au BufRead,BufNewFile *.py,*.pyw match BadWhitespace /^\t\+/
au BufRead,BufNewFile *.py,*.pyw,*.c,*.h match BadWhitespace /\s\+$/

au BufNewFile *.py,*.pyw,*.c,*.h set fileformat=unix
let python_highlight_all=1

