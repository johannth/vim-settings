set nocompatible
set smarttab autoindent
set expandtab
set smartindent
set tabstop=4
set shiftwidth=4
set showmatch
set ruler
set incsearch
set ignorecase smartcase
syntax on
filetype plugin on
filetype indent on

"--- Better pasting by first pressing <F5> ---"
nnoremap <F5> :set invpaste paste?<Enter>
imap <F5> <C-O><F5>
set pastetoggle=<F5>

"--- Remap the F1 button ---"
inoremap <F1> <Esc>
noremap <F1> :call MapF1()<CR>

function! MapF1()
    if &buftype == "help"
        exec 'quit'
    else
        exec 'help'
    endif
endfunction

