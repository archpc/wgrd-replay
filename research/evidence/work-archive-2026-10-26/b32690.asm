            0x00b32690      push  ebp
            0x00b32691      mov   ebp, esp
            0x00b32693      push  0xffffffff                           ; 255
            0x00b32695      push  0x18698f6
            0x00b3269a      mov   eax, dword fs:[0x0]
            0x00b326a0      push  eax
            0x00b326a1      sub   esp, 0x520
            0x00b326a7      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00b326ac      xor   eax, ebp
            0x00b326ae      mov   dword [ebp-0x10], eax
            0x00b326b1      push  esi
            0x00b326b2      push  edi
            0x00b326b3      push  eax
            0x00b326b4      lea   eax, dword [ebp-0x0c]
            0x00b326b7      mov   dword fs:[0x0], eax
            0x00b326bd      mov   ecx, dword [ebp+0x18]
            0x00b326c0      mov   eax, dword [ebp+0x14]
            0x00b326c3      mov   edi, dword [ebp+0x08]
            0x00b326c6      mov   esi, dword [ebp+0x10]
            0x00b326c9      mov   dword [ebp-0x410], eax
            0x00b326cf      mov   eax, dword [ebp+0x20]
            0x00b326d2      mov   dword [ebp-0x478], eax
            0x00b326d8      mov   eax, dword [ebp+0x28]
            0x00b326db      mov   dword [ebp-0x3dc], eax
            0x00b326e1      mov   al, byte [ecx+0x04]
            0x00b326e4      mov   dword [ebp-0x424], ecx
            0x00b326ea      push  ecx
            0x00b326eb      lea   ecx, dword [ebp-0x4fc]
            0x00b326f1      mov   dword [ebp-0x3d0], edi
            0x00b326f7      mov   dword [ebp-0x474], esi
            0x00b326fd      mov   byte [ebp-0x3e0], al
            0x00b32703      call  0xabb0d0
            0x00b32708      movss xmm0, dword [esi]
            0x00b3270c      xor   ecx, ecx
            0x00b3270e      movss dword [ebp-0x1c], xmm0
            0x00b32713      movss xmm0, dword [esi+0x04]
            0x00b32718      movss dword [ebp-0x18], xmm0
            0x00b3271d      movss xmm0, dword [esi+0x08]
            0x00b32722      mov   byte [ebp-0x4f8], 0x00
            0x00b32729      movss dword [ebp-0x14], xmm0
            0x00b3272e      mov   dword [ebp-0x34], 0x7f800000
            0x00b32735      mov   dword [ebp-0x30], 0x7f800000
            0x00b3273c      mov   dword [ebp-0x2c], 0x7f800000
        ┌─> 0x00b32743      movss xmm0, dword [ebp+ecx*1-0x1c]
        ╎   0x00b32749      ucomiss xmm0, dword [ebp+ecx*1-0x34]
        ╎   0x00b3274e      lahf
        ╎   0x00b3274f      test  ah, 0x44                             ; 68
       ┌──< 0x00b32752      jp    0xb3275e
       │╎   0x00b32754      add   ecx, 0x04
       │╎   0x00b32757      cmp   ecx, 0x0c                            ; 0xc ; 12
       │└─< 0x00b3275a      jb    0xb32743
       │┌─< 0x00b3275c      jmp   0xb3276a
       └──> 0x00b3275e      lea   eax, dword [ebp-0x1c]
        │   0x00b32761      push  eax
        │   0x00b32762      call  0xbb19b0
        │   0x00b32767      add   esp, 0x04
        └─> 0x00b3276a      mov   dword [ebp-0x438], 0x00
            0x00b32774      mov   dword [ebp-0x430], 0x00
            0x00b3277e      mov   dword [ebp-0x42c], 0x00
            0x00b32788      push  dword [edi+0x04]
            0x00b3278b      lea   ecx, dword [ebp-0x43c]
            0x00b32791      mov   dword [ebp-0x04], 0x00
            0x00b32798      call  0x9d7140
            0x00b3279d      mov   eax, dword [0x201f660]               ; [0x201f660:4]=0
            0x00b327a2      mov   eax, dword [eax+0x1f8]
            0x00b327a8      mov   dword [ebp-0x3c0], 0x00
            0x00b327b2      mov   dword [ebp-0x3bc], 0x00
            0x00b327bc      mov   dword [ebp-0x3b8], 0x00
            0x00b327c6      mov   ecx, dword [eax*4+0x2027ed0]
            0x00b327cd      mov   dword [ebp-0x3b4], 0x00
            0x00b327d7      mov   dword [ebp-0x3c4], ecx
            0x00b327dd      test  ecx, ecx
        ┌─< 0x00b327df      jz    0xb327f4
        │   0x00b327e1      mov   eax, dword [ecx]
        │   0x00b327e3      lea   edx, dword [ebp-0x3b8]
        │   0x00b327e9      push  edx
        │   0x00b327ea      lea   edx, dword [ebp-0x3c0]
        │   0x00b327f0      push  edx
        │   0x00b327f1      call  dword [eax+0x3c]                     ; 60
        └─> 0x00b327f4      mov   eax, dword [ebp-0x42c]
            0x00b327fa      xor   esi, esi
            0x00b327fc      mov   byte [ebp-0x04], 0x01
            0x00b32800      mov   dword [ebp-0x39c], eax
            0x00b32806      cmp   dword [edi+0x04], esi
        ┌─< 0x00b32809      jbe   0xb3289e
        │   0x00b3280f      nop
       ┌──> 0x00b32810      mov   eax, dword [edi]
       ╎│   0x00b32812      lea   edi, dword [eax+esi*4]
       ╎│   0x00b32815      mov   ecx, edi
       ╎│   0x00b32817      call  0xb01530
       ╎│   0x00b3281c      cmp   dword [ebp-0x3c4], 0x00
      ┌───< 0x00b32823      jz    0xb3288e
      │╎│   0x00b32825      movzx ecx, word [edi]
      │╎│   0x00b32828      cmp   ecx, dword [ebp-0x3bc]
     ┌────< 0x00b3282e      jnb   0xb3288e
     ││╎│   0x00b32830      mov   eax, dword [ebp-0x3c0]
     ││╎│   0x00b32836      cmp   dword [eax+ecx*4], 0x00
    ┌─────< 0x00b3283a      jnz   0xb32850
    │││╎│   0x00b3283c      cmp   ecx, dword [ebp-0x3b4]
   ┌──────< 0x00b32842      jnb   0xb3288e
   ││││╎│   0x00b32844      mov   eax, dword [ebp-0x3b8]
   ││││╎│   0x00b3284a      cmp   dword [eax+ecx*4], 0x00
  ┌───────< 0x00b3284e      jz    0xb3288e
  ││└─────> 0x00b32850      mov   ecx, dword [ebp-0x39c]
  ││ ││╎│   0x00b32856      cmp   ecx, dword [ebp-0x438]
  ││┌─────< 0x00b3285c      jnz   0xb3286f
  │││││╎│   0x00b3285e      lea   ecx, dword [ebp-0x43c]
  │││││╎│   0x00b32864      call  0x7aab00
  │││││╎│   0x00b32869      mov   ecx, dword [ebp-0x39c]
  ││└─────> 0x00b3286f      mov   edx, dword [ebp-0x430]
  ││ ││╎│   0x00b32875      mov   dword [edx+ecx*4], 0xffffffff        ; [0xffffffff:4]=-1 ; -1
  ││ ││╎│   0x00b3287c      mov   eax, dword [edi]
  ││ ││╎│   0x00b3287e      mov   dword [edx+ecx*4], eax
  ││ ││╎│   0x00b32881      inc   ecx
  ││ ││╎│   0x00b32882      mov   dword [ebp-0x39c], ecx
  ││ ││╎│   0x00b32888      mov   dword [ebp-0x42c], ecx
  └└─└└───> 0x00b3288e      mov   edi, dword [ebp-0x3d0]
       ╎│   0x00b32894      inc   esi
       ╎│   0x00b32895      cmp   esi, dword [edi+0x04]
       └──< 0x00b32898      jb    0xb32810
        └─> 0x00b3289e      mov   eax, dword [ebp+0x0c]
            0x00b328a1      mov   byte [ebp-0x04], 0x00
            0x00b328a5      mov   eax, dword [eax+0x04]
            0x00b328a8      mov   dword [ebp-0x3d0], eax
            0x00b328ae      lea   esi, dword [eax*4]
            0x00b328b5      lea   eax, dword [esi+0x0f]
            0x00b328b8      cmp   eax, 0x4020                          ; ' @'
        ┌─< 0x00b328bd      jnbe  0xb328c8
        │   0x00b328bf      call  0x18076c0
        │   0x00b328c4      mov   eax, esp
       ┌──< 0x00b328c6      jmp   0xb328ca
       │└─> 0x00b328c8      xor   eax, eax
       └──> 0x00b328ca      add   eax, 0x0f                            ; 0xf ; 15
            0x00b328cd      lea   ecx, dword [ebp-0x3f4]
            0x00b328d3      and   eax, 0xfffffff0                      ; 4294967280
            0x00b328d6      push  esi
            0x00b328d7      push  eax
            0x00b328d8      mov   dword [ebp-0x3ec], eax
            0x00b328de      call  0x4ea610
            0x00b328e3      mov   eax, dword [ebp-0x3d0]
            0x00b328e9      xor   edi, edi
            0x00b328eb      mov   dword [ebp-0x3e8], edi
            0x00b328f1      mov   dword [ebp-0x3e4], eax
            0x00b328f7      mov   ecx, dword [ebp+0x0c]
            0x00b328fa      mov   eax, dword [ecx]
            0x00b328fc      mov   ecx, dword [ecx+0x04]
            0x00b328ff      lea   ecx, dword [eax+ecx*4]
            0x00b32902      cmp   eax, ecx
        ┌─< 0x00b32904      jz    0xb32936
        │   0x00b32906      nop   word [eax+eax*1], ax
       ┌──> 0x00b32910      mov   esi, dword [ebp-0x3ec]
       ╎│   0x00b32916      mov   dword [esi+edi*4], 0xffffffff        ; [0xffffffff:4]=-1 ; -1
       ╎│   0x00b3291d      mov   edx, dword [eax]
       ╎│   0x00b3291f      add   eax, 0x04
       ╎│   0x00b32922      mov   dword [esi+edi*4], edx
       ╎│   0x00b32925      mov   edi, dword [ebp-0x3e8]
       ╎│   0x00b3292b      inc   edi
       ╎│   0x00b3292c      mov   dword [ebp-0x3e8], edi
       ╎│   0x00b32932      cmp   eax, ecx
       └──< 0x00b32934      jnz   0xb32910
        └─> 0x00b32936      mov   dword [ebp-0x528], 0x00
            0x00b32940      mov   dword [ebp-0x520], 0x00
            0x00b3294a      mov   dword [ebp-0x51c], 0x00
            0x00b32954      push  0xb2b380
            0x00b32959      push  0x6f38e0
            0x00b3295e      push  0x27                                 ; ''' ; 39
            0x00b32960      push  0x14                                 ; 20
            0x00b32962      lea   eax, dword [ebp-0x358]
            0x00b32968      mov   byte [ebp-0x04], 0x05
            0x00b3296c      push  eax
            0x00b3296d      call  0x1806ffe
            0x00b32972      mov   eax, dword [ebp-0x3ec]
            0x00b32978      sub   esp, 0x08
            0x00b3297b      mov   ecx, dword [ebp-0x430]
            0x00b32981      mov   edx, dword [ebp-0x410]
            0x00b32987      mov   edi, dword [ebp-0x39c]
            0x00b3298d      mov   dword [ebp-0x480], eax
            0x00b32993      mov   eax, dword [ebp-0x3e8]
            0x00b32999      mov   dword [ebp-0x47c], eax
            0x00b3299f      mov   eax, dword [edx]
            0x00b329a1      mov   dword [ebp-0x488], ecx
            0x00b329a7      mov   ecx, esp
            0x00b329a9      push  dword [ebp+0x1c]
            0x00b329ac      mov   dword [ebp-0x484], edi
            0x00b329b2      push  0x00
            0x00b329b4      mov   dword [ecx], eax
            0x00b329b6      mov   eax, dword [edx+0x04]
            0x00b329b9      mov   dword [ecx+0x04], eax
            0x00b329bc      lea   eax, dword [ebp-0x4fc]
            0x00b329c2      push  eax
            0x00b329c3      lea   eax, dword [ebp-0x1c]
            0x00b329c6      mov   byte [ebp-0x04], 0x06
            0x00b329ca      push  eax
            0x00b329cb      lea   eax, dword [ebp-0x480]
            0x00b329d1      push  eax
            0x00b329d2      lea   eax, dword [ebp-0x488]
            0x00b329d8      push  eax
            0x00b329d9      lea   eax, dword [ebp-0x52c]
            0x00b329df      push  eax
            0x00b329e0      lea   eax, dword [ebp-0x358]
            0x00b329e6      push  eax
            0x00b329e7      call  0xc972a0
            0x00b329ec      add   esp, 0x28
            0x00b329ef      xor   ecx, ecx
            0x00b329f1      mov   dword [ebp-0x3cc], ecx
            0x00b329f7      nop   word [eax+eax*1], ax
        ┌─> 0x00b32a00      mov   dword [ebp-0x380], ecx
        ╎   0x00b32a06      cmp   ecx, 0x0b                            ; 0xb ; 11
       ┌──< 0x00b32a09      jz    0xb341ad
       │╎   0x00b32a0f      lea   eax, dword [ecx+ecx*4]
       │╎   0x00b32a12      lea   esi, dword [ebp-0x358]
       │╎   0x00b32a18      cmp   dword [esi+eax*4+0x10], 0x00
       │╎   0x00b32a1d      lea   esi, dword [esi+eax*4]
       │╎   0x00b32a20      mov   dword [ebp-0x35c], esi
      ┌───< 0x00b32a26      jz    0xb341ad
      ││╎   0x00b32a2c      cmp   ecx, 0x06                            ; 6
     ┌────< 0x00b32a2f      jz    0xb32aba
     │││╎   0x00b32a35      cmp   ecx, 0x25                            ; '%' ; 37
    ┌─────< 0x00b32a38      jz    0xb32aba
    ││││╎   0x00b32a3e      cmp   ecx, 0x13                            ; 19
   ┌──────< 0x00b32a41      jz    0xb32aba
   │││││╎   0x00b32a43      cmp   ecx, 0x04                            ; 4
  ┌───────< 0x00b32a46      jz    0xb32aba
  ││││││╎   0x00b32a48      cmp   ecx, 0x21                            ; '!' ; 33
  ────────< 0x00b32a4b      jz    0xb32aba
  ││││││╎   0x00b32a4d      cmp   ecx, 0x24                            ; '$' ; 36
  ────────< 0x00b32a50      jz    0xb32aba
  ││││││╎   0x00b32a52      cmp   ecx, 0x22                            ; '"' ; 34
  ────────< 0x00b32a55      jz    0xb32aba
  ││││││╎   0x00b32a57      cmp   ecx, 0x10                            ; 16
  ────────< 0x00b32a5a      jz    0xb32aba
  ││││││╎   0x00b32a5c      cmp   ecx, 0x0f                            ; 0xf ; 15
  ────────< 0x00b32a5f      jz    0xb32aba
  ││││││╎   0x00b32a61      cmp   ecx, 0x14                            ; 20
  ────────< 0x00b32a64      jz    0xb32aba
  ││││││╎   0x00b32a66      cmp   ecx, 0x1c                            ; 28
  ────────< 0x00b32a69      jz    0xb32aba
  ││││││╎   0x00b32a6b      cmp   ecx, 0x0c                            ; 0xc ; 12
  ────────< 0x00b32a6e      jz    0xb32aba
  ││││││╎   0x00b32a70      cmp   ecx, 0x0d                            ; 0xd ; 13
  ────────< 0x00b32a73      jz    0xb32aba
  ││││││╎   0x00b32a75      cmp   ecx, 0x0e                            ; 0xe ; 14
  ────────< 0x00b32a78      jz    0xb32aba
  ││││││╎   0x00b32a7a      cmp   ecx, 0x17                            ; 23
  ────────< 0x00b32a7d      jz    0xb32aba
  ││││││╎   0x00b32a7f      cmp   ecx, 0x16                            ; 22
  ────────< 0x00b32a82      jz    0xb32aba
  ││││││╎   0x00b32a84      cmp   ecx, 0x15                            ; 21
  ────────< 0x00b32a87      jz    0xb32aba
  ││││││╎   0x00b32a89      cmp   ecx, 0x01                            ; 1
  ────────< 0x00b32a8c      jz    0xb32aba
  ││││││╎   0x00b32a8e      cmp   ecx, 0x11                            ; 17
  ────────< 0x00b32a91      jz    0xb32aba
  ││││││╎   0x00b32a93      cmp   ecx, 0x12                            ; 18
  ────────< 0x00b32a96      jz    0xb32aba
  ││││││╎   0x00b32a98      cmp   ecx, 0x1b                            ; 27
  ────────< 0x00b32a9b      jz    0xb32aba
  ││││││╎   0x00b32a9d      cmp   ecx, 0x1d                            ; 29
  ────────< 0x00b32aa0      jz    0xb32aba
  ││││││╎   0x00b32aa2      cmp   ecx, 0x1e                            ; 30
  ────────< 0x00b32aa5      jz    0xb32aba
  ││││││╎   0x00b32aa7      cmp   ecx, 0x1f                            ; 31
  ────────< 0x00b32aaa      jz    0xb32aba
  ││││││╎   0x00b32aac      cmp   ecx, 0x23                            ; '#' ; 35
  ────────< 0x00b32aaf      jz    0xb32aba
  ││││││╎   0x00b32ab1      cmp   ecx, 0x20                            ; 32
  ────────< 0x00b32ab4      jz    0xb32aba
  ││││││╎   0x00b32ab6      xor   al, al
  ────────< 0x00b32ab8      jmp   0xb32abc
  └└└└────> 0x00b32aba      mov   al, 0x01
  ────────> 0x00b32abc      test  al, al
     ┌────< 0x00b32abe      jz    0xb33ef1
     │││╎   0x00b32ac4      mov   byte [ebp-0x41c], 0x00
     │││╎   0x00b32acb      cmp   ecx, 0x0d                            ; 0xd ; 13
    ┌─────< 0x00b32ace      jz    0xb32ada
    ││││╎   0x00b32ad0      cmp   ecx, 0x0c                            ; 0xc ; 12
   ┌──────< 0x00b32ad3      jz    0xb32ada
   │││││╎   0x00b32ad5      cmp   ecx, 0x16                            ; 22
  ┌───────< 0x00b32ad8      jnz   0xb32ae1
  │└└─────> 0x00b32ada      mov   byte [ebp-0x41c], 0x01
  └───────> 0x00b32ae1      cmp   edi, 0x01                            ; 1
    ┌─────< 0x00b32ae4      jnz   0xb32c77
    ││││╎   0x00b32aea      cmp   ecx, 0x15                            ; 21
   ┌──────< 0x00b32aed      jnz   0xb32c77
   │││││╎   0x00b32af3      mov   eax, dword [ebp-0x430]
   │││││╎   0x00b32af9      mov   dword [ebp-0x364], 0xffffffff        ; -1
   │││││╎   0x00b32b03      mov   edx, dword [eax]
   │││││╎   0x00b32b05      mov   dword [ebp-0x364], edx
   │││││╎   0x00b32b0b      mov   eax, dword [0x201f660]               ; [0x201f660:4]=0
   │││││╎   0x00b32b10      xor   esi, esi
   │││││╎   0x00b32b12      xor   edi, edi
   │││││╎   0x00b32b14      mov   byte [ebp-0x04], 0x07
   │││││╎   0x00b32b18      mov   eax, dword [eax+0x1f8]
   │││││╎   0x00b32b1e      mov   dword [ebp-0x3ac], edi
   │││││╎   0x00b32b24      mov   dword [ebp-0x3a8], esi
   │││││╎   0x00b32b2a      mov   dword [ebp-0x3a4], esi
   │││││╎   0x00b32b30      mov   ecx, dword [eax*4+0x2027ed0]
   │││││╎   0x00b32b37      mov   dword [ebp-0x3a0], esi
   │││││╎   0x00b32b3d      mov   dword [ebp-0x3b0], ecx
   │││││╎   0x00b32b43      test  ecx, ecx
  ┌───────< 0x00b32b45      jz    0xb32b72
  ││││││╎   0x00b32b47      mov   eax, dword [ecx]
  ││││││╎   0x00b32b49      lea   edx, dword [ebp-0x3a4]
  ││││││╎   0x00b32b4f      push  edx
  ││││││╎   0x00b32b50      lea   edx, dword [ebp-0x3ac]
  ││││││╎   0x00b32b56      push  edx
  ││││││╎   0x00b32b57      call  dword [eax+0x3c]                     ; 60
  ││││││╎   0x00b32b5a      mov   edx, dword [ebp-0x364]
  ││││││╎   0x00b32b60      mov   esi, dword [ebp-0x3a8]
  ││││││╎   0x00b32b66      mov   edi, dword [ebp-0x3ac]
  ││││││╎   0x00b32b6c      mov   ecx, dword [ebp-0x3b0]
  └───────> 0x00b32b72      mov   byte [ebp-0x04], 0x08
   │││││╎   0x00b32b76      test  ecx, ecx
  ┌───────< 0x00b32b78      jz    0xb32b9b
  ││││││╎   0x00b32b7a      movzx eax, dx
  ││││││╎   0x00b32b7d      xor   ecx, ecx
  ││││││╎   0x00b32b7f      cmp   eax, esi
  ────────< 0x00b32b81      jnb   0xb32b9b
  ││││││╎   0x00b32b83      mov   ecx, dword [edi+eax*4]
  ││││││╎   0x00b32b86      test  ecx, ecx
  ────────< 0x00b32b88      jnz   0xb32b9b
  ││││││╎   0x00b32b8a      cmp   eax, dword [ebp-0x3a0]
  ────────< 0x00b32b90      jnb   0xb32b9b
  ││││││╎   0x00b32b92      mov   ecx, dword [ebp-0x3a4]
  ││││││╎   0x00b32b98      mov   ecx, dword [ecx+eax*4]
  └───────> 0x00b32b9b      lea   eax, dword [ebp-0x4d0]
   │││││╎   0x00b32ba1      push  eax
   │││││╎   0x00b32ba2      call  0x6e2140
   │││││╎   0x00b32ba7      mov   esi, dword [ebp-0x4d0]
   │││││╎   0x00b32bad      mov   eax, dword [ebp-0x4cc]
   │││││╎   0x00b32bb3      lea   edi, dword [esi+eax*4]
   │││││╎   0x00b32bb6      cmp   esi, edi
  ┌───────< 0x00b32bb8      jz    0xb32c58
  ││││││╎   0x00b32bbe      nop
  ────────> 0x00b32bc0      push  esi
  ││││││╎   0x00b32bc1      call  0xa95090
  ││││││╎   0x00b32bc6      mov   edx, eax
  ││││││╎   0x00b32bc8      xorps xmm0, xmm0
  ││││││╎   0x00b32bcb      psrldq xmm0, 0x0c
  ││││││╎   0x00b32bd0      xorps xmm1, xmm1
  ││││││╎   0x00b32bd3      movd  ecx, xmm0
  ││││││╎   0x00b32bd7      add   esp, 0x04
  ││││││╎   0x00b32bda      xorps xmm0, xmm0
  ││││││╎   0x00b32bdd      psrldq xmm1, 0x04
  ││││││╎   0x00b32be2      mov   eax, dword [edx+0x0c]
  ││││││╎   0x00b32be5      and   eax, ecx
  ││││││╎   0x00b32be7      psrldq xmm0, 0x08
  ││││││╎   0x00b32bec      not   ecx
  ││││││╎   0x00b32bee      xor   eax, ecx
  ││││││╎   0x00b32bf0      mov   ecx, dword [edx+0x08]
  ││││││╎   0x00b32bf3      mov   dword [ebp-0x368], eax
  ││││││╎   0x00b32bf9      movd  eax, xmm0
  ││││││╎   0x00b32bfd      and   ecx, eax
  ││││││╎   0x00b32bff      not   eax
  ││││││╎   0x00b32c01      xor   ecx, eax
  ││││││╎   0x00b32c03      movd  eax, xmm1
  ││││││╎   0x00b32c07      and   dword [ebp-0x368], ecx
  ││││││╎   0x00b32c0d      mov   ecx, dword [edx+0x04]
  ││││││╎   0x00b32c10      and   ecx, eax
  ││││││╎   0x00b32c12      not   eax
  ││││││╎   0x00b32c14      xor   ecx, eax
  ││││││╎   0x00b32c16      mov   eax, dword [edx]
  ││││││╎   0x00b32c18      and   dword [ebp-0x368], ecx
  ││││││╎   0x00b32c1e      and   eax, 0x10                            ; 16
  ││││││╎   0x00b32c21      mov   ecx, dword [ebp-0x368]
  ││││││╎   0x00b32c27      xor   eax, 0xffffffef                      ; 4294967279
  ││││││╎   0x00b32c2a      and   ecx, eax
  ││││││╎   0x00b32c2c      cmp   ecx, 0xffffffff                      ; -1
  ────────< 0x00b32c2f      jz    0xb32c3a
  ││││││╎   0x00b32c31      add   esi, 0x04
  ││││││╎   0x00b32c34      cmp   esi, edi
  ────────< 0x00b32c36      jnz   0xb32bc0
  ────────< 0x00b32c38      jmp   0xb32c58
  ────────> 0x00b32c3a      mov   eax, dword [ebp-0x3ec]
  ││││││╎   0x00b32c40      mov   ecx, dword [ebp-0x430]
  ││││││╎   0x00b32c46      mov   eax, dword [eax]
  ││││││╎   0x00b32c48      mov   dword [ecx], eax
  ││││││╎   0x00b32c4a      mov   ecx, dword [ebp-0x3ec]
  ││││││╎   0x00b32c50      mov   eax, dword [ebp-0x364]
  ││││││╎   0x00b32c56      mov   dword [ecx], eax
  └───────> 0x00b32c58      lea   ecx, dword [ebp-0x364]
   │││││╎   0x00b32c5e      mov   dword [ebp-0x3b0], 0x00
   │││││╎   0x00b32c68      mov   byte [ebp-0x04], 0x06
   │││││╎   0x00b32c6c      call  0x4dc500
   │││││╎   0x00b32c71      mov   esi, dword [ebp-0x35c]
   └└─────> 0x00b32c77      mov   edi, dword [esi+0x10]
     │││╎   0x00b32c7a      add   edi, dword [ebp-0x3e8]
     │││╎   0x00b32c80      lea   eax, dword [edi*4]
     │││╎   0x00b32c87      add   eax, 0x0f                            ; 0xf ; 15
     │││╎   0x00b32c8a      cmp   eax, 0x4020                          ; ' @'
    ┌─────< 0x00b32c8f      jnbe  0xb32c9a
    ││││╎   0x00b32c91      call  0x18076c0
    ││││╎   0x00b32c96      mov   eax, esp
   ┌──────< 0x00b32c98      jmp   0xb32c9c
   │└─────> 0x00b32c9a      xor   eax, eax
   └──────> 0x00b32c9c      add   eax, 0x0f                            ; 0xf ; 15
     │││╎   0x00b32c9f      lea   ecx, dword [edi*4]
     │││╎   0x00b32ca6      and   eax, 0xfffffff0                      ; 4294967280
     │││╎   0x00b32ca9      push  ecx
     │││╎   0x00b32caa      push  eax
     │││╎   0x00b32cab      lea   ecx, dword [ebp-0x3c4]
     │││╎   0x00b32cb1      mov   dword [ebp-0x3bc], eax
     │││╎   0x00b32cb7      call  0x4ea610
     │││╎   0x00b32cbc      mov   dword [ebp-0x3b8], 0x00
     │││╎   0x00b32cc6      mov   dword [ebp-0x3b4], edi
     │││╎   0x00b32ccc      push  dword [ebp-0x3e0]
     │││╎   0x00b32cd2      lea   eax, dword [ebp-0x3f4]
     │││╎   0x00b32cd8      mov   byte [ebp-0x04], 0x0a
     │││╎   0x00b32cdc      push  dword [ebp-0x41c]
     │││╎   0x00b32ce2      push  esi
     │││╎   0x00b32ce3      push  eax
     │││╎   0x00b32ce4      lea   eax, dword [ebp-0x3c4]
     │││╎   0x00b32cea      push  eax
     │││╎   0x00b32ceb      call  0xb2da90
     │││╎   0x00b32cf0      mov   edi, dword [ebp-0x3b8]
     │││╎   0x00b32cf6      add   esp, 0x14
     │││╎   0x00b32cf9      test  edi, edi
    ┌─────< 0x00b32cfb      jz    0xb33ec3
    ││││╎   0x00b32d01      mov   eax, dword [ebp-0x3cc]
    ││││╎   0x00b32d07      mov   byte [ebp-0x40c], 0x00
    ││││╎   0x00b32d0e      cmp   eax, 0x19                            ; 25
   ┌──────< 0x00b32d11      jz    0xb32d1d
   │││││╎   0x00b32d13      cmp   eax, 0x0c                            ; 0xc ; 12
  ┌───────< 0x00b32d16      jz    0xb32d1d
  ││││││╎   0x00b32d18      cmp   eax, 0x0d                            ; 0xd ; 13
  ────────< 0x00b32d1b      jnz   0xb32d24
  └└──────> 0x00b32d1d      mov   byte [ebp-0x40c], 0x01
  ────────> 0x00b32d24      lea   esi, dword [edi*4]
    ││││╎   0x00b32d2b      add   esi, 0x0f                            ; 0xf ; 15
    ││││╎   0x00b32d2e      mov   dword [ebp-0x374], esi
    ││││╎   0x00b32d34      cmp   esi, 0x4020                          ; ' @'
   ┌──────< 0x00b32d3a      jnbe  0xb32d47
   │││││╎   0x00b32d3c      mov   eax, esi
   │││││╎   0x00b32d3e      call  0x18076c0
   │││││╎   0x00b32d43      mov   eax, esp
  ┌───────< 0x00b32d45      jmp   0xb32d49
  │└──────> 0x00b32d47      xor   eax, eax
  └───────> 0x00b32d49      add   eax, 0x0f                            ; 0xf ; 15
    ││││╎   0x00b32d4c      lea   ecx, dword [edi*4]
    ││││╎   0x00b32d53      and   eax, 0xfffffff0                      ; 4294967280
    ││││╎   0x00b32d56      push  ecx
    ││││╎   0x00b32d57      push  eax
    ││││╎   0x00b32d58      lea   ecx, dword [ebp-0x3b0]
    ││││╎   0x00b32d5e      mov   dword [ebp-0x3a8], eax
    ││││╎   0x00b32d64      call  0x4ea610
    ││││╎   0x00b32d69      mov   dword [ebp-0x3a4], 0x00
    ││││╎   0x00b32d73      mov   dword [ebp-0x3a0], edi
    ││││╎   0x00b32d79      mov   byte [ebp-0x04], 0x0b                ; 0xb ; 11
    ││││╎   0x00b32d7d      cmp   esi, 0x4020                          ; ' @'
   ┌──────< 0x00b32d83      jnbe  0xb32d90
   │││││╎   0x00b32d85      mov   eax, esi
   │││││╎   0x00b32d87      call  0x18076c0
   │││││╎   0x00b32d8c      mov   eax, esp
  ┌───────< 0x00b32d8e      jmp   0xb32d92
  │└──────> 0x00b32d90      xor   eax, eax
  └───────> 0x00b32d92      add   eax, 0x0f                            ; 0xf ; 15
    ││││╎   0x00b32d95      lea   ecx, dword [edi*4]
    ││││╎   0x00b32d9c      and   eax, 0xfffffff0                      ; 4294967280
    ││││╎   0x00b32d9f      push  ecx
    ││││╎   0x00b32da0      push  eax
    ││││╎   0x00b32da1      lea   ecx, dword [ebp-0x394]
    ││││╎   0x00b32da7      mov   dword [ebp-0x38c], eax
    ││││╎   0x00b32dad      call  0x4ea610
    ││││╎   0x00b32db2      mov   dword [ebp-0x388], 0x00
    ││││╎   0x00b32dbc      mov   dword [ebp-0x384], edi
    ││││╎   0x00b32dc2      mov   byte [ebp-0x04], 0x0c                ; 0xc ; 12
    ││││╎   0x00b32dc6      test  edi, edi
   ┌──────< 0x00b32dc8      jz    0xb32df0
   │││││╎   0x00b32dca      xor   esi, esi
   │││││╎   0x00b32dcc      nop   dword [eax], eax
  ┌───────> 0x00b32dd0      mov   eax, dword [ebp-0x38c]
  ╎│││││╎   0x00b32dd6      lea   ecx, dword [eax+esi*4]
  ╎│││││╎   0x00b32dd9      call  0x4f6c50
  ╎│││││╎   0x00b32dde      inc   esi
  ╎│││││╎   0x00b32ddf      cmp   esi, edi
  └───────< 0x00b32de1      jb    0xb32dd0
   │││││╎   0x00b32de3      mov   esi, dword [ebp-0x374]
   │││││╎   0x00b32de9      nop   dword [eax], eax
   └──────> 0x00b32df0      mov   eax, dword [ebp-0x38c]
    ││││╎   0x00b32df6      mov   dword [ebp-0x4d8], eax
    ││││╎   0x00b32dfc      mov   eax, dword [ebp-0x3bc]
    ││││╎   0x00b32e02      mov   dword [ebp-0x4c8], eax
    ││││╎   0x00b32e08      mov   eax, dword [ebp-0x3b8]
    ││││╎   0x00b32e0e      mov   dword [ebp-0x4c4], eax
    ││││╎   0x00b32e14      lea   eax, dword [ebp-0x4c8]
    ││││╎   0x00b32e1a      push  0x00
    ││││╎   0x00b32e1c      push  eax
    ││││╎   0x00b32e1d      lea   eax, dword [ebp-0x4d8]
    ││││╎   0x00b32e23      mov   dword [ebp-0x388], edi
    ││││╎   0x00b32e29      push  eax
    ││││╎   0x00b32e2a      mov   dword [ebp-0x4d4], edi
    ││││╎   0x00b32e30      call  0xac7ee0
    ││││╎   0x00b32e35      add   esp, 0x0c
    ││││╎   0x00b32e38      cmp   esi, 0x4020                          ; ' @'
   ┌──────< 0x00b32e3e      jnbe  0xb32e4b
   │││││╎   0x00b32e40      mov   eax, esi
   │││││╎   0x00b32e42      call  0x18076c0
   │││││╎   0x00b32e47      mov   eax, esp
  ┌───────< 0x00b32e49      jmp   0xb32e4d
  │└──────> 0x00b32e4b      xor   eax, eax
  └───────> 0x00b32e4d      add   eax, 0x0f                            ; 0xf ; 15
    ││││╎   0x00b32e50      lea   ecx, dword [edi*4]
    ││││╎   0x00b32e57      and   eax, 0xfffffff0                      ; 4294967280
    ││││╎   0x00b32e5a      push  ecx
    ││││╎   0x00b32e5b      push  eax
    ││││╎   0x00b32e5c      lea   ecx, dword [ebp-0x408]
    ││││╎   0x00b32e62      mov   dword [ebp-0x400], eax
    ││││╎   0x00b32e68      call  0x4ea610
    ││││╎   0x00b32e6d      mov   dword [ebp-0x3fc], 0x00
    ││││╎   0x00b32e77      mov   dword [ebp-0x3f8], edi
    ││││╎   0x00b32e7d      xor   edi, edi
    ││││╎   0x00b32e7f      mov   byte [ebp-0x04], 0x0d                ; 0xd ; 13
    ││││╎   0x00b32e83      cmp   dword [ebp-0x388], edi
   ┌──────< 0x00b32e89      jbe   0xb32efa
   │││││╎   0x00b32e8b      nop   dword [eax+eax*1], eax
  ┌───────> 0x00b32e90      mov   esi, dword [ebp-0x3fc]
  ╎│││││╎   0x00b32e96      test  esi, esi
  ────────< 0x00b32e98      jz    0xb32eb6
  ╎│││││╎   0x00b32e9a      nop   word [eax+eax*1], ax
  ────────> 0x00b32ea0      mov   ecx, dword [ebp-0x400]
  ╎│││││╎   0x00b32ea6      add   ecx, 0xfffffffc                      ; 4294967292
  ╎│││││╎   0x00b32ea9      lea   ecx, dword [ecx+esi*4]
  ╎│││││╎   0x00b32eac      call  0x4dc500
  ╎│││││╎   0x00b32eb1      sub   esi, 0x01
  ────────< 0x00b32eb4      jnz   0xb32ea0
  ────────> 0x00b32eb6      mov   eax, dword [ebp-0x38c]
  ╎│││││╎   0x00b32ebc      mov   dword [ebp-0x3fc], 0x00
  ╎│││││╎   0x00b32ec6      cmp   dword [eax+edi*4], 0xffffffff
  ────────< 0x00b32eca      jnz   0xb32ef1
  ╎│││││╎   0x00b32ecc      mov   edx, dword [ebp-0x3a4]
  ╎│││││╎   0x00b32ed2      mov   eax, dword [ebp-0x3bc]
  ╎│││││╎   0x00b32ed8      mov   ecx, dword [ebp-0x3a8]
  ╎│││││╎   0x00b32ede      mov   dword [ecx+edx*4], 0xffffffff        ; [0xffffffff:4]=-1 ; -1
  ╎│││││╎   0x00b32ee5      mov   eax, dword [eax+edi*4]
  ╎│││││╎   0x00b32ee8      mov   dword [ecx+edx*4], eax
  ╎│││││╎   0x00b32eeb      inc   dword [ebp-0x3a4]
  ────────> 0x00b32ef1      inc   edi
  ╎│││││╎   0x00b32ef2      cmp   edi, dword [ebp-0x388]
  └───────< 0x00b32ef8      jb    0xb32e90
   └──────> 0x00b32efa      mov   eax, dword [0x201f660]               ; [0x201f660:4]=0
    ││││╎   0x00b32eff      mov   eax, dword [eax+0x88]
    ││││╎   0x00b32f05      mov   dword [ebp-0x444], 0x00
    ││││╎   0x00b32f0f      mov   dword [ebp-0x440], 0x00
    ││││╎   0x00b32f19      mov   ecx, dword [eax*4+0x20282d4]
    ││││╎   0x00b32f20      mov   dword [ebp-0x448], ecx
    ││││╎   0x00b32f26      test  ecx, ecx
   ┌──────< 0x00b32f28      jz    0xb32f38
   │││││╎   0x00b32f2a      mov   eax, dword [ecx]
   │││││╎   0x00b32f2c      lea   edx, dword [ebp-0x444]
   │││││╎   0x00b32f32      push  0x00
   │││││╎   0x00b32f34      push  edx
   │││││╎   0x00b32f35      call  dword [eax+0x40]                     ; 64
   └──────> 0x00b32f38      xor   edi, edi
    ││││╎   0x00b32f3a      mov   dword [ebp-0x370], edi
    ││││╎   0x00b32f40      cmp   dword [ebp-0x388], edi
   ┌──────< 0x00b32f46      jbe   0xb33134
   │││││╎   0x00b32f4c      nop   dword [eax], eax
  ┌───────> 0x00b32f50      mov   esi, dword [ebp-0x3fc]
  ╎│││││╎   0x00b32f56      test  esi, esi
  ────────< 0x00b32f58      jz    0xb32f76
  ╎│││││╎   0x00b32f5a      nop   word [eax+eax*1], ax
  ────────> 0x00b32f60      mov   ecx, dword [ebp-0x400]
  ╎│││││╎   0x00b32f66      add   ecx, 0xfffffffc                      ; 4294967292
  ╎│││││╎   0x00b32f69      lea   ecx, dword [ecx+esi*4]
  ╎│││││╎   0x00b32f6c      call  0x4dc500
  ╎│││││╎   0x00b32f71      sub   esi, 0x01
  ────────< 0x00b32f74      jnz   0xb32f60
  ────────> 0x00b32f76      mov   eax, dword [ebp-0x38c]
  ╎│││││╎   0x00b32f7c      xor   edx, edx
  ╎│││││╎   0x00b32f7e      mov   dword [ebp-0x3d8], 0xffffffff        ; -1
  ╎│││││╎   0x00b32f88      mov   dword [ebp-0x3fc], edx
  ╎│││││╎   0x00b32f8e      mov   eax, dword [eax+edi*4]
  ╎│││││╎   0x00b32f91      mov   dword [ebp-0x3d8], eax
  ╎│││││╎   0x00b32f97      mov   byte [ebp-0x04], 0x0f                ; 0xf ; 15
  ╎│││││╎   0x00b32f9b      cmp   eax, 0xffffffff                      ; -1
  ────────< 0x00b32f9e      jz    0xb33116
  ╎│││││╎   0x00b32fa4      mov   esi, edi
  ╎│││││╎   0x00b32fa6      cmp   edi, dword [ebp-0x388]
  ────────< 0x00b32fac      jnb   0xb32ffd
  ╎│││││╎   0x00b32fae      nop
  ────────> 0x00b32fb0      mov   ecx, dword [ebp-0x38c]
  ╎│││││╎   0x00b32fb6      cmp   dword [ecx+esi*4], eax
  ────────< 0x00b32fb9      jnz   0xb32ff4
  ╎│││││╎   0x00b32fbb      mov   ecx, dword [ebp-0x400]
  ╎│││││╎   0x00b32fc1      mov   eax, dword [ebp-0x3bc]
  ╎│││││╎   0x00b32fc7      mov   dword [ecx+edx*4], 0xffffffff        ; [0xffffffff:4]=-1 ; -1
  ╎│││││╎   0x00b32fce      mov   eax, dword [eax+esi*4]
  ╎│││││╎   0x00b32fd1      mov   dword [ecx+edx*4], eax
  ╎│││││╎   0x00b32fd4      mov   eax, dword [ebp-0x38c]
  ╎│││││╎   0x00b32fda      inc   dword [ebp-0x3fc]
  ╎│││││╎   0x00b32fe0      lea   ecx, dword [eax+esi*4]
  ╎│││││╎   0x00b32fe3      call  0xaffbf0
  ╎│││││╎   0x00b32fe8      mov   edx, dword [ebp-0x3fc]
  ╎│││││╎   0x00b32fee      mov   eax, dword [ebp-0x3d8]
  ────────> 0x00b32ff4      inc   esi
  ╎│││││╎   0x00b32ff5      cmp   esi, dword [ebp-0x388]
  ────────< 0x00b32ffb      jb    0xb32fb0
  ────────> 0x00b32ffd      cmp   dword [ebp-0x448], 0x00
  ────────< 0x00b33004      jz    0xb3301c
  ╎│││││╎   0x00b33006      movzx esi, ax
  ╎│││││╎   0x00b33009      cmp   esi, dword [ebp-0x440]
  ────────< 0x00b3300f      jnb   0xb3301c
  ╎│││││╎   0x00b33011      mov   eax, dword [ebp-0x444]
  ╎│││││╎   0x00b33017      mov   esi, dword [eax+esi*4]
  ────────< 0x00b3301a      jmp   0xb3301e
  ────────> 0x00b3301c      xor   esi, esi
  ────────> 0x00b3301e      push  dword [ebp-0x3e0]
  ╎│││││╎   0x00b33024      mov   eax, dword [ebp-0x3ec]
  ╎│││││╎   0x00b3302a      push  dword [ebp-0x40c]
  ╎│││││╎   0x00b33030      mov   dword [ebp-0x498], eax
  ╎│││││╎   0x00b33036      mov   eax, dword [ebp-0x3e8]
  ╎│││││╎   0x00b3303c      mov   dword [ebp-0x494], eax
  ╎│││││╎   0x00b33042      mov   eax, dword [ebp-0x400]
  ╎│││││╎   0x00b33048      mov   dword [ebp-0x4a0], eax
  ╎│││││╎   0x00b3304e      lea   eax, dword [ebp-0x4fc]
  ╎│││││╎   0x00b33054      push  eax
  ╎│││││╎   0x00b33055      push  dword [ebp-0x410]
  ╎│││││╎   0x00b3305b      lea   eax, dword [ebp-0x498]
  ╎│││││╎   0x00b33061      mov   dword [ebp-0x49c], edx
  ╎│││││╎   0x00b33067      push  dword [ebp-0x474]
  ╎│││││╎   0x00b3306d      push  eax
  ╎│││││╎   0x00b3306e      lea   eax, dword [ebp-0x4a0]
  ╎│││││╎   0x00b33074      push  eax
  ╎│││││╎   0x00b33075      push  ecx
  ╎│││││╎   0x00b33076      push  esp
  ╎│││││╎   0x00b33077      call  0xb70410
  ╎│││││╎   0x00b3307c      add   esp, 0x04
  ╎│││││╎   0x00b3307f      mov   ecx, esi
  ╎│││││╎   0x00b33081      push  dword [ebp-0x3cc]
  ╎│││││╎   0x00b33087      call  0xabbd70
  ╎│││││╎   0x00b3308c      test  al, al
  ────────< 0x00b3308e      jnz   0xb330de
  ╎│││││╎   0x00b33090      mov   eax, dword [ebp-0x400]
  ╎│││││╎   0x00b33096      mov   ecx, dword [ebp-0x3fc]
  ╎│││││╎   0x00b3309c      lea   ecx, dword [eax+ecx*4]
  ╎│││││╎   0x00b3309f      cmp   eax, ecx
  ────────< 0x00b330a1      jz    0xb33116
  ╎│││││╎   0x00b330a7      mov   edi, dword [ebp-0x3a4]
  ╎│││││╎   0x00b330ad      nop   dword [eax], eax
  ────────> 0x00b330b0      mov   esi, dword [ebp-0x3a8]
  ╎│││││╎   0x00b330b6      mov   dword [esi+edi*4], 0xffffffff        ; [0xffffffff:4]=-1 ; -1
  ╎│││││╎   0x00b330bd      mov   edx, dword [eax]
  ╎│││││╎   0x00b330bf      add   eax, 0x04
  ╎│││││╎   0x00b330c2      mov   dword [esi+edi*4], edx
  ╎│││││╎   0x00b330c5      mov   edi, dword [ebp-0x3a4]
  ╎│││││╎   0x00b330cb      inc   edi
  ╎│││││╎   0x00b330cc      mov   dword [ebp-0x3a4], edi
  ╎│││││╎   0x00b330d2      cmp   eax, ecx
  ────────< 0x00b330d4      jnz   0xb330b0
  ╎│││││╎   0x00b330d6      mov   edi, dword [ebp-0x370]
  ────────< 0x00b330dc      jmp   0xb33116
  ────────> 0x00b330de      mov   edx, dword [ebp-0x3dc]
  ╎│││││╎   0x00b330e4      test  edx, edx
  ────────< 0x00b330e6      jz    0xb33116
  ╎│││││╎   0x00b330e8      mov   esi, dword [edx+0x10]
  ╎│││││╎   0x00b330eb      cmp   esi, dword [edx+0x04]
  ────────< 0x00b330ee      jnz   0xb330fd
  ╎│││││╎   0x00b330f0      mov   ecx, edx
  ╎│││││╎   0x00b330f2      call  0x7aab00
  ╎│││││╎   0x00b330f7      mov   edx, dword [ebp-0x3dc]
  ────────> 0x00b330fd      mov   ecx, dword [edx+0x0c]
  ╎│││││╎   0x00b33100      mov   dword [ecx+esi*4], 0xffffffff        ; [0xffffffff:4]=-1 ; -1
  ╎│││││╎   0x00b33107      mov   eax, dword [ebp-0x3d8]
  ╎│││││╎   0x00b3310d      mov   dword [ecx+esi*4], eax
  ╎│││││╎   0x00b33110      lea   eax, dword [esi+0x01]
  ╎│││││╎   0x00b33113      mov   dword [edx+0x10], eax
  ────────> 0x00b33116      lea   ecx, dword [ebp-0x3d8]
  ╎│││││╎   0x00b3311c      call  0x4dc500
  ╎│││││╎   0x00b33121      inc   edi
  ╎│││││╎   0x00b33122      mov   dword [ebp-0x370], edi
  ╎│││││╎   0x00b33128      cmp   edi, dword [ebp-0x388]
  └───────< 0x00b3312e      jb    0xb32f50
   └──────> 0x00b33134      mov   eax, dword [ebp-0x3a8]
    ││││╎   0x00b3313a      mov   dword [ebp-0x36c], eax
    ││││╎   0x00b33140      mov   dword [ebp-0x4b8], eax
    ││││╎   0x00b33146      mov   eax, dword [ebp-0x3a4]
    ││││╎   0x00b3314c      mov   dword [ebp-0x370], eax
    ││││╎   0x00b33152      mov   dword [ebp-0x4b4], eax
    ││││╎   0x00b33158      mov   esi, dword [ebp-0x3fc]
    ││││╎   0x00b3315e      mov   dword [ebp-0x448], 0x00
    ││││╎   0x00b33168      test  esi, esi
   ┌──────< 0x00b3316a      jz    0xb33186
   │││││╎   0x00b3316c      nop   dword [eax], eax
  ┌───────> 0x00b33170      mov   ecx, dword [ebp-0x400]
  ╎│││││╎   0x00b33176      add   ecx, 0xfffffffc                      ; 4294967292
  ╎│││││╎   0x00b33179      lea   ecx, dword [ecx+esi*4]
  ╎│││││╎   0x00b3317c      call  0x4dc500
  ╎│││││╎   0x00b33181      sub   esi, 0x01
  └───────< 0x00b33184      jnz   0xb33170
   └──────> 0x00b33186      mov   dword [ebp-0x3fc], 0x00
    ││││╎   0x00b33190      mov   ecx, dword [ebp-0x408]
    ││││╎   0x00b33196      mov   byte [ebp-0x04], 0x11                ; 17
    ││││╎   0x00b3319a      test  ecx, ecx
   ┌──────< 0x00b3319c      jz    0xb331aa
   │││││╎   0x00b3319e      lea   eax, dword [ebp-0x408]
   │││││╎   0x00b331a4      push  eax
   │││││╎   0x00b331a5      call  0x517c70
   └──────> 0x00b331aa      mov   esi, dword [ebp-0x388]
    ││││╎   0x00b331b0      test  esi, esi
   ┌──────< 0x00b331b2      jz    0xb331ca
  ┌───────> 0x00b331b4      mov   ecx, dword [ebp-0x38c]
  ╎│││││╎   0x00b331ba      add   ecx, 0xfffffffc                      ; 4294967292
  ╎│││││╎   0x00b331bd      lea   ecx, dword [ecx+esi*4]
  ╎│││││╎   0x00b331c0      call  0x4dc500
  ╎│││││╎   0x00b331c5      sub   esi, 0x01
  └───────< 0x00b331c8      jnz   0xb331b4
   └──────> 0x00b331ca      mov   dword [ebp-0x388], 0x00
    ││││╎   0x00b331d4      mov   ecx, dword [ebp-0x394]
    ││││╎   0x00b331da      mov   byte [ebp-0x04], 0x12                ; 18
    ││││╎   0x00b331de      test  ecx, ecx
   ┌──────< 0x00b331e0      jz    0xb331ee
   │││││╎   0x00b331e2      lea   eax, dword [ebp-0x394]
   │││││╎   0x00b331e8      push  eax
   │││││╎   0x00b331e9      call  0x517c70
   └──────> 0x00b331ee      cmp   dword [ebp-0x370], 0x00
    ││││╎   0x00b331f5      mov   byte [ebp-0x04], 0x0b                ; 0xb ; 11
   ┌──────< 0x00b331f9      jz    0xb33e9e
   │││││╎   0x00b331ff      mov   eax, dword [ebp-0x3cc]
   │││││╎   0x00b33205      add   eax, 0xffffffed                      ; 4294967277
   │││││╎   0x00b33208      mov   dword [ebp-0x35c], 0x00
   │││││╎   0x00b33212      cmp   eax, 0x11                            ; 17
  ┌───────< 0x00b33215      jnbe  0xb33bf1
  ││││││╎   0x00b3321b      movzx eax, byte [eax+0xb34238]
  ││││││╎   0x00b33222      jmp   dword [eax*4+0xb34218]
  ││││││╎   0x00b33229      mov   eax, dword [0x201f660]               ; [0x201f660:4]=0
  ││││││╎   0x00b3322e      xor   esi, esi
  ││││││╎   0x00b33230      xor   edx, edx
  ││││││╎   0x00b33232      mov   eax, dword [eax+0x1f8]
  ││││││╎   0x00b33238      mov   dword [ebp-0x30], esi
  ││││││╎   0x00b3323b      mov   dword [ebp-0x2c], edx
  ││││││╎   0x00b3323e      mov   ecx, dword [eax*4+0x2027ed0]
  ││││││╎   0x00b33245      mov   dword [ebp-0x34], ecx
  ││││││╎   0x00b33248      test  ecx, ecx
  ────────< 0x00b3324a      jz    0xb3325f
  ││││││╎   0x00b3324c      mov   eax, dword [ecx]
  ││││││╎   0x00b3324e      push  edx
  ││││││╎   0x00b3324f      lea   edx, dword [ebp-0x30]
  ││││││╎   0x00b33252      push  edx
  ││││││╎   0x00b33253      call  dword [eax+0x3c]                     ; 60
  ││││││╎   0x00b33256      mov   edx, dword [ebp-0x2c]
  ││││││╎   0x00b33259      mov   esi, dword [ebp-0x30]
  ││││││╎   0x00b3325c      mov   ecx, dword [ebp-0x34]
  ────────> 0x00b3325f      mov   byte [ebp-0x04], 0x13                ; 19
  ││││││╎   0x00b33263      test  ecx, ecx
  ────────< 0x00b33265      jz    0xb33279
  ││││││╎   0x00b33267      mov   eax, dword [ebp-0x3ec]
  ││││││╎   0x00b3326d      movzx ecx, word [eax]
  ││││││╎   0x00b33270      cmp   ecx, edx
  ────────< 0x00b33272      jnb   0xb33279
  ││││││╎   0x00b33274      mov   ecx, dword [esi+ecx*4]
  ────────< 0x00b33277      jmp   0xb3327b
  ────────> 0x00b33279      xor   ecx, ecx
  ────────> 0x00b3327b      mov   ecx, dword [ecx+0x3c]
  ││││││╎   0x00b3327e      call  0x670a40
  ││││││╎   0x00b33283      movss xmm0, dword [eax]
  ││││││╎   0x00b33287      movss xmm1, dword [eax+0x04]
  ││││││╎   0x00b3328c      movss dword [ebp-0x1c], xmm0
  ││││││╎   0x00b33291      movss dword [ebp-0x18], xmm1
  ││││││╎   0x00b33296      mov   dword [ebp-0x14], 0x00
  ││││││╎   0x00b3329d      mov   dword [ebp-0x34], 0x00
  ││││││╎   0x00b332a4      mov   byte [ebp-0x04], 0x0b                ; 0xb ; 11
  ││││││╎   0x00b332a8      mov   esi, dword [ebp-0x35c]
  ────────< 0x00b332ae      jmp   0xb33bf3
  ││││││╎   0x00b332b3      lea   eax, dword [ebp-0x510]
  ││││││╎   0x00b332b9      push  eax
  ││││││╎   0x00b332ba      call  0xb6b590
  ││││││╎   0x00b332bf      push  eax
  ││││││╎   0x00b332c0      call  0xb3d280
  ││││││╎   0x00b332c5      mov   edi, dword [eax+0x18]
  ││││││╎   0x00b332c8      add   esp, 0x08
  ││││││╎   0x00b332cb      mov   dword [ebp-0x35c], eax
  ││││││╎   0x00b332d1      cmp   edi, dword [eax+0x0c]
  ││││││╎   0x00b332d4      lea   esi, dword [eax+0x08]
  ────────< 0x00b332d7      jnz   0xb332e0
  ││││││╎   0x00b332d9      mov   ecx, esi
  ││││││╎   0x00b332db      call  0xa23680
  ────────> 0x00b332e0      mov   eax, dword [esi+0x0c]
  ││││││╎   0x00b332e3      lea   ecx, dword [edi+edi*2]
  ││││││╎   0x00b332e6      movss xmm0, dword [ebp-0x1c]
  ││││││╎   0x00b332eb      movss dword [eax+ecx*4], xmm0
  ││││││╎   0x00b332f0      movss xmm0, dword [ebp-0x18]
  ││││││╎   0x00b332f5      movss dword [eax+ecx*4+0x04], xmm0
  ││││││╎   0x00b332fb      movss xmm0, dword [ebp-0x14]
  ││││││╎   0x00b33300      movss dword [eax+ecx*4+0x08], xmm0
  ││││││╎   0x00b33306      lea   eax, dword [edi+0x01]
  ││││││╎   0x00b33309      mov   dword [esi+0x10], eax
  ││││││╎   0x00b3330c      mov   esi, dword [ebp-0x35c]
  ────────< 0x00b33312      jmp   0xb33bf3
  ││││││╎   0x00b33317      lea   eax, dword [ebp-0x50c]
  ││││││╎   0x00b3331d      push  eax
  ││││││╎   0x00b3331e      call  0xb6b570
  ││││││╎   0x00b33323      push  eax
  ││││││╎   0x00b33324      call  0xb3d280
  ││││││╎   0x00b33329      add   esp, 0x08
  ││││││╎   0x00b3332c      mov   esi, eax
  ────────< 0x00b3332e      jmp   0xb33bf3
  ││││││╎   0x00b33333      mov   dword [ebp-0x40], 0x00
  ││││││╎   0x00b3333a      xor   ecx, ecx
  ││││││╎   0x00b3333c      mov   dword [ebp-0x3c], 0x00
  ││││││╎   0x00b33343      mov   dword [ebp-0x38], 0x00
  ││││││╎   0x00b3334a      nop   word [eax+eax*1], ax
  ────────> 0x00b33350      movss xmm0, dword [ebp+ecx*1-0x1c]
  ││││││╎   0x00b33356      ucomiss xmm0, dword [ebp+ecx*1-0x40]
  ││││││╎   0x00b3335b      lahf
  ││││││╎   0x00b3335c      test  ah, 0x44                             ; 68
  ────────< 0x00b3335f      jp    0xb33392
  ││││││╎   0x00b33361      add   ecx, 0x04
  ││││││╎   0x00b33364      cmp   ecx, 0x0c                            ; 0xc ; 12
  ────────< 0x00b33367      jb    0xb33350
  ││││││╎   0x00b33369      lea   eax, dword [ebp-0x508]
  ││││││╎   0x00b3336f      push  eax
  ││││││╎   0x00b33370      call  0xb6b5c0
  ││││││╎   0x00b33375      push  eax
  ││││││╎   0x00b33376      call  0xb3d280
  ││││││╎   0x00b3337b      add   esp, 0x08
  ││││││╎   0x00b3337e      mov   dword [ebp-0x35c], eax
  ││││││╎   0x00b33384      mov   esi, eax
  ││││││╎   0x00b33386      mov   dword [eax+0x04], 0x21               ; '!'
  ││││││╎                                                              ; [0x21:4]=-1 ; 33
  ────────< 0x00b3338d      jmp   0xb33bf3
  ────────> 0x00b33392      lea   eax, dword [ebp-0x504]
  ││││││╎   0x00b33398      push  eax
  ││││││╎   0x00b33399      call  0xb6b5c0
  ││││││╎   0x00b3339e      push  eax
  ││││││╎   0x00b3339f      call  0xb3d280
  ││││││╎   0x00b333a4      add   esp, 0x08
  ││││││╎   0x00b333a7      mov   dword [ebp-0x35c], eax
  ││││││╎   0x00b333ad      mov   esi, eax
  ││││││╎   0x00b333af      mov   dword [eax+0x04], 0x21               ; '!'
  ││││││╎                                                              ; [0x21:4]=-1 ; 33
  ││││││╎   0x00b333b6      movss xmm1, dword [ebp-0x18]
  ││││││╎   0x00b333bb      movss xmm2, dword [ebp-0x14]
  ││││││╎   0x00b333c0      movss xmm0, dword [ebp-0x1c]
  ││││││╎   0x00b333c5      movss dword [eax+0x34], xmm0
  ││││││╎   0x00b333ca      movss dword [eax+0x38], xmm1
  ││││││╎   0x00b333cf      movss dword [eax+0x3c], xmm2
  ────────< 0x00b333d4      jmp   0xb33bf3
  ││││││╎   0x00b333d9      lea   eax, dword [ebp-0x500]
  ││││││╎   0x00b333df      push  eax
  ││││││╎   0x00b333e0      call  0xb6eb20
  ││││││╎   0x00b333e5      push  eax
  ││││││╎   0x00b333e6      call  0xb3d280
  ││││││╎   0x00b333eb      mov   ecx, eax
  ││││││╎   0x00b333ed      add   esp, 0x08
  ││││││╎   0x00b333f0      mov   eax, dword [ebp-0x3ec]
  ││││││╎   0x00b333f6      mov   dword [ebp-0x35c], ecx
  ││││││╎   0x00b333fc      mov   eax, dword [eax]
  ││││││╎   0x00b333fe      mov   dword [ecx+0x04], eax
  ││││││╎   0x00b33401      mov   ecx, dword [ebp-0x424]
  ││││││╎   0x00b33407      call  0xb402b0
  ││││││╎   0x00b3340c      mov   esi, dword [ebp-0x35c]
  ││││││╎   0x00b33412      mov   dword [esi+0x08], eax
  ────────< 0x00b33415      jmp   0xb33bf3
  ││││││╎   0x00b3341a      cmp   dword [ebp-0x3e8], 0x00
  ││││││╎   0x00b33421      mov   dword [ebp-0x28], 0x7f800000
  ││││││╎   0x00b33428      mov   dword [ebp-0x24], 0x7f800000
  ││││││╎   0x00b3342f      mov   dword [ebp-0x20], 0x7f800000
  ────────< 0x00b33436      jz    0xb33554
  ││││││╎   0x00b3343c      mov   eax, dword [ebp-0x3ec]
  ││││││╎   0x00b33442      xor   edx, edx
  ││││││╎   0x00b33444      mov   dword [ebp-0x364], eax
  ││││││╎   0x00b3344a      xor   esi, esi
  ││││││╎   0x00b3344c      mov   eax, dword [0x201f660]               ; [0x201f660:4]=0
  ││││││╎   0x00b33451      xor   edi, edi
  ││││││╎   0x00b33453      mov   eax, dword [eax+0x1f8]
  ││││││╎   0x00b33459      mov   dword [ebp-0x390], esi
  ││││││╎   0x00b3345f      mov   dword [ebp-0x38c], edx
  ││││││╎   0x00b33465      mov   dword [ebp-0x388], edx
  ││││││╎   0x00b3346b      mov   ecx, dword [eax*4+0x2027ed0]
  ││││││╎   0x00b33472      mov   dword [ebp-0x384], edi
  ││││││╎   0x00b33478      mov   dword [ebp-0x394], ecx
  ││││││╎   0x00b3347e      test  ecx, ecx
  ────────< 0x00b33480      jz    0xb334ad
  ││││││╎   0x00b33482      mov   eax, dword [ecx]
  ││││││╎   0x00b33484      lea   edx, dword [ebp-0x388]
  ││││││╎   0x00b3348a      push  edx
  ││││││╎   0x00b3348b      lea   edx, dword [ebp-0x390]
  ││││││╎   0x00b33491      push  edx
  ││││││╎   0x00b33492      call  dword [eax+0x3c]                     ; 60
  ││││││╎   0x00b33495      mov   edi, dword [ebp-0x384]
  ││││││╎   0x00b3349b      mov   edx, dword [ebp-0x38c]
  ││││││╎   0x00b334a1      mov   esi, dword [ebp-0x390]
  ││││││╎   0x00b334a7      mov   ecx, dword [ebp-0x394]
  ────────> 0x00b334ad      xor   eax, eax
  ││││││╎   0x00b334af      mov   byte [ebp-0x04], 0x15                ; 21
  ││││││╎   0x00b334b3      test  ecx, ecx
  ────────< 0x00b334b5      jz    0xb334d8
  ││││││╎   0x00b334b7      mov   ecx, dword [ebp-0x364]
  ││││││╎   0x00b334bd      movzx ecx, word [ecx]
  ││││││╎   0x00b334c0      cmp   ecx, edx
  ────────< 0x00b334c2      jnb   0xb334d8
  ││││││╎   0x00b334c4      mov   eax, dword [esi+ecx*4]
  ││││││╎   0x00b334c7      test  eax, eax
  ────────< 0x00b334c9      jnz   0xb334dc
  ││││││╎   0x00b334cb      cmp   ecx, edi
  ────────< 0x00b334cd      jnb   0xb334d8
  ││││││╎   0x00b334cf      mov   eax, dword [ebp-0x388]
  ││││││╎   0x00b334d5      mov   eax, dword [eax+ecx*4]
  ────────> 0x00b334d8      test  eax, eax
  ────────< 0x00b334da      jz    0xb33508
  ────────> 0x00b334dc      push  dword [ebp-0x364]
  ││││││╎   0x00b334e2      lea   eax, dword [ebp-0x4c]
  ││││││╎   0x00b334e5      push  eax
  ││││││╎   0x00b334e6      call  0xc7e350
  ││││││╎   0x00b334eb      add   esp, 0x08
  ││││││╎   0x00b334ee      movss xmm0, dword [eax]
  ││││││╎   0x00b334f2      movss dword [ebp-0x28], xmm0
  ││││││╎   0x00b334f7      movss xmm0, dword [eax+0x04]
  ││││││╎   0x00b334fc      movss dword [ebp-0x24], xmm0
  ││││││╎   0x00b33501      movss xmm0, dword [eax+0x08]
  ────────< 0x00b33506      jmp   0xb33535
  ────────> 0x00b33508      mov   ecx, dword [ebp-0x364]
  ││││││╎   0x00b3350e      call  0xb014f0
  ││││││╎   0x00b33513      mov   eax, dword [eax+0xe4]
  ││││││╎   0x00b33519      and   eax, 0xfffffffc                      ; 4294967292
  ││││││╎   0x00b3351c      movss xmm0, dword [eax+0x30]
  ││││││╎   0x00b33521      movss dword [ebp-0x28], xmm0
  ││││││╎   0x00b33526      movss xmm0, dword [eax+0x34]
  ││││││╎   0x00b3352b      movss dword [ebp-0x24], xmm0
  ││││││╎   0x00b33530      movss xmm0, dword [eax+0x38]
  ────────> 0x00b33535      mov   ecx, dword [0x201e2dc]               ; [0x201e2dc:4]=0
  ││││││╎   0x00b3353b      lea   eax, dword [ebp-0x28]
  ││││││╎   0x00b3353e      push  0x00
  ││││││╎   0x00b33540      push  eax
  ││││││╎   0x00b33541      movss dword [ebp-0x20], xmm0
  ││││││╎   0x00b33546      call  0xbb1d20
  ││││││╎   0x00b3354b      fstp  dword [ebp-0x20]
  ││││││╎   0x00b3354e      mov   byte [ebp-0x04], 0x0b                ; 0xb ; 11
  ────────< 0x00b33552      jmp   0xb33564
  ────────> 0x00b33554      movq  xmm0, qword [ebp-0x1c]
  ││││││╎   0x00b33559      mov   eax, dword [ebp-0x14]
  ││││││╎   0x00b3355c      movq  qword [ebp-0x28], xmm0
  ││││││╎   0x00b33561      mov   dword [ebp-0x20], eax
  ────────> 0x00b33564      mov   eax, dword [0x201f660]               ; [0x201f660:4]=0
  ││││││╎   0x00b33569      xor   edx, edx
  ││││││╎   0x00b3356b      xor   esi, esi
  ││││││╎   0x00b3356d      xor   edi, edi
  ││││││╎   0x00b3356f      mov   eax, dword [eax+0x1f8]
  ││││││╎   0x00b33575      mov   dword [ebp-0x458], esi
  ││││││╎   0x00b3357b      mov   dword [ebp-0x454], edx
  ││││││╎   0x00b33581      mov   dword [ebp-0x450], edx
  ││││││╎   0x00b33587      mov   ecx, dword [eax*4+0x2027ed0]
  ││││││╎   0x00b3358e      mov   dword [ebp-0x44c], edi
  ││││││╎   0x00b33594      mov   dword [ebp-0x45c], ecx
  ││││││╎   0x00b3359a      test  ecx, ecx
  ────────< 0x00b3359c      jz    0xb335c9
  ││││││╎   0x00b3359e      mov   eax, dword [ecx]
  ││││││╎   0x00b335a0      lea   edx, dword [ebp-0x450]
  ││││││╎   0x00b335a6      push  edx
  ││││││╎   0x00b335a7      lea   edx, dword [ebp-0x458]
  ││││││╎   0x00b335ad      push  edx
  ││││││╎   0x00b335ae      call  dword [eax+0x3c]                     ; 60
  ││││││╎   0x00b335b1      mov   edi, dword [ebp-0x44c]
  ││││││╎   0x00b335b7      mov   edx, dword [ebp-0x454]
  ││││││╎   0x00b335bd      mov   esi, dword [ebp-0x458]
  ││││││╎   0x00b335c3      mov   ecx, dword [ebp-0x45c]
  ────────> 0x00b335c9      mov   byte [ebp-0x04], 0x17                ; 23
  ││││││╎   0x00b335cd      test  ecx, ecx
  ────────< 0x00b335cf      jz    0xb335f4
  ││││││╎   0x00b335d1      mov   eax, dword [ebp-0x36c]
  ││││││╎   0x00b335d7      xor   ecx, ecx
  ││││││╎   0x00b335d9      movzx eax, word [eax]
  ││││││╎   0x00b335dc      cmp   eax, edx
  ────────< 0x00b335de      jnb   0xb335f4
  ││││││╎   0x00b335e0      mov   ecx, dword [esi+eax*4]
  ││││││╎   0x00b335e3      test  ecx, ecx
  ────────< 0x00b335e5      jnz   0xb335f4
  ││││││╎   0x00b335e7      cmp   eax, edi
  ────────< 0x00b335e9      jnb   0xb335f4
  ││││││╎   0x00b335eb      mov   ecx, dword [ebp-0x450]
  ││││││╎   0x00b335f1      mov   ecx, dword [ecx+eax*4]
  ────────> 0x00b335f4      lea   eax, dword [ebp-0x414]
  ││││││╎   0x00b335fa      push  eax
  ││││││╎   0x00b335fb      call  0xdb1640
  ││││││╎   0x00b33600      lea   eax, dword [ebp-0x414]
  ││││││╎   0x00b33606      mov   byte [ebp-0x04], 0x18                ; 24
  ││││││╎   0x00b3360a      push  eax
  ││││││╎   0x00b3360b      call  0xcc0720
  ││││││╎   0x00b33610      add   esp, 0x04
  ││││││╎   0x00b33613      test  al, al
  ────────< 0x00b33615      jz    0xb33896
  ││││││╎   0x00b3361b      lea   eax, dword [ebp-0x414]
  ││││││╎   0x00b33621      push  eax
  ││││││╎   0x00b33622      call  0xcc0380
  ││││││╎   0x00b33627      add   esp, 0x04
  ││││││╎   0x00b3362a      test  al, al
  ────────< 0x00b3362c      jz    0xb33896
  ││││││╎   0x00b33632      lea   eax, dword [ebp-0x514]
  ││││││╎   0x00b33638      push  eax
  ││││││╎   0x00b33639      call  0xb6b5c0
  ││││││╎   0x00b3363e      push  eax
  ││││││╎   0x00b3363f      call  0xb3d280
  ││││││╎   0x00b33644      mov   ecx, eax
  ││││││╎   0x00b33646      add   esp, 0x08
  ││││││╎   0x00b33649      lea   edx, dword [ecx+0x14]
  ││││││╎   0x00b3364c      mov   dword [ebp-0x35c], ecx
  ││││││╎   0x00b33652      mov   dword [ebp-0x374], edx
  ││││││╎   0x00b33658      mov   dword [ecx+0x04], 0x24               ; '$'
  ││││││╎                                                              ; [0x24:4]=-1 ; 36
  ││││││╎   0x00b3365f      mov   esi, dword [ebp-0x3ec]
  ││││││╎   0x00b33665      mov   eax, dword [ebp-0x3e8]
  ││││││╎   0x00b3366b      mov   dword [ebp-0x418], esi
  ││││││╎   0x00b33671      lea   edi, dword [esi+eax*4]
  ││││││╎   0x00b33674      mov   eax, dword [ecx+0x20]
  ││││││╎   0x00b33677      mov   dword [ebp-0x368], edi
  ││││││╎   0x00b3367d      mov   edi, dword [edx+0x0c]
  ││││││╎   0x00b33680      sub   eax, edi
  ││││││╎   0x00b33682      sar   eax, 0x02
  ││││││╎   0x00b33685      mov   dword [ebp-0x380], eax
  ││││││╎   0x00b3368b      mov   eax, dword [ebp-0x368]
  ││││││╎   0x00b33691      sub   eax, esi
  ││││││╎   0x00b33693      mov   dword [ebp-0x378], edi
  ││││││╎   0x00b33699      sar   eax, 0x02
  ││││││╎   0x00b3369c      mov   dword [ebp-0x360], eax
  ││││││╎   0x00b336a2      test  eax, eax
  ││││││╎   0x00b336a4      mov   eax, dword [ebp-0x380]
  ────────< 0x00b336aa      jz    0xb33829
  ││││││╎   0x00b336b0      mov   edi, dword [ebp-0x360]
  ││││││╎   0x00b336b6      mov   ecx, dword [edx+0x10]
  ││││││╎   0x00b336b9      add   edi, ecx
  ││││││╎   0x00b336bb      mov   dword [ebp-0x37c], edi
  ││││││╎   0x00b336c1      cmp   dword [edx+0x04], edi
  ────────< 0x00b336c4      jnb   0xb336e6
  ││││││╎   0x00b336c6      push  edi
  ││││││╎   0x00b336c7      mov   ecx, edx
  ││││││╎   0x00b336c9      call  0xa65f00
  ││││││╎   0x00b336ce      mov   eax, dword [ebp-0x35c]
  ││││││╎   0x00b336d4      mov   ecx, dword [eax+0x24]
  ││││││╎   0x00b336d7      mov   eax, dword [eax+0x20]
  ││││││╎   0x00b336da      mov   dword [ebp-0x378], eax
  ││││││╎   0x00b336e0      mov   eax, dword [ebp-0x380]
  ────────> 0x00b336e6      mov   edi, dword [ebp-0x378]
  ││││││╎   0x00b336ec      lea   edx, dword [eax*4]
  ││││││╎   0x00b336f3      sub   ecx, eax
  ││││││╎   0x00b336f5      mov   dword [ebp-0x3d4], edx
  ││││││╎   0x00b336fb      mov   eax, dword [ebp-0x378]
  ││││││╎   0x00b33701      add   eax, edx
  ││││││╎   0x00b33703      mov   dword [ebp-0x37c], ecx
  ││││││╎   0x00b33709      mov   dword [ebp-0x364], eax
  ││││││╎   0x00b3370f      mov   eax, dword [ebp-0x380]
  ││││││╎   0x00b33715      add   eax, dword [ebp-0x360]
  ││││││╎   0x00b3371b      lea   eax, dword [edi+eax*4]
  ││││││╎   0x00b3371e      mov   edi, dword [ebp-0x368]
  ││││││╎   0x00b33724      mov   dword [ebp-0x378], eax
  ││││││╎   0x00b3372a      cmp   ecx, 0x04                            ; 4
  ────────< 0x00b3372d      jb    0xb337aa
  ││││││╎   0x00b33733      mov   eax, dword [ebp-0x364]
  ││││││╎   0x00b33739      mov   esi, ecx
  ││││││╎   0x00b3373b      mov   edx, dword [ebp-0x378]
  ││││││╎   0x00b33741      lea   edi, dword [esi-0x03]
  ││││││╎   0x00b33744      lea   ecx, dword [esi-0x01]
  ││││││╎   0x00b33747      lea   edi, dword [eax+edi*4]
  ││││││╎   0x00b3374a      sub   eax, edx
  ││││││╎   0x00b3374c      lea   ecx, dword [edx+ecx*4]
  ││││││╎   0x00b3374f      mov   dword [ebp-0x37c], eax
  ││││││╎   0x00b33755      mov   edx, esi
  ││││││╎   0x00b33757      shr   edx, 0x02
  ││││││╎   0x00b3375a      nop   word [eax+eax*1], ax
  ────────> 0x00b33760      mov   eax, dword [eax+ecx*1]
  ││││││╎   0x00b33763      lea   ecx, dword [ecx-0x10]
  ││││││╎   0x00b33766      mov   dword [ecx+0x10], eax
  ││││││╎   0x00b33769      lea   edi, dword [edi-0x10]
  ││││││╎   0x00b3376c      mov   eax, dword [edi+0x14]
  ││││││╎   0x00b3376f      sub   esi, 0x04
  ││││││╎   0x00b33772      mov   dword [ecx+0x0c], eax
  ││││││╎   0x00b33775      mov   eax, dword [edi+0x10]
  ││││││╎   0x00b33778      mov   dword [ecx+0x08], eax
  ││││││╎   0x00b3377b      mov   eax, dword [edi+0x0c]
  ││││││╎   0x00b3377e      mov   dword [ecx+0x04], eax
  ││││││╎   0x00b33781      mov   eax, dword [ebp-0x37c]
  ││││││╎   0x00b33787      sub   edx, 0x01
  ────────< 0x00b3378a      jnz   0xb33760
  ││││││╎   0x00b3378c      mov   edi, dword [ebp-0x368]
  ││││││╎   0x00b33792      mov   edx, dword [ebp-0x3d4]
  ││││││╎   0x00b33798      mov   dword [ebp-0x37c], esi
  ││││││╎   0x00b3379e      mov   esi, dword [ebp-0x418]
  ││││││╎   0x00b337a4      mov   ecx, dword [ebp-0x37c]
  ────────> 0x00b337aa      cmp   ecx, 0x02                            ; 2
  ────────< 0x00b337ad      jb    0xb337da
  ││││││╎   0x00b337af      mov   edi, dword [ebp-0x378]
  ││││││╎   0x00b337b5      mov   eax, dword [ebp-0x364]
  ││││││╎   0x00b337bb      mov   eax, dword [eax+ecx*4-0x04]
  ││││││╎   0x00b337bf      mov   dword [edi+ecx*4-0x04], eax
  ││││││╎   0x00b337c3      mov   eax, dword [ebp-0x364]
  ││││││╎   0x00b337c9      mov   eax, dword [eax+ecx*4-0x08]
  ││││││╎   0x00b337cd      mov   dword [edi+ecx*4-0x08], eax
  ││││││╎   0x00b337d1      sub   ecx, 0x02
  ││││││╎   0x00b337d4      mov   edi, dword [ebp-0x368]
  ────────> 0x00b337da      cmp   ecx, 0x01                            ; 1
  ────────< 0x00b337dd      jb    0xb337ef
  ││││││╎   0x00b337df      mov   eax, dword [ebp-0x364]
  ││││││╎   0x00b337e5      mov   ecx, dword [ebp-0x378]
  ││││││╎   0x00b337eb      mov   eax, dword [eax]
  ││││││╎   0x00b337ed      mov   dword [ecx], eax
  ────────> 0x00b337ef      mov   eax, dword [ebp-0x374]
  ││││││╎   0x00b337f5      mov   ecx, dword [ebp-0x360]
  ││││││╎   0x00b337fb      add   dword [eax+0x10], ecx
  ││││││╎   0x00b337fe      cmp   esi, edi
  ────────< 0x00b33800      jz    0xb33823
  ────────> 0x00b33802      mov   ecx, dword [eax+0x0c]
  ││││││╎   0x00b33805      lea   edx, dword [edx+0x04]
  ││││││╎   0x00b33808      mov   dword [ecx+edx*1-0x04], 0xffffffff   ; [0xffffffff:4]=-1 ; -1
  ││││││╎   0x00b33810      mov   eax, dword [esi]
  ││││││╎   0x00b33812      add   esi, 0x04
  ││││││╎   0x00b33815      mov   dword [ecx+edx*1-0x04], eax
  ││││││╎   0x00b33819      mov   eax, dword [ebp-0x374]
  ││││││╎   0x00b3381f      cmp   esi, edi
  ────────< 0x00b33821      jnz   0xb33802
  ────────> 0x00b33823      mov   ecx, dword [ebp-0x35c]
  ────────> 0x00b33829      movss xmm0, dword [ebp-0x28]
  ││││││╎   0x00b3382e      movss dword [ecx+0x28], xmm0
  ││││││╎   0x00b33833      movss xmm0, dword [ebp-0x24]
  ││││││╎   0x00b33838      mov   esi, dword [ebp-0x35c]
  ││││││╎   0x00b3383e      movss dword [ecx+0x2c], xmm0
  ││││││╎   0x00b33843      movss xmm0, dword [ebp-0x20]
  ││││││╎   0x00b33848      movss dword [ecx+0x30], xmm0
  ││││││╎   0x00b3384d      movss xmm0, dword [ebp-0x1c]
  ││││││╎   0x00b33852      movss xmm1, dword [ebp-0x18]
  ││││││╎   0x00b33857      movss xmm2, dword [ebp-0x14]
  ││││││╎   0x00b3385c      movss dword [ecx+0x34], xmm0
  ││││││╎   0x00b33861      movss dword [ecx+0x38], xmm1
  ││││││╎   0x00b33866      movss dword [ecx+0x3c], xmm2
  ││││││╎   0x00b3386b      movups xmm0, xmmword [ebp-0x4fc]
  ││││││╎   0x00b33872      mov   dword [ebp-0x380], 0x20              ; 32
  ││││││╎   0x00b3387c      movups xmmword [ecx+0x40], xmm0
  ││││││╎   0x00b33880      movups xmm0, xmmword [ebp-0x4ec]
  ││││││╎   0x00b33887      movups xmmword [ecx+0x50], xmm0
  ││││││╎   0x00b3388b      mov   eax, dword [ebp-0x4dc]
  ││││││╎   0x00b33891      mov   dword [ecx+0x60], eax
  ────────< 0x00b33894      jmp   0xb338cf
  ────────> 0x00b33896      lea   eax, dword [ebp-0x518]
  ││││││╎   0x00b3389c      push  eax
  ││││││╎   0x00b3389d      call  0xb72540
  ││││││╎   0x00b338a2      push  eax
  ││││││╎   0x00b338a3      call  0xb3d280
  ││││││╎   0x00b338a8      add   esp, 0x08
  ││││││╎   0x00b338ab      mov   dword [ebp-0x35c], eax
  ││││││╎   0x00b338b1      lea   ecx, dword [ebp-0x28]
  ││││││╎   0x00b338b4      push  ecx
  ││││││╎   0x00b338b5      mov   ecx, eax
  ││││││╎   0x00b338b7      call  0xd01d10
  ││││││╎   0x00b338bc      mov   esi, dword [ebp-0x35c]
  ││││││╎   0x00b338c2      mov   al, byte [ebp-0x4f6]
  ││││││╎   0x00b338c8      mov   byte [esi+0x10], al
  ││││││╎   0x00b338cb      mov   byte [esi+0x11], 0x01
  ────────> 0x00b338cf      lea   ecx, dword [ebp-0x414]
  ││││││╎   0x00b338d5      call  0x4dc500
  ││││││╎   0x00b338da      mov   dword [ebp-0x45c], 0x00
  ││││││╎   0x00b338e4      mov   byte [ebp-0x04], 0x0b                ; 0xb ; 11
  ────────< 0x00b338e8      jmp   0xb33bf3
  ││││││╎   0x00b338ed      mov   eax, dword [0x201f660]               ; [0x201f660:4]=0
  ││││││╎   0x00b338f2      xor   edx, edx
  ││││││╎   0x00b338f4      xor   esi, esi
  ││││││╎   0x00b338f6      xor   edi, edi
  ││││││╎   0x00b338f8      mov   eax, dword [eax+0x1f8]
  ││││││╎   0x00b338fe      mov   dword [ebp-0x46c], esi
  ││││││╎   0x00b33904      mov   dword [ebp-0x468], edx
  ││││││╎   0x00b3390a      mov   dword [ebp-0x464], edx
  ││││││╎   0x00b33910      mov   ecx, dword [eax*4+0x2027ed0]
  ││││││╎   0x00b33917      mov   dword [ebp-0x460], edi
  ││││││╎   0x00b3391d      mov   dword [ebp-0x470], ecx
  ││││││╎   0x00b33923      test  ecx, ecx
  ────────< 0x00b33925      jz    0xb33952
  ││││││╎   0x00b33927      mov   eax, dword [ecx]
  ││││││╎   0x00b33929      lea   edx, dword [ebp-0x464]
  ││││││╎   0x00b3392f      push  edx
  ││││││╎   0x00b33930      lea   edx, dword [ebp-0x46c]
  ││││││╎   0x00b33936      push  edx
  ││││││╎   0x00b33937      call  dword [eax+0x3c]                     ; 60
  ││││││╎   0x00b3393a      mov   edi, dword [ebp-0x460]
  ││││││╎   0x00b33940      mov   edx, dword [ebp-0x468]
  ││││││╎   0x00b33946      mov   esi, dword [ebp-0x46c]
  ││││││╎   0x00b3394c      mov   ecx, dword [ebp-0x470]
  ────────> 0x00b33952      mov   byte [ebp-0x04], 0x1b                ; 27
  ││││││╎   0x00b33956      test  ecx, ecx
  ────────< 0x00b33958      jz    0xb3397d
  ││││││╎   0x00b3395a      mov   eax, dword [ebp-0x36c]
  ││││││╎   0x00b33960      xor   ecx, ecx
  ││││││╎   0x00b33962      movzx eax, word [eax]
  ││││││╎   0x00b33965      cmp   eax, edx
  ────────< 0x00b33967      jnb   0xb3397d
  ││││││╎   0x00b33969      mov   ecx, dword [esi+eax*4]
  ││││││╎   0x00b3396c      test  ecx, ecx
  ────────< 0x00b3396e      jnz   0xb3397d
  ││││││╎   0x00b33970      cmp   eax, edi
  ────────< 0x00b33972      jnb   0xb3397d
  ││││││╎   0x00b33974      mov   ecx, dword [ebp-0x464]
  ││││││╎   0x00b3397a      mov   ecx, dword [ecx+eax*4]
  ────────> 0x00b3397d      lea   eax, dword [ebp-0x420]
  ││││││╎   0x00b33983      push  eax
  ││││││╎   0x00b33984      call  0xdb1640
  ││││││╎   0x00b33989      lea   eax, dword [ebp-0x420]
  ││││││╎   0x00b3398f      mov   byte [ebp-0x04], 0x1c                ; 28
  ││││││╎   0x00b33993      push  eax
  ││││││╎   0x00b33994      call  0xcc0380
  ││││││╎   0x00b33999      add   esp, 0x04
  ││││││╎   0x00b3399c      test  al, al
  ────────< 0x00b3399e      jz    0xb33bd0
  ││││││╎   0x00b339a4      lea   eax, dword [ebp-0x484]
  ││││││╎   0x00b339aa      push  eax
  ││││││╎   0x00b339ab      call  0xb6b5c0
  ││││││╎   0x00b339b0      push  eax
  ││││││╎   0x00b339b1      call  0xb3d280
  ││││││╎   0x00b339b6      mov   ecx, eax
  ││││││╎   0x00b339b8      add   esp, 0x08
  ││││││╎   0x00b339bb      mov   eax, dword [ebp+0x0c]
  ││││││╎   0x00b339be      mov   dword [ebp-0x35c], ecx
  ││││││╎   0x00b339c4      mov   dword [ecx+0x04], 0x22               ; '"'
  ││││││╎                                                              ; [0x22:4]=-1 ; 34
  ││││││╎   0x00b339cb      lea   edx, dword [ecx+0x14]
  ││││││╎   0x00b339ce      mov   esi, dword [eax]
  ││││││╎   0x00b339d0      mov   eax, dword [eax+0x04]
  ││││││╎   0x00b339d3      mov   dword [ebp-0x380], edx
  ││││││╎   0x00b339d9      mov   dword [ebp-0x418], esi
  ││││││╎   0x00b339df      lea   edi, dword [esi+eax*4]
  ││││││╎   0x00b339e2      mov   eax, dword [ecx+0x20]
  ││││││╎   0x00b339e5      mov   ecx, dword [edx+0x0c]
  ││││││╎   0x00b339e8      sub   eax, ecx
  ││││││╎   0x00b339ea      mov   dword [ebp-0x360], ecx
  ││││││╎   0x00b339f0      mov   ecx, edi
  ││││││╎   0x00b339f2      sub   ecx, esi
  ││││││╎   0x00b339f4      sar   eax, 0x02
  ││││││╎   0x00b339f7      sar   ecx, 0x02
  ││││││╎   0x00b339fa      mov   dword [ebp-0x364], edi
  ││││││╎   0x00b33a00      mov   dword [ebp-0x374], eax
  ││││││╎   0x00b33a06      mov   dword [ebp-0x378], ecx
  ││││││╎   0x00b33a0c      test  ecx, ecx
  ────────< 0x00b33a0e      jz    0xb33b83
  ││││││╎   0x00b33a14      mov   edi, dword [ebp-0x378]
  ││││││╎   0x00b33a1a      mov   ecx, dword [edx+0x10]
  ││││││╎   0x00b33a1d      add   edi, ecx
  ││││││╎   0x00b33a1f      mov   dword [ebp-0x3d4], edi
  ││││││╎   0x00b33a25      cmp   dword [edx+0x04], edi
  ────────< 0x00b33a28      jnb   0xb33a4a
  ││││││╎   0x00b33a2a      push  edi
  ││││││╎   0x00b33a2b      mov   ecx, edx
  ││││││╎   0x00b33a2d      call  0xa65f00
  ││││││╎   0x00b33a32      mov   eax, dword [ebp-0x35c]
  ││││││╎   0x00b33a38      mov   ecx, dword [eax+0x24]
  ││││││╎   0x00b33a3b      mov   eax, dword [eax+0x20]
  ││││││╎   0x00b33a3e      mov   dword [ebp-0x360], eax
  ││││││╎   0x00b33a44      mov   eax, dword [ebp-0x374]
  ────────> 0x00b33a4a      mov   edi, dword [ebp-0x360]
  ││││││╎   0x00b33a50      lea   edx, dword [eax*4]
  ││││││╎   0x00b33a57      sub   ecx, eax
  ││││││╎   0x00b33a59      mov   dword [ebp-0x398], edx
  ││││││╎   0x00b33a5f      mov   eax, dword [ebp-0x360]
  ││││││╎   0x00b33a65      add   eax, edx
  ││││││╎   0x00b33a67      mov   dword [ebp-0x37c], ecx
  ││││││╎   0x00b33a6d      mov   dword [ebp-0x368], eax
  ││││││╎   0x00b33a73      mov   eax, dword [ebp-0x374]
  ││││││╎   0x00b33a79      add   eax, dword [ebp-0x378]
  ││││││╎   0x00b33a7f      lea   eax, dword [edi+eax*4]
  ││││││╎   0x00b33a82      mov   edi, dword [ebp-0x364]
  ││││││╎   0x00b33a88      mov   dword [ebp-0x360], eax
  ││││││╎   0x00b33a8e      cmp   ecx, 0x04                            ; 4
  ────────< 0x00b33a91      jb    0xb33b0a
  ││││││╎   0x00b33a97      mov   eax, dword [ebp-0x368]
  ││││││╎   0x00b33a9d      mov   esi, ecx
  ││││││╎   0x00b33a9f      mov   edx, dword [ebp-0x360]
  ││││││╎   0x00b33aa5      lea   edi, dword [esi-0x03]
  ││││││╎   0x00b33aa8      lea   ecx, dword [esi-0x01]
  ││││││╎   0x00b33aab      lea   edi, dword [eax+edi*4]
  ││││││╎   0x00b33aae      sub   eax, edx
  ││││││╎   0x00b33ab0      lea   ecx, dword [edx+ecx*4]
  ││││││╎   0x00b33ab3      mov   dword [ebp-0x3d4], eax
  ││││││╎   0x00b33ab9      mov   edx, esi
  ││││││╎   0x00b33abb      shr   edx, 0x02
  ││││││╎   0x00b33abe      nop
  ────────> 0x00b33ac0      mov   eax, dword [eax+ecx*1]
  ││││││╎   0x00b33ac3      lea   ecx, dword [ecx-0x10]
  ││││││╎   0x00b33ac6      mov   dword [ecx+0x10], eax
  ││││││╎   0x00b33ac9      lea   edi, dword [edi-0x10]
  ││││││╎   0x00b33acc      mov   eax, dword [edi+0x14]
  ││││││╎   0x00b33acf      sub   esi, 0x04
  ││││││╎   0x00b33ad2      mov   dword [ecx+0x0c], eax
  ││││││╎   0x00b33ad5      mov   eax, dword [edi+0x10]
  ││││││╎   0x00b33ad8      mov   dword [ecx+0x08], eax
  ││││││╎   0x00b33adb      mov   eax, dword [edi+0x0c]
  ││││││╎   0x00b33ade      mov   dword [ecx+0x04], eax
  ││││││╎   0x00b33ae1      mov   eax, dword [ebp-0x3d4]
  ││││││╎   0x00b33ae7      sub   edx, 0x01
  ────────< 0x00b33aea      jnz   0xb33ac0
  ││││││╎   0x00b33aec      mov   edi, dword [ebp-0x364]
  ││││││╎   0x00b33af2      mov   edx, dword [ebp-0x398]
  ││││││╎   0x00b33af8      mov   dword [ebp-0x37c], esi
  ││││││╎   0x00b33afe      mov   esi, dword [ebp-0x418]
  ││││││╎   0x00b33b04      mov   ecx, dword [ebp-0x37c]
  ────────> 0x00b33b0a      cmp   ecx, 0x02                            ; 2
  ────────< 0x00b33b0d      jb    0xb33b3a
  ││││││╎   0x00b33b0f      mov   edi, dword [ebp-0x360]
  ││││││╎   0x00b33b15      mov   eax, dword [ebp-0x368]
  ││││││╎   0x00b33b1b      mov   eax, dword [eax+ecx*4-0x04]
  ││││││╎   0x00b33b1f      mov   dword [edi+ecx*4-0x04], eax
  ││││││╎   0x00b33b23      mov   eax, dword [ebp-0x368]
  ││││││╎   0x00b33b29      mov   eax, dword [eax+ecx*4-0x08]
  ││││││╎   0x00b33b2d      mov   dword [edi+ecx*4-0x08], eax
  ││││││╎   0x00b33b31      sub   ecx, 0x02
  ││││││╎   0x00b33b34      mov   edi, dword [ebp-0x364]
  ────────> 0x00b33b3a      cmp   ecx, 0x01                            ; 1
  ────────< 0x00b33b3d      jb    0xb33b4f
  ││││││╎   0x00b33b3f      mov   eax, dword [ebp-0x368]
  ││││││╎   0x00b33b45      mov   ecx, dword [ebp-0x360]
  ││││││╎   0x00b33b4b      mov   eax, dword [eax]
  ││││││╎   0x00b33b4d      mov   dword [ecx], eax
  ────────> 0x00b33b4f      mov   eax, dword [ebp-0x380]
  ││││││╎   0x00b33b55      mov   ecx, dword [ebp-0x378]
  ││││││╎   0x00b33b5b      add   dword [eax+0x10], ecx
  ││││││╎   0x00b33b5e      cmp   esi, edi
  ────────< 0x00b33b60      jz    0xb33b83
  ────────> 0x00b33b62      mov   ecx, dword [eax+0x0c]
  ││││││╎   0x00b33b65      lea   edx, dword [edx+0x04]
  ││││││╎   0x00b33b68      mov   dword [ecx+edx*1-0x04], 0xffffffff   ; [0xffffffff:4]=-1 ; -1
  ││││││╎   0x00b33b70      mov   eax, dword [esi]
  ││││││╎   0x00b33b72      add   esi, 0x04
  ││││││╎   0x00b33b75      mov   dword [ecx+edx*1-0x04], eax
  ││││││╎   0x00b33b79      mov   eax, dword [ebp-0x380]
  ││││││╎   0x00b33b7f      cmp   esi, edi
  ────────< 0x00b33b81      jnz   0xb33b62
  ────────> 0x00b33b83      mov   esi, dword [ebp-0x35c]
  ││││││╎   0x00b33b89      movss xmm0, dword [ebp-0x1c]
  ││││││╎   0x00b33b8e      movss xmm1, dword [ebp-0x18]
  ││││││╎   0x00b33b93      movss xmm2, dword [ebp-0x14]
  ││││││╎   0x00b33b98      movss dword [esi+0x34], xmm0
  ││││││╎   0x00b33b9d      movss dword [esi+0x38], xmm1
  ││││││╎   0x00b33ba2      movss dword [esi+0x3c], xmm2
  ││││││╎   0x00b33ba7      movups xmm0, xmmword [ebp-0x4fc]
  ││││││╎   0x00b33bae      mov   dword [ebp-0x380], 0x20              ; 32
  ││││││╎   0x00b33bb8      movups xmmword [esi+0x40], xmm0
  ││││││╎   0x00b33bbc      movups xmm0, xmmword [ebp-0x4ec]
  ││││││╎   0x00b33bc3      movups xmmword [esi+0x50], xmm0
  ││││││╎   0x00b33bc7      mov   eax, dword [ebp-0x4dc]
  ││││││╎   0x00b33bcd      mov   dword [esi+0x60], eax
  ────────> 0x00b33bd0      lea   ecx, dword [ebp-0x420]
  ││││││╎   0x00b33bd6      call  0x4dc500
  ││││││╎   0x00b33bdb      mov   esi, dword [ebp-0x35c]
  ││││││╎   0x00b33be1      mov   dword [ebp-0x470], 0x00
  ││││││╎   0x00b33beb      mov   byte [ebp-0x04], 0x0b                ; 0xb ; 11
  ────────< 0x00b33bef      jmp   0xb33bf3
  └───────> 0x00b33bf1      xor   esi, esi
  ────────> 0x00b33bf3      push  dword [ebp-0x478]
   │││││╎   0x00b33bf9      mov   eax, dword [ebp-0x3ec]
   │││││╎   0x00b33bff      push  dword [ebp-0x40c]
   │││││╎   0x00b33c05      mov   edi, dword [ebp-0x36c]
   │││││╎   0x00b33c0b      mov   dword [ebp-0x4a8], eax
   │││││╎   0x00b33c11      mov   eax, dword [ebp-0x3e8]
   │││││╎   0x00b33c17      mov   dword [ebp-0x4a4], eax
   │││││╎   0x00b33c1d      mov   eax, dword [ebp-0x370]
   │││││╎   0x00b33c23      push  esi
   │││││╎   0x00b33c24      mov   dword [ebp-0x4ac], eax
   │││││╎   0x00b33c2a      lea   eax, dword [ebp-0x4fc]
   │││││╎   0x00b33c30      push  eax
   │││││╎   0x00b33c31      push  dword [ebp-0x410]
   │││││╎   0x00b33c37      lea   eax, dword [ebp-0x1c]
   │││││╎   0x00b33c3a      mov   dword [ebp-0x4b0], edi
   │││││╎   0x00b33c40      push  eax
   │││││╎   0x00b33c41      lea   eax, dword [ebp-0x4a8]
   │││││╎   0x00b33c47      push  eax
   │││││╎   0x00b33c48      lea   eax, dword [ebp-0x4b0]
   │││││╎   0x00b33c4e      push  eax
   │││││╎   0x00b33c4f      push  ecx
   │││││╎   0x00b33c50      push  esp
   │││││╎   0x00b33c51      call  0xb70410
   │││││╎   0x00b33c56      add   esp, 0x04
   │││││╎   0x00b33c59      lea   eax, dword [ebp-0x3c8]
   │││││╎   0x00b33c5f      push  dword [ebp-0x380]
   │││││╎   0x00b33c65      push  eax
   │││││╎   0x00b33c66      call  0xabd410
   │││││╎   0x00b33c6b      add   esp, 0x2c
   │││││╎   0x00b33c6e      mov   edx, dword [ebp-0x3dc]
   │││││╎   0x00b33c74      mov   byte [ebp-0x04], 0x1f                ; 31
   │││││╎   0x00b33c78      test  edx, edx
  ┌───────< 0x00b33c7a      jz    0xb33caa
  ││││││╎   0x00b33c7c      mov   esi, dword [edx+0x10]
  ││││││╎   0x00b33c7f      cmp   esi, dword [edx+0x04]
  ────────< 0x00b33c82      jnz   0xb33c91
  ││││││╎   0x00b33c84      mov   ecx, edx
  ││││││╎   0x00b33c86      call  0x7aab00
  ││││││╎   0x00b33c8b      mov   edx, dword [ebp-0x3dc]
  ────────> 0x00b33c91      mov   ecx, dword [edx+0x0c]
  ││││││╎   0x00b33c94      mov   dword [ecx+esi*4], 0xffffffff        ; [0xffffffff:4]=-1 ; -1
  ││││││╎   0x00b33c9b      mov   eax, dword [ebp-0x3c8]
  ││││││╎   0x00b33ca1      mov   dword [ecx+esi*4], eax
  ││││││╎   0x00b33ca4      lea   eax, dword [esi+0x01]
  ││││││╎   0x00b33ca7      mov   dword [edx+0x10], eax
  └───────> 0x00b33caa      mov   eax, dword [ebp-0x380]
   │││││╎   0x00b33cb0      cmp   eax, 0x04                            ; 4
  ┌───────< 0x00b33cb3      jz    0xb33ce6
  ││││││╎   0x00b33cb5      cmp   eax, 0x10                            ; 16
  ────────< 0x00b33cb8      jz    0xb33ce6
  ││││││╎   0x00b33cba      cmp   eax, 0x1b                            ; 27
  ────────< 0x00b33cbd      jz    0xb33ce6
  ││││││╎   0x00b33cbf      cmp   eax, 0x1c                            ; 28
  ────────< 0x00b33cc2      jz    0xb33ce6
  ││││││╎   0x00b33cc4      cmp   eax, 0x17                            ; 23
  ────────< 0x00b33cc7      jz    0xb33ce6
  ││││││╎   0x00b33cc9      cmp   eax, 0x16                            ; 22
  ────────< 0x00b33ccc      jz    0xb33ce6
  ││││││╎   0x00b33cce      cmp   eax, 0x15                            ; 21
  ────────< 0x00b33cd1      jz    0xb33ce6
  ││││││╎   0x00b33cd3      cmp   eax, 0x1d                            ; 29
  ────────< 0x00b33cd6      jz    0xb33ce6
  ││││││╎   0x00b33cd8      cmp   eax, 0x1e                            ; 30
  ────────< 0x00b33cdb      jz    0xb33ce6
  ││││││╎   0x00b33cdd      cmp   eax, 0x1f                            ; 31
  ────────< 0x00b33ce0      jz    0xb33ce6
  ││││││╎   0x00b33ce2      xor   al, al
  ────────< 0x00b33ce4      jmp   0xb33ce8
  └───────> 0x00b33ce6      mov   al, 0x01
  ────────> 0x00b33ce8      test  al, al
  ┌───────< 0x00b33cea      jz    0xb33da8
  ││││││╎   0x00b33cf0      mov   eax, dword [0x201f660]               ; [0x201f660:4]=0
  ││││││╎   0x00b33cf5      xor   edx, edx
  ││││││╎   0x00b33cf7      xor   esi, esi
  ││││││╎   0x00b33cf9      xor   edi, edi
  ││││││╎   0x00b33cfb      mov   eax, dword [eax+0x88]
  ││││││╎   0x00b33d01      mov   dword [ebp-0x390], esi
  ││││││╎   0x00b33d07      mov   dword [ebp-0x38c], edx
  ││││││╎   0x00b33d0d      mov   dword [ebp-0x388], edx
  ││││││╎   0x00b33d13      mov   ecx, dword [eax*4+0x20282d4]
  ││││││╎   0x00b33d1a      mov   dword [ebp-0x384], edi
  ││││││╎   0x00b33d20      mov   dword [ebp-0x394], ecx
  ││││││╎   0x00b33d26      test  ecx, ecx
  ────────< 0x00b33d28      jz    0xb33d55
  ││││││╎   0x00b33d2a      mov   eax, dword [ecx]
  ││││││╎   0x00b33d2c      lea   edx, dword [ebp-0x388]
  ││││││╎   0x00b33d32      push  edx
  ││││││╎   0x00b33d33      lea   edx, dword [ebp-0x390]
  ││││││╎   0x00b33d39      push  edx
  ││││││╎   0x00b33d3a      call  dword [eax+0x40]                     ; 64
  ││││││╎   0x00b33d3d      mov   edi, dword [ebp-0x384]
  ││││││╎   0x00b33d43      mov   edx, dword [ebp-0x38c]
  ││││││╎   0x00b33d49      mov   esi, dword [ebp-0x390]
  ││││││╎   0x00b33d4f      mov   ecx, dword [ebp-0x394]
  ────────> 0x00b33d55      mov   byte [ebp-0x04], 0x20                ; 32
  ││││││╎   0x00b33d59      test  ecx, ecx
  ────────< 0x00b33d5b      jz    0xb33d7e
  ││││││╎   0x00b33d5d      movzx eax, word [ebp-0x3c8]
  ││││││╎   0x00b33d64      xor   ecx, ecx
  ││││││╎   0x00b33d66      cmp   eax, edx
  ────────< 0x00b33d68      jnb   0xb33d7e
  ││││││╎   0x00b33d6a      mov   ecx, dword [esi+eax*4]
  ││││││╎   0x00b33d6d      test  ecx, ecx
  ────────< 0x00b33d6f      jnz   0xb33d7e
  ││││││╎   0x00b33d71      cmp   eax, edi
  ────────< 0x00b33d73      jnb   0xb33d7e
  ││││││╎   0x00b33d75      mov   ecx, dword [ebp-0x388]
  ││││││╎   0x00b33d7b      mov   ecx, dword [ecx+eax*4]
  ────────> 0x00b33d7e      mov   eax, dword [ebp-0x424]
  ││││││╎   0x00b33d84      push  ecx
  ││││││╎   0x00b33d85      movss xmm0, dword [eax+0x0c]
  ││││││╎   0x00b33d8a      mov   al, byte [eax+0x08]
  ││││││╎   0x00b33d8d      movss dword [esp], xmm0
  ││││││╎   0x00b33d92      push  eax
  ││││││╎   0x00b33d93      push  dword [ebp-0x3e0]
  ││││││╎   0x00b33d99      call  0xabcf60
  ││││││╎   0x00b33d9e      mov   edi, dword [ebp-0x36c]
  ││││││╎   0x00b33da4      mov   byte [ebp-0x04], 0x1f                ; 31
  └───────> 0x00b33da8      cmp   byte [ebp-0x3e0], 0x00
   │││││╎   0x00b33daf      push  0x00
  ┌───────< 0x00b33db1      jz    0xb33dce
  ││││││╎   0x00b33db3      lea   eax, dword [ebp-0x3c8]
  ││││││╎   0x00b33db9      push  eax
  ││││││╎   0x00b33dba      lea   eax, dword [ebp-0x4b8]
  ││││││╎   0x00b33dc0      push  eax
  ││││││╎   0x00b33dc1      call  0xb37b70
  ││││││╎   0x00b33dc6      add   esp, 0x0c
  ────────< 0x00b33dc9      jmp   0xb33e93
  └───────> 0x00b33dce      mov   eax, dword [ebp-0x370]
   │││││╎   0x00b33dd4      mov   dword [ebp-0x48c], eax
   │││││╎   0x00b33dda      lea   eax, dword [ebp-0x3c8]
   │││││╎   0x00b33de0      push  eax
   │││││╎   0x00b33de1      lea   eax, dword [ebp-0x490]
   │││││╎   0x00b33de7      mov   dword [ebp-0x490], edi
   │││││╎   0x00b33ded      push  eax
   │││││╎   0x00b33dee      call  0xabc210
   │││││╎   0x00b33df3      mov   eax, dword [0x201f660]               ; [0x201f660:4]=0
   │││││╎   0x00b33df8      lea   ecx, dword [ebp-0x394]
   │││││╎   0x00b33dfe      add   esp, 0x0c
   │││││╎   0x00b33e01      mov   eax, dword [eax+0x88]
   │││││╎   0x00b33e07      push  0x01                                 ; 1
   │││││╎   0x00b33e09      mov   dword [ebp-0x398], eax
   │││││╎   0x00b33e0f      lea   eax, dword [ebp-0x398]
   │││││╎   0x00b33e15      push  0x01                                 ; 1
   │││││╎   0x00b33e17      push  eax
   │││││╎   0x00b33e18      call  0xa6aaf0
   │││││╎   0x00b33e1d      xor   ecx, ecx
   │││││╎   0x00b33e1f      mov   byte [ebp-0x04], 0x22                ; '"' ; 34
   │││││╎   0x00b33e23      mov   dword [ebp-0x36c], ecx
   │││││╎   0x00b33e29      cmp   dword [ebp-0x394], ecx
  ┌───────< 0x00b33e2f      jz    0xb33e6a
  ││││││╎   0x00b33e31      movzx edx, word [ebp-0x3c8]
  ││││││╎   0x00b33e38      cmp   edx, dword [ebp-0x38c]
  ────────< 0x00b33e3e      jnb   0xb33e6a
  ││││││╎   0x00b33e40      mov   eax, dword [ebp-0x390]
  ││││││╎   0x00b33e46      mov   ecx, dword [eax+edx*4]
  ││││││╎   0x00b33e49      mov   dword [ebp-0x36c], ecx
  ││││││╎   0x00b33e4f      test  ecx, ecx
  ────────< 0x00b33e51      jnz   0xb33e6a
  ││││││╎   0x00b33e53      cmp   edx, dword [ebp-0x384]
  ────────< 0x00b33e59      jnb   0xb33e6a
  ││││││╎   0x00b33e5b      mov   eax, dword [ebp-0x388]
  ││││││╎   0x00b33e61      mov   ecx, dword [eax+edx*4]
  ││││││╎   0x00b33e64      mov   dword [ebp-0x36c], ecx
  └───────> 0x00b33e6a      mov   esi, dword [ecx+0xa0]
   │││││╎   0x00b33e70      mov   eax, dword [ecx+0xa4]
   │││││╎   0x00b33e76      lea   edi, dword [esi+eax*4]
   │││││╎   0x00b33e79      cmp   esi, edi
  ┌───────< 0x00b33e7b      jz    0xb33e93
  ││││││╎   0x00b33e7d      nop   dword [eax], eax
  ────────> 0x00b33e80      push  esi
  ││││││╎   0x00b33e81      call  0xabbb40
  ││││││╎   0x00b33e86      mov   ecx, dword [ebp-0x36c]
  ││││││╎   0x00b33e8c      add   esi, 0x04
  ││││││╎   0x00b33e8f      cmp   esi, edi
  ────────< 0x00b33e91      jnz   0xb33e80
  └───────> 0x00b33e93      lea   ecx, dword [ebp-0x3c8]
   │││││╎   0x00b33e99      call  0x4dc500
   └──────> 0x00b33e9e      lea   ecx, dword [ebp-0x3b0]
    ││││╎   0x00b33ea4      call  0xb37f50
    ││││╎   0x00b33ea9      mov   ecx, dword [ebp-0x3b0]
    ││││╎   0x00b33eaf      mov   byte [ebp-0x04], 0x24                ; '$' ; 36
    ││││╎   0x00b33eb3      test  ecx, ecx
   ┌──────< 0x00b33eb5      jz    0xb33ec3
   │││││╎   0x00b33eb7      lea   eax, dword [ebp-0x3b0]
   │││││╎   0x00b33ebd      push  eax
   │││││╎   0x00b33ebe      call  0x517c70
   └└─────> 0x00b33ec3      lea   ecx, dword [ebp-0x3c4]
     │││╎   0x00b33ec9      call  0xb37f50
     │││╎   0x00b33ece      mov   ecx, dword [ebp-0x3c4]
     │││╎   0x00b33ed4      mov   byte [ebp-0x04], 0x25                ; '%' ; 37
     │││╎   0x00b33ed8      test  ecx, ecx
    ┌─────< 0x00b33eda      jz    0xb3419d
    ││││╎   0x00b33ee0      lea   eax, dword [ebp-0x3c4]
    ││││╎   0x00b33ee6      push  eax
    ││││╎   0x00b33ee7      call  0x517c70
   ┌──────< 0x00b33eec      jmp   0xb3419d
   ││└────> 0x00b33ef1      cmp   ecx, 0x0a                            ; 0xa ; 10
   ││┌────< 0x00b33ef4      jnz   0xb341ad
   │││││╎   0x00b33efa      mov   eax, dword [0x201f660]               ; [0x201f660:4]=0
   │││││╎   0x00b33eff      mov   eax, dword [eax+0xc8]
   │││││╎   0x00b33f05      mov   dword [ebp-0x3c0], 0x00
   │││││╎   0x00b33f0f      mov   dword [ebp-0x3bc], 0x00
   │││││╎   0x00b33f19      mov   dword [ebp-0x3b8], 0x00
   │││││╎   0x00b33f23      mov   ecx, dword [eax*4+0x2027ed0]
   │││││╎   0x00b33f2a      mov   dword [ebp-0x3b4], 0x00
   │││││╎   0x00b33f34      mov   dword [ebp-0x3c4], ecx
   │││││╎   0x00b33f3a      test  ecx, ecx
  ┌───────< 0x00b33f3c      jz    0xb33f51
  ││││││╎   0x00b33f3e      mov   eax, dword [ecx]
  ││││││╎   0x00b33f40      lea   edx, dword [ebp-0x3b8]
  ││││││╎   0x00b33f46      push  edx
  ││││││╎   0x00b33f47      lea   edx, dword [ebp-0x3c0]
  ││││││╎   0x00b33f4d      push  edx
  ││││││╎   0x00b33f4e      call  dword [eax+0x40]                     ; 64
  └───────> 0x00b33f51      xor   ecx, ecx
   │││││╎   0x00b33f53      xor   edi, edi
   │││││╎   0x00b33f55      xor   esi, esi
   │││││╎   0x00b33f57      mov   dword [ebp-0x3ac], ecx
   │││││╎   0x00b33f5d      mov   dword [ebp-0x3a4], edi
   │││││╎   0x00b33f63      mov   dword [ebp-0x3a0], esi
   │││││╎   0x00b33f69      mov   eax, dword [ebp-0x35c]
   │││││╎   0x00b33f6f      mov   byte [ebp-0x04], 0x27                ; ''' ; 39
   │││││╎   0x00b33f73      mov   edx, dword [eax+0x10]
   │││││╎   0x00b33f76      mov   dword [ebp-0x374], edx
   │││││╎   0x00b33f7c      test  edx, edx
  ┌───────< 0x00b33f7e      jz    0xb33fc4
  ││││││╎   0x00b33f80      call  0x52b950
  ││││││╎   0x00b33f85      push  dword [0x1d6c084]
  ││││││╎   0x00b33f8b      mov   ecx, dword [ebp-0x374]
  ││││││╎   0x00b33f91      shl   ecx, 0x02
  ││││││╎   0x00b33f94      push  ecx
  ││││││╎   0x00b33f95      mov   ecx, eax
  ││││││╎   0x00b33f97      call  0x52b5a0
  ││││││╎   0x00b33f9c      push  esi
  ││││││╎   0x00b33f9d      mov   edi, eax
  ││││││╎   0x00b33f9f      push  esi
  ││││││╎   0x00b33fa0      push  edi
  ││││││╎   0x00b33fa1      call  0x4df350
  ││││││╎   0x00b33fa6      mov   eax, dword [ebp-0x35c]
  ││││││╎   0x00b33fac      add   esp, 0x0c
  ││││││╎   0x00b33faf      mov   ecx, dword [ebp-0x374]
  ││││││╎   0x00b33fb5      mov   dword [ebp-0x3a4], edi
  ││││││╎   0x00b33fbb      mov   dword [ebp-0x3ac], ecx
  ││││││╎   0x00b33fc1      mov   edx, dword [eax+0x10]
  └───────> 0x00b33fc4      mov   dword [ebp-0x370], 0x00
   │││││╎   0x00b33fce      test  edx, edx
  ┌───────< 0x00b33fd0      jz    0xb3404b
  ││││││╎   0x00b33fd6      xor   edx, edx
  ││││││╎   0x00b33fd8      xor   esi, esi
  ││││││╎   0x00b33fda      mov   dword [ebp-0x360], edx
  ────────> 0x00b33fe0      mov   eax, dword [eax+0x0c]
  ││││││╎   0x00b33fe3      add   eax, edx
  ││││││╎   0x00b33fe5      mov   dword [ebp-0x398], eax
  ││││││╎   0x00b33feb      cmp   esi, ecx
  ────────< 0x00b33fed      jnz   0xb34012
  ││││││╎   0x00b33fef      lea   ecx, dword [ebp-0x3b0]
  ││││││╎   0x00b33ff5      call  0x7aab00
  ││││││╎   0x00b33ffa      mov   edi, dword [ebp-0x3a4]
  ││││││╎   0x00b34000      mov   ecx, dword [ebp-0x3ac]
  ││││││╎   0x00b34006      mov   eax, dword [ebp-0x398]
  ││││││╎   0x00b3400c      mov   edx, dword [ebp-0x360]
  ────────> 0x00b34012      inc   dword [ebp-0x370]
  ││││││╎   0x00b34018      add   edx, 0x14                            ; 20
  ││││││╎   0x00b3401b      mov   dword [edi+esi*4], 0xffffffff        ; [0xffffffff:4]=-1 ; -1
  ││││││╎   0x00b34022      mov   eax, dword [eax]
  ││││││╎   0x00b34024      mov   dword [edi+esi*4], eax
  ││││││╎   0x00b34027      inc   esi
  ││││││╎   0x00b34028      mov   eax, dword [ebp-0x35c]
  ││││││╎   0x00b3402e      mov   dword [ebp-0x360], edx
  ││││││╎   0x00b34034      mov   edx, dword [ebp-0x370]
  ││││││╎   0x00b3403a      mov   dword [ebp-0x3a0], esi
  ││││││╎   0x00b34040      cmp   edx, dword [eax+0x10]
  ││││││╎   0x00b34043      mov   edx, dword [ebp-0x360]
  ────────< 0x00b34049      jb    0xb33fe0
  └───────> 0x00b3404b      lea   ecx, dword [ebp-0x428]
   │││││╎   0x00b34051      call  0x4f6c50
   │││││╎   0x00b34056      push  0x00
   │││││╎   0x00b34058      push  eax
   │││││╎   0x00b34059      lea   eax, dword [ebp-0x4c0]
   │││││╎   0x00b3405f      mov   byte [ebp-0x04], 0x28                ; '(' ; 40
   │││││╎   0x00b34063      push  eax
   │││││╎   0x00b34064      mov   dword [ebp-0x4c0], edi
   │││││╎   0x00b3406a      mov   dword [ebp-0x4bc], esi
   │││││╎   0x00b34070      call  0xabc210
   │││││╎   0x00b34075      add   esp, 0x0c
   │││││╎   0x00b34078      lea   ecx, dword [ebp-0x428]
   │││││╎   0x00b3407e      call  0x4dc500
   │││││╎   0x00b34083      mov   eax, dword [ebp-0x35c]
   │││││╎   0x00b34089      mov   dword [ebp-0x370], 0x00
   │││││╎   0x00b34093      cmp   dword [eax+0x10], 0x00
  ┌───────< 0x00b34097      jbe   0xb34192
  ││││││╎   0x00b3409d      xor   ecx, ecx
  ││││││╎   0x00b3409f      mov   dword [ebp-0x360], ecx
  ││││││╎   0x00b340a5      nop   word [eax+eax*1], ax
  ────────> 0x00b340b0      mov   eax, dword [eax+0x0c]
  ││││││╎   0x00b340b3      add   eax, ecx
  ││││││╎   0x00b340b5      mov   dword [ebp-0x374], 0xffffffff        ; -1
  ││││││╎   0x00b340bf      mov   ecx, dword [eax]
  ││││││╎   0x00b340c1      mov   dword [ebp-0x374], ecx
  ││││││╎   0x00b340c7      mov   dword [ebp-0x3d0], 0xffffffff        ; -1
  ││││││╎   0x00b340d1      mov   eax, dword [eax+0x04]
  ││││││╎   0x00b340d4      mov   dword [ebp-0x3d0], eax
  ││││││╎   0x00b340da      cmp   dword [ebp-0x3c4], 0x00
  ││││││╎   0x00b340e1      mov   byte [ebp-0x04], 0x2a                ; '*' ; 42
  ││││││╎   0x00b340e5      mov   dword [ebp-0x36c], 0x00
  ────────< 0x00b340ef      jz    0xb34126
  ││││││╎   0x00b340f1      movzx ecx, cx
  ││││││╎   0x00b340f4      cmp   ecx, dword [ebp-0x3bc]
  ────────< 0x00b340fa      jnb   0xb34126
  ││││││╎   0x00b340fc      mov   eax, dword [ebp-0x3c0]
  ││││││╎   0x00b34102      mov   eax, dword [eax+ecx*4]
  ││││││╎   0x00b34105      mov   dword [ebp-0x36c], eax
  ││││││╎   0x00b3410b      test  eax, eax
  ────────< 0x00b3410d      jnz   0xb34126
  ││││││╎   0x00b3410f      cmp   ecx, dword [ebp-0x3b4]
  ────────< 0x00b34115      jnb   0xb34126
  ││││││╎   0x00b34117      mov   eax, dword [ebp-0x3b8]
  ││││││╎   0x00b3411d      mov   eax, dword [eax+ecx*4]
  ││││││╎   0x00b34120      mov   dword [ebp-0x36c], eax
  ────────> 0x00b34126      lea   eax, dword [ebp-0x47c]
  ││││││╎   0x00b3412c      push  eax
  ││││││╎   0x00b3412d      call  0xb72d90
  ││││││╎   0x00b34132      add   esp, 0x04
  ││││││╎   0x00b34135      mov   edi, eax
  ││││││╎   0x00b34137      push  0x00
  ││││││╎   0x00b34139      call  0x512430
  ││││││╎   0x00b3413e      push  ecx
  ││││││╎   0x00b3413f      mov   ecx, dword [ebp-0x36c]
  ││││││╎   0x00b34145      mov   esi, esp
  ││││││╎   0x00b34147      push  edi
  ││││││╎   0x00b34148      mov   edx, dword [eax]
  ││││││╎   0x00b3414a      mov   dword [esi], edx
  ││││││╎   0x00b3414c      call  0xb723f0
  ││││││╎   0x00b34151      lea   ecx, dword [ebp-0x3d0]
  ││││││╎   0x00b34157      call  0x4dc500
  ││││││╎   0x00b3415c      lea   ecx, dword [ebp-0x374]
  ││││││╎   0x00b34162      call  0x4dc500
  ││││││╎   0x00b34167      mov   edx, dword [ebp-0x370]
  ││││││╎   0x00b3416d      mov   eax, dword [ebp-0x35c]
  ││││││╎   0x00b34173      inc   edx
  ││││││╎   0x00b34174      mov   ecx, dword [ebp-0x360]
  ││││││╎   0x00b3417a      add   ecx, 0x14                            ; 20
  ││││││╎   0x00b3417d      mov   dword [ebp-0x370], edx
  ││││││╎   0x00b34183      mov   dword [ebp-0x360], ecx
  ││││││╎   0x00b34189      cmp   edx, dword [eax+0x10]
  ────────< 0x00b3418c      jb    0xb340b0
  └───────> 0x00b34192      lea   ecx, dword [ebp-0x3b0]
   │││││╎   0x00b34198      call  0x975700
   └└─────> 0x00b3419d      mov   edi, dword [ebp-0x39c]
     │││╎   0x00b341a3      mov   ecx, dword [ebp-0x3cc]
     │││╎   0x00b341a9      mov   byte [ebp-0x04], 0x06
     └└└──> 0x00b341ad      inc   ecx
        ╎   0x00b341ae      mov   dword [ebp-0x3cc], ecx
        ╎   0x00b341b4      cmp   ecx, 0x27                            ; ''' ; 39
        └─< 0x00b341b7      jb    0xb32a00
            0x00b341bd      push  0xb2b380
            0x00b341c2      push  0x27                                 ; ''' ; 39
            0x00b341c4      push  0x14                                 ; 20
            0x00b341c6      lea   eax, dword [ebp-0x358]
            0x00b341cc      mov   byte [ebp-0x04], 0x2c                ; ',' ; 44
            0x00b341d0      push  eax
            0x00b341d1      call  0x1807072
            0x00b341d6      lea   ecx, dword [ebp-0x52c]
            0x00b341dc      call  0x975700
            0x00b341e1      lea   ecx, dword [ebp-0x3f4]
            0x00b341e7      call  0xa9e320
            0x00b341ec      lea   ecx, dword [ebp-0x43c]
            0x00b341f2      call  0x975700
            0x00b341f7      lea   esp, dword [ebp-0x538]
            0x00b341fd      mov   ecx, dword [ebp-0x0c]
            0x00b34200      mov   dword fs:[0x0], ecx
            0x00b34207      pop   ecx
            0x00b34208      pop   edi
            0x00b34209      pop   esi
            0x00b3420a      mov   ecx, dword [ebp-0x10]
            0x00b3420d      xor   ecx, ebp
            0x00b3420f      call  0x18075f6
            0x00b34214      mov   esp, ebp
            0x00b34216      pop   ebp
            0x00b34217      ret
            0x00b34218      sbb   dh, byte [ebx+esi*4]
            0x00b3421b      add   cl, bl
            0x00b3421d      xor   esi, dword [ebx-0x4ccdd700]
            0x00b34223      add   byte [ebx], dh
            0x00b34225      xor   esi, dword [ebx-0x4ccd4d00]
            0x00b3422b      add   ch, ch
            0x00b3422d      cmp   byte [ebx-0x4ccce900], dh
            0x00b34233      add   byte [eax+0xb332], ch
            0x00b34239      pop   es
            0x00b3423a      pop   es
            0x00b3423b      pop   es
            0x00b3423c      add   dword [edi], eax
            0x00b3423e      pop   es
            0x00b3423f      pop   es
            0x00b34240      pop   es
            0x00b34241      pop   es
            0x00b34242      pop   es
            0x00b34243      pop   es
            0x00b34244      add   al, byte [ebx]
            0x00b34246      add   al, 0x05
            0x00b34248      push  es
            0x00b34249      add   ah, cl
            0x00b3424b      int3
            0x00b3424c      int3
            0x00b3424d      int3
            0x00b3424e      int3
            0x00b3424f      int3
            0x00b34250      mov   edx, dword [esp+0x04]
            0x00b34254      test  edx, edx
        ┌─< 0x00b34256      jz    0xb34268
        │   0x00b34258      mov   ecx, dword [0x201e2dc]               ; [0x201e2dc:4]=0
        │   0x00b3425e      push  dword [esp+0x08]
        │   0x00b34262      push  edx
        │   0x00b34263      mov   eax, dword [ecx]
        │   0x00b34265      call  dword [eax+0x28]                     ; 40
        └─> 0x00b34268      ret
            0x00b34269      int3
            0x00b3426a      int3
            0x00b3426b      int3
            0x00b3426c      int3
            0x00b3426d      int3
            0x00b3426e      int3
            0x00b3426f      int3
            0x00b34270      push  ebp
            0x00b34271      mov   ebp, esp
            0x00b34273      push  0xffffffff                           ; 255
            0x00b34275      push  0x1869928
            0x00b3427a      mov   eax, dword fs:[0x0]
            0x00b34280      push  eax
            0x00b34281      sub   esp, 0x10
            0x00b34284      push  ebx
            0x00b34285      push  esi
            0x00b34286      push  edi
            0x00b34287      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00b3428c      xor   eax, ebp
            0x00b3428e      push  eax
            0x00b3428f      invalid
