            0x00c09820      push  ebp
            0x00c09821      mov   ebp, esp
            0x00c09823      push  0xffffffff                           ; 255
            0x00c09825      push  0x1876328
            0x00c0982a      mov   eax, dword fs:[0x0]
            0x00c09830      push  eax
            0x00c09831      sub   esp, 0x60
            0x00c09834      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00c09839      xor   eax, ebp
            0x00c0983b      mov   dword [ebp-0x10], eax
            0x00c0983e      push  ebx
            0x00c0983f      push  esi
            0x00c09840      push  edi
            0x00c09841      push  eax
            0x00c09842      lea   eax, dword [ebp-0x0c]
            0x00c09845      mov   dword fs:[0x0], eax
            0x00c0984b      mov   edi, ecx
            0x00c0984d      mov   dword [ebp-0x64], edi
            0x00c09850      mov   eax, dword [ebp+0x08]
            0x00c09853      xor   edx, edx
            0x00c09855      mov   ebx, dword [edi+0x08]
            0x00c09858      xor   esi, esi
            0x00c0985a      mov   dword [ebp-0x4c], eax
            0x00c0985d      mov   eax, dword [ebp+0x0c]
            0x00c09860      mov   dword [ebp-0x50], eax
            0x00c09863      mov   eax, dword [0x201f660]               ; [0x201f660:4]=0
            0x00c09868      mov   eax, dword [eax+0xd8]
            0x00c0986e      mov   dword [ebp-0x58], edx
            0x00c09871      mov   dword [ebp-0x54], esi
            0x00c09874      mov   ecx, dword [eax*4+0x20286d8]
            0x00c0987b      mov   dword [ebp-0x5c], ecx
            0x00c0987e      test  ecx, ecx
        ,=< 0x00c09880      jz    0xc09895
        |   0x00c09882      mov   eax, dword [ecx]
        |   0x00c09884      lea   edx, dword [ebp-0x58]
        |   0x00c09887      push  esi
        |   0x00c09888      push  edx
        |   0x00c09889      call  dword [eax+0x40]                     ; 64
        |   0x00c0988c      mov   esi, dword [ebp-0x54]
        |   0x00c0988f      mov   edx, dword [ebp-0x58]
        |   0x00c09892      mov   ecx, dword [ebp-0x5c]
        `-> 0x00c09895      mov   dword [ebp-0x04], 0x00
            0x00c0989c      test  ecx, ecx
        ,=< 0x00c0989e      jz    0xc098ad
        |   0x00c098a0      movzx eax, word [ebx+0x20]
        |   0x00c098a4      cmp   eax, esi
       ,==< 0x00c098a6      jnb   0xc098ad
       ||   0x00c098a8      mov   ecx, dword [edx+eax*4]
      ,===< 0x00c098ab      jmp   0xc098af
      |``-> 0x00c098ad      xor   ecx, ecx
      `---> 0x00c098af      mov   eax, dword [0x203cfa8]               ; [0x203cfa8:4]=0
            0x00c098b4      mov   dword [ebp-0x38], ecx
            0x00c098b7      mov   eax, dword [eax+0x1c]
            0x00c098ba      push  eax
            0x00c098bb      mov   dword [ebp-0x48], eax
            0x00c098be      call  0xb7d600
            0x00c098c3      cmp   byte [edi+0x95], 0x00
            0x00c098ca      mov   ebx, eax
        ,=< 0x00c098cc      jnz   0xc098ee
        |   0x00c098ce      mov   ecx, edi
        |   0x00c098d0      call  0xc0ce90
        |   0x00c098d5      mov   ecx, ebx
        |   0x00c098d7      mov   esi, eax
        |   0x00c098d9      call  0xb47e90
        |   0x00c098de      cmp   eax, esi
       ,==< 0x00c098e0      jnl   0xc098ee
       ||   0x00c098e2      mov   ecx, edi
       ||   0x00c098e4      call  0xc0ec40
      ,===< 0x00c098e9      jmp   0xc09bdd
      |``-> 0x00c098ee      mov   eax, dword [0x201f660]               ; [0x201f660:4]=0
      |     0x00c098f3      xor   edx, edx
      |     0x00c098f5      xor   esi, esi
      |     0x00c098f7      mov   eax, dword [eax+0x210]
      |     0x00c098fd      mov   dword [ebp-0x18], edx
      |     0x00c09900      mov   dword [ebp-0x14], esi
      |     0x00c09903      mov   ecx, dword [eax*4+0x20286d8]
      |     0x00c0990a      mov   dword [ebp-0x1c], ecx
      |     0x00c0990d      test  ecx, ecx
      | ,=< 0x00c0990f      jz    0xc09924
      | |   0x00c09911      mov   eax, dword [ecx]
      | |   0x00c09913      lea   edx, dword [ebp-0x18]
      | |   0x00c09916      push  esi
      | |   0x00c09917      push  edx
      | |   0x00c09918      call  dword [eax+0x3c]                     ; 60
      | |   0x00c0991b      mov   esi, dword [ebp-0x14]
      | |   0x00c0991e      mov   edx, dword [ebp-0x18]
      | |   0x00c09921      mov   ecx, dword [ebp-0x1c]
      | `-> 0x00c09924      mov   eax, dword [edi+0x08]
      |     0x00c09927      mov   byte [ebp-0x04], 0x02
      |     0x00c0992b      test  ecx, ecx
      | ,=< 0x00c0992d      jz    0xc0998e
      | |   0x00c0992f      movzx eax, word [eax+0x20]
      | |   0x00c09933      cmp   eax, esi
      |,==< 0x00c09935      jnb   0xc0998e
      |||   0x00c09937      mov   ecx, dword [edx+eax*4]
      |||   0x00c0993a      mov   dword [ebp-0x3c], ecx
      |||   0x00c0993d      test  ecx, ecx
     ,====< 0x00c0993f      jz    0xc0998e
     ||||   0x00c09941      xor   eax, eax
     ||||   0x00c09943      xor   esi, esi
     ||||   0x00c09945      cmp   dword [edi+0x70], eax
    ,=====< 0x00c09948      jz    0xc0996b
    |||||   0x00c0994a      lea   edx, dword [esi-0x10]
    |||||   0x00c0994d      lea   ebx, dword [edi+0x84]
   .------> 0x00c09953      mov   ecx, ebx
   :|||||   0x00c09955      cmp   eax, 0x04                            ; 4
  ,=======< 0x00c09958      jb    0xc0995c
  |:|||||   0x00c0995a      mov   ecx, dword [ebx]
  `-------> 0x00c0995c      add   esi, dword [ecx+edx*1]
   :|||||   0x00c0995f      inc   eax
   :|||||   0x00c09960      add   edx, 0x04
   :|||||   0x00c09963      cmp   eax, dword [edi+0x70]
   `======< 0x00c09966      jnz   0xc09953
    |||||   0x00c09968      mov   ecx, dword [ebp-0x3c]
    `-----> 0x00c0996b      cmp   byte [edi+0x96], 0x00
    ,=====< 0x00c09972      jz    0xc0998e
    |||||   0x00c09974      push  esi
    |||||   0x00c09975      lea   eax, dword [edi+0x0c]
    |||||   0x00c09978      push  eax
    |||||   0x00c09979      call  0xbf29f0
    |||||   0x00c0997e      test  al, al
   ,======< 0x00c09980      jnz   0xc0998e
   ||||||   0x00c09982      mov   ecx, edi
   ||||||   0x00c09984      call  0xc0ec40
  ,=======< 0x00c09989      jmp   0xc09bdd
  |```-``-> 0x00c0998e      cmp   dword [edi+0x90], 0x02
  |   |     0x00c09995      mov   bl, 0x01
  |   |     0x00c09997      mov   byte [ebp-0x04], 0x00
  |   |     0x00c0999b      mov   byte [ebp-0x31], bl
  |   | ,=< 0x00c0999e      jnz   0xc09a62
  |   | |   0x00c099a4      mov   eax, dword [edi+0x70]
  |   | |   0x00c099a7      xor   esi, esi
  |   | |   0x00c099a9      mov   edx, dword [0x201e2d8]               ; [0x201e2d8:4]=0
  |   | |   0x00c099af      mov   dword [ebp-0x44], edx
  |   | |   0x00c099b2      mov   dword [ebp-0x68], eax
  |   | |   0x00c099b5      test  eax, eax
  |   |,==< 0x00c099b7      jz    0xc09a62
  |   |||   0x00c099bd      mov   dword [ebp-0x1c], 0x7f800000
  |   |||   0x00c099c4      mov   dword [ebp-0x18], 0x7f800000
  |   |||   0x00c099cb      mov   dword [ebp-0x14], 0x7f800000
  |   |||   0x00c099d2      mov   dword [ebp-0x3c], 0xffffffc0         ; 4294967232
  |  .----> 0x00c099d9      mov   ebx, dword [edx+0x38]
  |  :|||   0x00c099dc      lea   ecx, dword [edi+0x0c]
  |  :|||   0x00c099df      call  0xbcf930
  |  :|||   0x00c099e4      push  eax
  |  :|||   0x00c099e5      call  0xcc08a0
  |  :|||   0x00c099ea      add   esp, 0x04
  |  :|||   0x00c099ed      mov   byte [ebp-0x60], al
  |  :|||   0x00c099f0      lea   ecx, dword [edi+0x0c]
  |  :|||   0x00c099f3      call  0xbcf930
  |  :|||   0x00c099f8      mov   edx, dword [edi+0x08]
  |  :|||   0x00c099fb      lea   ecx, dword [edi+0x5c]
  |  :|||   0x00c099fe      add   edx, 0x20                            ; 32
  |  :|||   0x00c09a01      cmp   esi, 0x04                            ; 4
  | ,=====< 0x00c09a04      jb    0xc09a09
  | |:|||   0x00c09a06      mov   ecx, dword [edi+0x5c]
  | `-----> 0x00c09a09      lea   edi, dword [ebp-0x6c]
  |  :|||   0x00c09a0c      push  edi
  |  :|||   0x00c09a0d      push  dword [ebp-0x60]
  |  :|||   0x00c09a10      push  eax
  |  :|||   0x00c09a11      mov   eax, dword [ebp-0x3c]
  |  :|||   0x00c09a14      add   eax, ecx
  |  :|||   0x00c09a16      mov   ecx, ebx
  |  :|||   0x00c09a18      push  edx
  |  :|||   0x00c09a19      push  eax
  |  :|||   0x00c09a1a      lea   eax, dword [ebp-0x28]
  |  :|||   0x00c09a1d      push  eax
  |  :|||   0x00c09a1e      call  0xaa31e0
  |  :|||   0x00c09a23      mov   edi, dword [ebp-0x64]
  |  :|||   0x00c09a26      xor   ecx, ecx
  |  :|||   0x00c09a28      nop   dword [eax+eax*1], eax
  | .-----> 0x00c09a30      movss xmm0, dword [ebp+ecx*1-0x28]
  | ::|||   0x00c09a36      ucomiss xmm0, dword [ebp+ecx*1-0x1c]
  | ::|||   0x00c09a3b      lahf
  | ::|||   0x00c09a3c      test  ah, 0x44                             ; 68
  |,======< 0x00c09a3f      jp    0xc09a4d
  ||::|||   0x00c09a41      add   ecx, 0x04
  ||::|||   0x00c09a44      cmp   ecx, 0x0c                            ; 0xc ; 12
  ||`=====< 0x00c09a47      jb    0xc09a30
  || :|||   0x00c09a49      xor   bl, bl
  ||,=====< 0x00c09a4b      jmp   0xc09a62
  |`------> 0x00c09a4d      add   dword [ebp-0x3c], 0x10               ; [0x10:4]=-1 ; 16
  | |:|||   0x00c09a51      inc   esi
  | |:|||   0x00c09a52      cmp   esi, dword [ebp-0x68]
  |,======< 0x00c09a55      jz    0xc09a5f
  |||:|||   0x00c09a57      mov   edx, dword [ebp-0x44]
  |||`====< 0x00c09a5a      jmp   0xc099d9
  |`------> 0x00c09a5f      mov   bl, byte [ebp-0x31]
  | `--``-> 0x00c09a62      mov   eax, dword [0x201e2d8]               ; [0x201e2d8:4]=0
  |   |     0x00c09a67      mov   esi, dword [edi+0x90]
  |   |     0x00c09a6d      mov   ecx, dword [eax+0x38]
  |   |     0x00c09a70      call  0xaa3020
  |   |     0x00c09a75      cmp   esi, eax
  |   | ,=< 0x00c09a77      jnz   0xc09ba0
  |   | |   0x00c09a7d      mov   ecx, dword [edi+0x08]
  |   | |   0x00c09a80      call  0xb7ba40
  |   | |   0x00c09a85      test  al, al
  |   |,==< 0x00c09a87      jnz   0xc09ba0
  |   |||   0x00c09a8d      test  bl, bl
  |  ,====< 0x00c09a8f      jz    0xc09ba0
  |  ||||   0x00c09a95      cmp   byte [edi+0x95], al
  | ,=====< 0x00c09a9b      jnz   0xc09ab6
  | |||||   0x00c09a9d      push  0x00
  | |||||   0x00c09a9f      push  0x00
  | |||||   0x00c09aa1      mov   ecx, edi
  | |||||   0x00c09aa3      call  0xc0ce90
  | |||||   0x00c09aa8      mov   ecx, dword [ebp-0x38]
  | |||||   0x00c09aab      neg   eax
  | |||||   0x00c09aad      push  eax
  | |||||   0x00c09aae      push  dword [ebp-0x48]
  | |||||   0x00c09ab1      call  0xb78c30
  | `-----> 0x00c09ab6      push  dword [edi+0x70]
  |  ||||   0x00c09ab9      lea   ecx, dword [ebp-0x30]
  |  ||||   0x00c09abc      mov   dword [ebp-0x2c], 0x00
  |  ||||   0x00c09ac3      mov   dword [ebp-0x24], 0x00
  |  ||||   0x00c09aca      mov   dword [ebp-0x20], 0x00
  |  ||||   0x00c09ad1      call  0xc112e0
  |  ||||   0x00c09ad6      lea   ecx, dword [ebp-0x40]
  |  ||||   0x00c09ad9      mov   byte [ebp-0x04], 0x09
  |  ||||   0x00c09add      call  0x4f6c50
  |  ||||   0x00c09ae2      mov   eax, dword [edi+0x70]
  |  ||||   0x00c09ae5      xor   ebx, ebx
  |  ||||   0x00c09ae7      mov   byte [ebp-0x04], 0x0a
  |  ||||   0x00c09aeb      mov   dword [ebp-0x44], eax
  |  ||||   0x00c09aee      test  eax, eax
  | ,=====< 0x00c09af0      jz    0xc09b8e
  | |||||   0x00c09af6      mov   esi, dword [ebp-0x24]
  | |||||   0x00c09af9      mov   dword [ebp-0x38], esi
  | |||||   0x00c09afc      nop   dword [eax], eax
  |.------> 0x00c09b00      mov   eax, dword [edi]
  |:|||||   0x00c09b02      mov   ecx, edi
  |:|||||   0x00c09b04      call  dword [eax+0x20]                     ; 32
  |:|||||   0x00c09b07      mov   ecx, eax
  |:|||||   0x00c09b09      call  0xba8ff0
  |:|||||   0x00c09b0e      lea   ecx, dword [ebp-0x40]
  |:|||||   0x00c09b11      push  ecx
  |:|||||   0x00c09b12      push  esi
  |:|||||   0x00c09b13      push  ebx
  |:|||||   0x00c09b14      push  eax
  |:|||||   0x00c09b15      mov   ecx, edi
  |:|||||   0x00c09b17      call  0xc0b190
  |:|||||   0x00c09b1c      mov   dword [ebp-0x48], eax
  |:|||||   0x00c09b1f      test  eax, eax
  ========< 0x00c09b21      jz    0xc09b8e
  |:|||||   0x00c09b23      mov   ecx, dword [ebp-0x4c]
  |:|||||   0x00c09b26      test  ecx, ecx
  ========< 0x00c09b28      jz    0xc09b4c
  |:|||||   0x00c09b2a      mov   esi, dword [ecx+0x10]
  |:|||||   0x00c09b2d      cmp   esi, dword [ecx+0x04]
  ========< 0x00c09b30      jnz   0xc09b3a
  |:|||||   0x00c09b32      call  0x58f930
  |:|||||   0x00c09b37      mov   ecx, dword [ebp-0x4c]
  --------> 0x00c09b3a      mov   eax, dword [ecx+0x0c]
  |:|||||   0x00c09b3d      mov   edx, dword [ebp-0x48]
  |:|||||   0x00c09b40      mov   dword [eax+esi*4], edx
  |:|||||   0x00c09b43      lea   eax, dword [esi+0x01]
  |:|||||   0x00c09b46      mov   esi, dword [ebp-0x38]
  |:|||||   0x00c09b49      mov   dword [ecx+0x10], eax
  --------> 0x00c09b4c      mov   edx, dword [ebp-0x50]
  |:|||||   0x00c09b4f      test  edx, edx
  ========< 0x00c09b51      jz    0xc09b7e
  |:|||||   0x00c09b53      mov   esi, dword [edx+0x10]
  |:|||||   0x00c09b56      cmp   esi, dword [edx+0x04]
  ========< 0x00c09b59      jnz   0xc09b65
  |:|||||   0x00c09b5b      mov   ecx, edx
  |:|||||   0x00c09b5d      call  0x7aab00
  |:|||||   0x00c09b62      mov   edx, dword [ebp-0x50]
  --------> 0x00c09b65      mov   ecx, dword [edx+0x0c]
  |:|||||   0x00c09b68      mov   dword [ecx+esi*4], 0xffffffff        ; [0xffffffff:4]=-1 ; -1
  |:|||||   0x00c09b6f      mov   eax, dword [ebp-0x40]
  |:|||||   0x00c09b72      mov   dword [ecx+esi*4], eax
  |:|||||   0x00c09b75      lea   eax, dword [esi+0x01]
  |:|||||   0x00c09b78      mov   esi, dword [ebp-0x38]
  |:|||||   0x00c09b7b      mov   dword [edx+0x10], eax
  --------> 0x00c09b7e      inc   ebx
  |:|||||   0x00c09b7f      add   esi, 0x14                            ; 20
  |:|||||   0x00c09b82      mov   dword [ebp-0x38], esi
  |:|||||   0x00c09b85      cmp   ebx, dword [ebp-0x44]
  |`======< 0x00c09b88      jnz   0xc09b00
  --`-----> 0x00c09b8e      invalid
  |  ||||   0x00c09b8f      dec   ebp
            0x00c095d0      push  ebp
            0x00c095d1      mov   ebp, esp
            0x00c095d3      push  0xffffffff                           ; 255
            0x00c095d5      push  0x18762e0
            0x00c095da      mov   eax, dword fs:[0x0]
            0x00c095e0      push  eax
            0x00c095e1      sub   esp, 0x24
            0x00c095e4      push  ebx
            0x00c095e5      push  esi
            0x00c095e6      push  edi
            0x00c095e7      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00c095ec      xor   eax, ebp
            0x00c095ee      push  eax
            0x00c095ef      lea   eax, dword [ebp-0x0c]
            0x00c095f2      mov   dword fs:[0x0], eax
            0x00c095f8      mov   ebx, ecx
            0x00c095fa      mov   eax, dword [0x201f660]               ; [0x201f660:4]=0
            0x00c095ff      xor   edx, edx
            0x00c09601      mov   edi, dword [ebx+0x08]
            0x00c09604      xor   esi, esi
            0x00c09606      mov   eax, dword [eax+0xd8]
            0x00c0960c      mov   dword [ebp-0x20], edx
            0x00c0960f      mov   dword [ebp-0x1c], esi
            0x00c09612      mov   ecx, dword [eax*4+0x20286d8]
            0x00c09619      mov   dword [ebp-0x24], ecx
            0x00c0961c      test  ecx, ecx
        ,=< 0x00c0961e      jz    0xc09633
        |   0x00c09620      mov   eax, dword [ecx]
        |   0x00c09622      lea   edx, dword [ebp-0x20]
        |   0x00c09625      push  esi
        |   0x00c09626      push  edx
        |   0x00c09627      call  dword [eax+0x40]                     ; 64
        |   0x00c0962a      mov   esi, dword [ebp-0x1c]
        |   0x00c0962d      mov   edx, dword [ebp-0x20]
        |   0x00c09630      mov   ecx, dword [ebp-0x24]
        `-> 0x00c09633      mov   dword [ebp-0x04], 0x00
            0x00c0963a      test  ecx, ecx
        ,=< 0x00c0963c      jz    0xc0964b
        |   0x00c0963e      movzx ecx, word [edi+0x20]
        |   0x00c09642      cmp   ecx, esi
       ,==< 0x00c09644      jnb   0xc0964b
       ||   0x00c09646      mov   ecx, dword [edx+ecx*4]
      ,===< 0x00c09649      jmp   0xc0964d
      |``-> 0x00c0964b      xor   ecx, ecx
      `---> 0x00c0964d      mov   eax, dword [0x203cfa8]               ; [0x203cfa8:4]=0
            0x00c09652      mov   dword [ebp-0x10], ecx
            0x00c09655      mov   eax, dword [eax+0x1c]
            0x00c09658      push  eax
            0x00c09659      mov   dword [ebp-0x18], eax
            0x00c0965c      call  0xb7d600
            0x00c09661      push  dword [0x202731c]
            0x00c09667      lea   ecx, dword [ebx+0x0c]
            0x00c0966a      mov   edi, eax
            0x00c0966c      call  0xbcdcd0
            0x00c09671      mov   ecx, edi
            0x00c09673      mov   esi, eax
            0x00c09675      call  0xb47e90
            0x00c0967a      cmp   eax, esi
        ,=< 0x00c0967c      jnl   0xc09699
        |   0x00c0967e      mov   ecx, ebx
        |   0x00c09680      call  0xc0eb40
        |   0x00c09685      mov   ecx, dword [ebp-0x0c]
        |   0x00c09688      mov   dword fs:[0x0], ecx
        |   0x00c0968f      pop   ecx
        |   0x00c09690      pop   edi
        |   0x00c09691      pop   esi
        |   0x00c09692      pop   ebx
        |   0x00c09693      mov   esp, ebp
        |   0x00c09695      pop   ebp
        |   0x00c09696      ret   0x08
        `-> 0x00c09699      mov   eax, dword [0x201f660]               ; [0x201f660:4]=0
            0x00c0969e      xor   edx, edx
            0x00c096a0      xor   esi, esi
            0x00c096a2      mov   eax, dword [eax+0x210]
            0x00c096a8      mov   dword [ebp-0x2c], edx
            0x00c096ab      mov   dword [ebp-0x28], esi
            0x00c096ae      mov   ecx, dword [eax*4+0x20286d8]
            0x00c096b5      mov   dword [ebp-0x30], ecx
            0x00c096b8      test  ecx, ecx
        ,=< 0x00c096ba      jz    0xc096cf
        |   0x00c096bc      mov   eax, dword [ecx]
        |   0x00c096be      lea   edx, dword [ebp-0x2c]
        |   0x00c096c1      push  esi
        |   0x00c096c2      push  edx
        |   0x00c096c3      call  dword [eax+0x3c]                     ; 60
        |   0x00c096c6      mov   esi, dword [ebp-0x28]
        |   0x00c096c9      mov   edx, dword [ebp-0x2c]
        |   0x00c096cc      mov   ecx, dword [ebp-0x30]
        `-> 0x00c096cf      mov   eax, dword [ebx+0x08]
            0x00c096d2      lea   edi, dword [ebx+0x0c]
            0x00c096d5      mov   byte [ebp-0x04], 0x02
            0x00c096d9      test  ecx, ecx
        ,=< 0x00c096db      jz    0xc09713
        |   0x00c096dd      movzx ecx, word [eax+0x20]
        |   0x00c096e1      cmp   ecx, esi
       ,==< 0x00c096e3      jnb   0xc09713
       ||   0x00c096e5      mov   ecx, dword [edx+ecx*4]
       ||   0x00c096e8      test  ecx, ecx
      ,===< 0x00c096ea      jz    0xc09713
      |||   0x00c096ec      push  0x01                                 ; 1
      |||   0x00c096ee      push  edi
      |||   0x00c096ef      call  0xbf29f0
      |||   0x00c096f4      test  al, al
     ,====< 0x00c096f6      jnz   0xc09713
     ||||   0x00c096f8      mov   ecx, ebx
     ||||   0x00c096fa      call  0xc0eb40
     ||||   0x00c096ff      mov   ecx, dword [ebp-0x0c]
     ||||   0x00c09702      mov   dword fs:[0x0], ecx
     ||||   0x00c09709      pop   ecx
     ||||   0x00c0970a      pop   edi
     ||||   0x00c0970b      pop   esi
     ||||   0x00c0970c      pop   ebx
     ||||   0x00c0970d      mov   esp, ebp
     ||||   0x00c0970f      pop   ebp
     ||||   0x00c09710      ret   0x08
     ````-> 0x00c09713      mov   eax, dword [0x201e2d8]               ; [0x201e2d8:4]=0
            0x00c09718      mov   esi, dword [ebx+0x20]
            0x00c0971b      mov   byte [ebp-0x04], 0x00
            0x00c0971f      mov   ecx, dword [eax+0x38]
            0x00c09722      call  0xaa3020
            0x00c09727      cmp   esi, eax
        ,=< 0x00c09729      jnz   0xc097c7
        |   0x00c0972f      mov   ecx, dword [ebx+0x08]
        |   0x00c09732      call  0xb7ba40
        |   0x00c09737      test  al, al
       ,==< 0x00c09739      jnz   0xc097c7
       ||   0x00c0973f      push  0x00
       ||   0x00c09741      push  0x00
       ||   0x00c09743      push  dword [0x202731c]
       ||   0x00c09749      mov   ecx, edi
       ||   0x00c0974b      call  0xbcdcd0
       ||   0x00c09750      mov   ecx, dword [ebp-0x10]
       ||   0x00c09753      neg   eax
       ||   0x00c09755      push  eax
       ||   0x00c09756      push  dword [ebp-0x18]
       ||   0x00c09759      call  0xb78c30
       ||   0x00c0975e      lea   ecx, dword [ebp-0x14]
       ||   0x00c09761      call  0x4f6c50
       ||   0x00c09766      mov   eax, dword [ebx]
       ||   0x00c09768      mov   ecx, ebx
       ||   0x00c0976a      mov   byte [ebp-0x04], 0x09
       ||   0x00c0976e      call  dword [eax+0x20]                     ; 32
       ||   0x00c09771      mov   ecx, eax
       ||   0x00c09773      call  0xba8ff0
       ||   0x00c09778      lea   ecx, dword [ebp-0x14]
       ||   0x00c0977b      push  ecx
       ||   0x00c0977c      push  eax
       ||   0x00c0977d      mov   ecx, ebx
       ||   0x00c0977f      call  0xc0bec0
       ||   0x00c09784      mov   dword [ebp-0x18], eax
       ||   0x00c09787      test  eax, eax
      ,===< 0x00c09789      jz    0xc097ab
      |||   0x00c0978b      mov   ecx, dword [ebp+0x08]
      |||   0x00c0978e      test  ecx, ecx
     ,====< 0x00c09790      jz    0xc0979b
     ||||   0x00c09792      lea   eax, dword [ebp-0x18]
     ||||   0x00c09795      push  eax
     ||||   0x00c09796      call  0x750590
     `----> 0x00c0979b      mov   ecx, dword [ebp+0x0c]
      |||   0x00c0979e      test  ecx, ecx
     ,====< 0x00c097a0      jz    0xc097ab
     ||||   0x00c097a2      lea   eax, dword [ebp-0x14]
     ||||   0x00c097a5      push  eax
     ||||   0x00c097a6      call  0xac3200
     ``---> 0x00c097ab      lea   ecx, dword [ebp-0x14]
       ||   0x00c097ae      call  0x4dc500
       ||   0x00c097b3      mov   ecx, dword [ebp-0x0c]
       ||   0x00c097b6      mov   dword fs:[0x0], ecx
       ||   0x00c097bd      pop   ecx
       ||   0x00c097be      pop   edi
       ||   0x00c097bf      pop   esi
       ||   0x00c097c0      pop   ebx
       ||   0x00c097c1      mov   esp, ebp
       ||   0x00c097c3      pop   ebp
       ||   0x00c097c4      ret   0x08
       ``-> 0x00c097c7      mov   eax, dword [0x201f660]               ; [0x201f660:4]=0
            0x00c097cc      mov   eax, dword [eax+0xd8]
            0x00c097d2      mov   dword [ebp-0x2c], 0x00
            0x00c097d9      mov   dword [ebp-0x28], 0x00
            0x00c097e0      mov   ecx, dword [eax*4+0x20286d8]
            0x00c097e7      mov   dword [ebp-0x30], ecx
            0x00c097ea      test  ecx, ecx
        ,=< 0x00c097ec      jz    0xc097f9
        |   0x00c097ee      mov   eax, dword [ecx]
        |   0x00c097f0      lea   edx, dword [ebp-0x2c]
        |   0x00c097f3      push  0x00
        |   0x00c097f5      push  edx
        |   0x00c097f6      call  dword [eax+0x40]                     ; 64
        `-> 0x00c097f9      mov   ecx, ebx
            0x00c097fb      mov   byte [ebp-0x04], 0x06
            0x00c097ff      call  0xc0eb40
            0x00c09804      mov   ecx, dword [ebp-0x0c]
            0x00c09807      mov   dword fs:[0x0], ecx
            0x00c0980e      pop   ecx
            0x00c0980f      pop   edi
            0x00c09810      pop   esi
            0x00c09811      pop   ebx
            0x00c09812      mov   esp, ebp
            0x00c09814      pop   ebp
            0x00c09815      ret   0x08
            0x00c09818      int3
            0x00c09819      int3
            0x00c0981a      int3
            0x00c0981b      int3
            0x00c0981c      int3
            0x00c0981d      int3
            0x00c0981e      int3
            0x00c0981f      int3
            0x00ba5520      push  ebp
            0x00ba5521      mov   ebp, esp
            0x00ba5523      push  0xffffffff                           ; 255
            0x00ba5525      push  0x18363d8
            0x00ba552a      mov   eax, dword fs:[0x0]
            0x00ba5530      push  eax
            0x00ba5531      sub   esp, 0x24
            0x00ba5534      push  ebx
            0x00ba5535      push  esi
            0x00ba5536      push  edi
            0x00ba5537      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00ba553c      xor   eax, ebp
            0x00ba553e      push  eax
            0x00ba553f      lea   eax, dword [ebp-0x0c]
            0x00ba5542      mov   dword fs:[0x0], eax
            0x00ba5548      mov   esi, ecx
            0x00ba554a      mov   dword [ebp-0x10], esi
            0x00ba554d      mov   dword [ebp-0x2c], 0x00
            0x00ba5554      mov   dword [ebp-0x24], 0x00
            0x00ba555b      mov   dword [ebp-0x20], 0x00
            0x00ba5562      mov   ecx, dword [ebp+0x08]
            0x00ba5565      lea   edx, dword [ebp-0x30]
            0x00ba5568      push  dword [ebp+0x10]
            0x00ba556b      mov   dword [ebp-0x04], 0x00
            0x00ba5572      push  edx
            0x00ba5573      mov   eax, dword [ecx]
            0x00ba5575      call  dword [eax+0x28]                     ; 40
            0x00ba5578      mov   eax, dword [ebp-0x20]
            0x00ba557b      test  eax, eax
        ,=< 0x00ba557d      jz    0xba5625
        |   0x00ba5583      mov   edi, dword [ebp-0x24]
        |   0x00ba5586      mov   dword [ebp+0x08], edi
        |   0x00ba5589      lea   eax, dword [edi+eax*4]
        |   0x00ba558c      mov   dword [ebp-0x18], eax
        |   0x00ba558f      cmp   edi, eax
       ,==< 0x00ba5591      jz    0xba5615
       ||   0x00ba5597      lea   ebx, dword [esi+0x0c]
       ||   0x00ba559a      mov   dword [ebp-0x1c], ebx
       ||   0x00ba559d      nop   dword [eax], eax
      .---> 0x00ba55a0      mov   esi, dword [ebx+0x10]
      :||   0x00ba55a3      mov   eax, dword [edi]
      :||   0x00ba55a5      mov   dword [ebp+0x10], eax
      :||   0x00ba55a8      cmp   esi, dword [ebx+0x04]
     ,====< 0x00ba55ab      jnz   0xba55b4
     |:||   0x00ba55ad      mov   ecx, ebx
     |:||   0x00ba55af      call  0x58f930
     `----> 0x00ba55b4      mov   eax, dword [ebx+0x0c]
      :||   0x00ba55b7      mov   ecx, dword [ebp+0x10]
      :||   0x00ba55ba      mov   dword [eax+esi*4], ecx
      :||   0x00ba55bd      lea   eax, dword [esi+0x01]
      :||   0x00ba55c0      mov   dword [ebx+0x10], eax
      :||   0x00ba55c3      mov   eax, dword [ebp-0x10]
      :||   0x00ba55c6      cmp   dword [eax+0x1c], 0x00
      :||   0x00ba55ca      mov   ecx, dword [eax+0x34]
      :||   0x00ba55cd      mov   esi, dword [eax+0x30]
      :||   0x00ba55d0      setnz byte [ebp-0x14]
      :||   0x00ba55d4      shl   ecx, 0x02
      :||   0x00ba55d7      xor   edx, edx
      :||   0x00ba55d9      xor   ebx, ebx
      :||   0x00ba55db      lea   eax, dword [ecx+esi*1]
      :||   0x00ba55de      add   ecx, 0x03
      :||   0x00ba55e1      shr   ecx, 0x02
      :||   0x00ba55e4      cmp   esi, eax
      :||   0x00ba55e6      cmovnbe ecx, edx
      :||   0x00ba55e9      test  ecx, ecx
     ,====< 0x00ba55eb      jz    0xba5604
     |:||   0x00ba55ed      mov   edi, ecx
     |:||   0x00ba55ef      nop
    .-----> 0x00ba55f0      mov   ecx, dword [esi]
    :|:||   0x00ba55f2      push  dword [ebp-0x14]
    :|:||   0x00ba55f5      mov   eax, dword [ecx]
    :|:||   0x00ba55f7      call  dword [eax]
    :|:||   0x00ba55f9      inc   ebx
    :|:||   0x00ba55fa      lea   esi, dword [esi+0x04]
    :|:||   0x00ba55fd      cmp   ebx, edi
    `=====< 0x00ba55ff      jnz   0xba55f0
     |:||   0x00ba5601      mov   edi, dword [ebp+0x08]
     `----> 0x00ba5604      mov   ebx, dword [ebp-0x1c]
      :||   0x00ba5607      add   edi, 0x04
      :||   0x00ba560a      mov   dword [ebp+0x08], edi
      :||   0x00ba560d      cmp   edi, dword [ebp-0x18]
      `===< 0x00ba5610      jnz   0xba55a0
       ||   0x00ba5612      mov   esi, dword [ebp-0x10]
       `--> 0x00ba5615      mov   ecx, esi
        |   0x00ba5617      call  0xbaa890
        |   0x00ba561c      mov   eax, dword [ebp-0x20]
        |   0x00ba561f      mov   byte [ebp+0x0b], 0x01
       ,==< 0x00ba5623      jmp   0xba5629
       |`-> 0x00ba5625      mov   byte [ebp+0x0b], 0x00
       `--> 0x00ba5629      mov   ebx, dword [ebp+0x0c]
            0x00ba562c      test  ebx, ebx
        ,=< 0x00ba562e      jz    0xba566e
        |   0x00ba5630      mov   esi, dword [ebp-0x24]
        |   0x00ba5633      lea   edi, dword [esi+eax*4]
        |   0x00ba5636      cmp   esi, edi
       ,==< 0x00ba5638      jz    0xba566e
       ||   0x00ba563a      mov   ecx, dword [ebx+0x10]
       ||   0x00ba563d      mov   dword [ebp+0x10], ecx
      .---> 0x00ba5640      mov   eax, dword [esi]
      :||   0x00ba5642      mov   eax, dword [eax+0x08]
      :||   0x00ba5645      mov   dword [ebp+0x0c], eax
      :||   0x00ba5648      cmp   ecx, dword [ebx+0x04]
     ,====< 0x00ba564b      jnz   0xba5657
     |:||   0x00ba564d      mov   ecx, ebx
     |:||   0x00ba564f      call  0x92a100
     |:||   0x00ba5654      mov   ecx, dword [ebp+0x10]
     `----> 0x00ba5657      mov   eax, dword [ebx+0x0c]
      :||   0x00ba565a      add   esi, 0x04
      :||   0x00ba565d      mov   edx, dword [ebp+0x0c]
      :||   0x00ba5660      mov   dword [eax+ecx*4], edx
      :||   0x00ba5663      inc   ecx
      :||   0x00ba5664      mov   dword [ebp+0x10], ecx
      :||   0x00ba5667      mov   dword [ebx+0x10], ecx
      :||   0x00ba566a      cmp   esi, edi
      `===< 0x00ba566c      jnz   0xba5640
       ``-> 0x00ba566e      cmp   dword [ebp-0x2c], 0x00
            0x00ba5672      mov   dword [ebp-0x04], 0x01
            0x00ba5679      mov   dword [ebp-0x20], 0x00
        ,=< 0x00ba5680      jz    0xba5696
        |   0x00ba5682      mov   esi, dword [ebp-0x24]
        |   0x00ba5685      test  esi, esi
       ,==< 0x00ba5687      jz    0xba5696
       ||   0x00ba5689      call  0x52b950
       ||   0x00ba568e      push  esi
       ||   0x00ba568f      mov   ecx, eax
       ||   0x00ba5691      call  0x52b8b0
       ``-> 0x00ba5696      mov   al, byte [ebp+0x0b]
            0x00ba5699      mov   ecx, dword [ebp-0x0c]
            0x00ba569c      mov   dword fs:[0x0], ecx
            0x00ba56a3      pop   ecx
            0x00ba56a4      pop   edi
            0x00ba56a5      pop   esi
            0x00ba56a6      pop   ebx
            0x00ba56a7      mov   esp, ebp
            0x00ba56a9      pop   ebp
            0x00ba56aa      ret   0x0c
            0x00ba56ad      int3
            0x00ba56ae      int3
            0x00ba56af      int3
            0x00b245c0      push  ebp
            0x00b245c1      mov   ebp, esp
            0x00b245c3      push  0xffffffff                           ; 255
            0x00b245c5      push  0x18686c8
            0x00b245ca      mov   eax, dword fs:[0x0]
            0x00b245d0      push  eax
            0x00b245d1      sub   esp, 0x1c
            0x00b245d4      push  esi
            0x00b245d5      push  edi
            0x00b245d6      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00b245db      xor   eax, ebp
            0x00b245dd      push  eax
            0x00b245de      lea   eax, dword [ebp-0x0c]
            0x00b245e1      mov   dword fs:[0x0], eax
            0x00b245e7      mov   eax, dword [0x201f660]               ; [0x201f660:4]=0
            0x00b245ec      xor   edi, edi
            0x00b245ee      xor   edx, edx
            0x00b245f0      mov   eax, dword [eax+0xe0]
            0x00b245f6      mov   dword [ebp-0x14], edi
            0x00b245f9      mov   dword [ebp-0x10], edx
            0x00b245fc      mov   ecx, dword [eax*4+0x20286d8]
            0x00b24603      mov   dword [ebp-0x18], ecx
            0x00b24606      test  ecx, ecx
        ,=< 0x00b24608      jz    0xb2461d
        |   0x00b2460a      mov   eax, dword [ecx]
        |   0x00b2460c      push  edx
        |   0x00b2460d      lea   edx, dword [ebp-0x14]
        |   0x00b24610      push  edx
        |   0x00b24611      call  dword [eax+0x3c]                     ; 60
        |   0x00b24614      mov   edx, dword [ebp-0x10]
        |   0x00b24617      mov   edi, dword [ebp-0x14]
        |   0x00b2461a      mov   ecx, dword [ebp-0x18]
        `-> 0x00b2461d      mov   dword [ebp-0x04], 0x00
            0x00b24624      test  ecx, ecx
        ,=< 0x00b24626      jz    0xb24638
        |   0x00b24628      mov   eax, dword [ebp+0x08]
        |   0x00b2462b      movzx eax, word [eax+0x20]
        |   0x00b2462f      cmp   eax, edx
       ,==< 0x00b24631      jnb   0xb24638
       ||   0x00b24633      mov   edi, dword [edi+eax*4]
      ,===< 0x00b24636      jmp   0xb2463a
      |``-> 0x00b24638      xor   edi, edi
      `---> 0x00b2463a      mov   esi, dword [ebp+0x0c]
            0x00b2463d      mov   ecx, esi
            0x00b2463f      call  0xb9ce40
            0x00b24644      push  eax
            0x00b24645      mov   ecx, edi
            0x00b24647      call  0xc182a0
            0x00b2464c      mov   ecx, dword [ebp+0x10]
            0x00b2464f      mov   edi, eax
            0x00b24651      lea   eax, dword [ebp-0x28]
            0x00b24654      mov   dword [ebp-0x1c], ecx
            0x00b24657      push  eax
            0x00b24658      mov   ecx, edi
            0x00b2465a      mov   dword [ebp-0x28], 0x19a1778
            0x00b24661      mov   dword [ebp-0x24], 0x00
            0x00b24668      mov   dword [ebp-0x20], esi
            0x00b2466b      call  0xba90a0
            0x00b24670      mov   eax, dword [ebp-0x24]
            0x00b24673      test  eax, eax
        ,=< 0x00b24675      jz    0xb24692
        |   0x00b24677      push  eax
        |   0x00b24678      mov   ecx, edi
        |   0x00b2467a      call  0xba5990
        |   0x00b2467f      mov   ecx, dword [ebp-0x0c]
        |   0x00b24682      mov   dword fs:[0x0], ecx
        |   0x00b24689      pop   ecx
        |   0x00b2468a      pop   edi
        |   0x00b2468b      pop   esi
        |   0x00b2468c      mov   esp, ebp
        |   0x00b2468e      pop   ebp
        |   0x00b2468f      ret   0x0c
        `-> 0x00b24692      mov   ecx, dword [ebp-0x0c]
            0x00b24695      mov   dword fs:[0x0], ecx
            0x00b2469c      pop   ecx
            0x00b2469d      pop   edi
            0x00b2469e      pop   esi
            0x00b2469f      mov   esp, ebp
            0x00b246a1      pop   ebp
            0x00b246a2      ret   0x0c
            0x00b246a5      int3
            0x00b246a6      int3
            0x00b246a7      int3
            0x00b246a8      int3
            0x00b246a9      int3
            0x00b246aa      int3
            0x00b246ab      int3
            0x00b246ac      int3
            0x00b246ad      int3
            0x00b246ae      int3
            0x00b246af      int3
            0x00b246b0      push  ebp
            0x00b246b1      mov   ebp, esp
            0x00b246b3      push  0xffffffff                           ; 255
            0x00b246b5      push  0x1860bf8
            0x00b246ba      mov   eax, dword fs:[0x0]
            0x00b2ced0      push  ebp
            0x00b2ced1      mov   ebp, esp
            0x00b2ced3      push  0xffffffff                           ; 255
            0x00b2ced5      push  0x1869098
            0x00b2ceda      mov   eax, dword fs:[0x0]
            0x00b2cee0      push  eax
            0x00b2cee1      sub   esp, 0x20
            0x00b2cee4      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00b2cee9      xor   eax, ebp
            0x00b2ceeb      mov   dword [ebp-0x10], eax
            0x00b2ceee      push  ebx
            0x00b2ceef      push  esi
            0x00b2cef0      push  edi
            0x00b2cef1      push  eax
            0x00b2cef2      lea   eax, dword [ebp-0x0c]
            0x00b2cef5      mov   dword fs:[0x0], eax
            0x00b2cefb      mov   esi, ecx
            0x00b2cefd      mov   ebx, dword [ebp+0x08]
            0x00b2cf00      lea   eax, dword [esi+0x28]
            0x00b2cf03      mov   edi, dword [ebp+0x0c]
            0x00b2cf06      lea   ecx, dword [ebp-0x24]
            0x00b2cf09      push  eax
            0x00b2cf0a      call  0x4e6c30
            0x00b2cf0f      movss xmm0, dword [esi+0x18]
            0x00b2cf14      sub   esp, 0x14
            0x00b2cf17      mov   eax, dword [esi+0x24]
            0x00b2cf1a      mov   ecx, esp
            0x00b2cf1c      movss dword [ebp-0x1c], xmm0
            0x00b2cf21      movss xmm0, dword [esi+0x1c]
            0x00b2cf26      movss dword [ebp-0x18], xmm0
            0x00b2cf2b      movss xmm0, dword [esi+0x20]
            0x00b2cf30      mov   dword [ebp-0x2c], eax
            0x00b2cf33      mov   eax, dword [esi+0x04]
            0x00b2cf36      movss dword [ebp-0x14], xmm0
            0x00b2cf3b      mov   dword [ecx], eax
            0x00b2cf3d      add   ecx, 0x04
            0x00b2cf40      lea   eax, dword [esi+0x08]
            0x00b2cf43      mov   dword [ebp-0x04], 0x00
            0x00b2cf4a      push  eax
            0x00b2cf4b      call  0x4f70d0
            0x00b2cf50      push  edi
            0x00b2cf51      push  ebx
            0x00b2cf52      call  0xb2e4f0
            0x00b2cf57      add   esp, 0x1c
            0x00b2cf5a      mov   esi, dword [eax+0x124]
            0x00b2cf60      test  esi, esi
        ,=< 0x00b2cf62      jz    0xb2cfc9
        |   0x00b2cf64      lea   eax, dword [ebp-0x24]
        |   0x00b2cf67      push  eax
        |   0x00b2cf68      lea   eax, dword [ebp-0x20]
        |   0x00b2cf6b      push  eax
        |   0x00b2cf6c      call  0x5288e0
        |   0x00b2cf71      add   esp, 0x08
        |   0x00b2cf74      push  0x00
        |   0x00b2cf76      push  0x0a                                 ; 0xa ; 10
        |   0x00b2cf78      lea   ecx, dword [ebp-0x20]
        |   0x00b2cf7b      mov   byte [ebp-0x04], 0x01
        |   0x00b2cf7f      call  0x523620
        |   0x00b2cf84      cmp   eax, 0xffffffff                      ; -1
       ,==< 0x00b2cf87      jz    0xb2cfaf
       ||   0x00b2cf89      push  eax
       ||   0x00b2cf8a      lea   eax, dword [ebp-0x28]
       ||   0x00b2cf8d      push  eax
       ||   0x00b2cf8e      lea   ecx, dword [ebp-0x20]
       ||   0x00b2cf91      call  0x51d390
       ||   0x00b2cf96      push  eax
       ||   0x00b2cf97      lea   ecx, dword [ebp-0x20]
       ||   0x00b2cf9a      mov   byte [ebp-0x04], 0x02
       ||   0x00b2cf9e      call  0x4fcce0
       ||   0x00b2cfa3      lea   ecx, dword [ebp-0x28]
       ||   0x00b2cfa6      mov   byte [ebp-0x04], 0x01
       ||   0x00b2cfaa      call  0x4f94d0
       `--> 0x00b2cfaf      lea   eax, dword [ebp-0x20]
        |   0x00b2cfb2      mov   ecx, esi
        |   0x00b2cfb4      push  eax
        |   0x00b2cfb5      push  dword [ebp-0x2c]
        |   0x00b2cfb8      lea   eax, dword [ebp-0x1c]
        |   0x00b2cfbb      push  eax
        |   0x00b2cfbc      call  0xaa3d00
        |   0x00b2cfc1      lea   ecx, dword [ebp-0x20]
        |   0x00b2cfc4      call  0x4f94d0
        `-> 0x00b2cfc9      lea   ecx, dword [ebp-0x24]
            0x00b2cfcc      call  0x4f94a0
            0x00b2cfd1      mov   ecx, dword [ebp-0x0c]
            0x00b2cfd4      mov   dword fs:[0x0], ecx
            0x00b2cfdb      pop   ecx
            0x00b2cfdc      pop   edi
            0x00b2cfdd      pop   esi
            0x00b2cfde      pop   ebx
            0x00b2cfdf      mov   ecx, dword [ebp-0x10]
            0x00b2cfe2      xor   ecx, ebp
            0x00b2cfe4      call  0x18075f6
            0x00b2cfe9      mov   esp, ebp
            0x00b2cfeb      pop   ebp
            0x00b2cfec      ret   0x08
            0x00b2cfef      int3
            0x00b2cff0      sub   esp, 0x1c
            0x00b2cff3      push  ebx
            0x00b2cff4      push  ebp
            0x00b2cff5      push  esi
            0x00b2cff6      push  edi
            0x00b2cff7      mov   edi, ecx
            0x00b2cff9      push  ecx
            0x00b2cffa      mov   esi, esp
            0x00b2cffc      lea   ecx, dword [esp+0x20]
            0x00b2d000      mov   eax, dword [edi+0x04]
            0x00b2d003      mov   ebx, dword [edi+0x0c]
            0x00b2d006      mov   ebp, dword [edi+0x08]
            0x00b2d009      mov   dword [esp+0x14], eax
            0x00b2d00d      mov   eax, dword [edi+0x10]
            0x00b2d010      mov   dword [esp+0x1c], eax
            0x00b2d014      lea   eax, dword [edi+0x14]
            0x00b2d017      push  eax
            0x00b2d018      call  0x4f70d0
            0x00b2d01d      mov   eax, dword [esp+0x1c]
            0x00b2d021      sub   esp, 0x14
            0x00b2d024      mov   ecx, esp
            0x00b2d026      mov   dword [ecx], eax
            0x00b2d028      lea   eax, dword [esp+0x34]
            0x00b2d02c      push  eax
            0x00b2d02d      add   ecx, 0x04
            0x00b2d030      call  0x4f70d0
            0x00b2d035      push  dword [esp+0x4c]
            0x00b2d039      push  dword [esp+0x4c]
            0x00b2d03d      invalid
            0x00b2d03e      invalid
            0x00b2d03f      invalid
            0x00b2c6c0      push  ebp
            0x00b2c6c1      lea   ebp, dword [esp-0x64]
            0x00b2c6c5      sub   esp, 0x64
            0x00b2c6c8      push  0xffffffff                           ; 255
            0x00b2c6ca      push  0x1868f4e
            0x00b2c6cf      mov   eax, dword fs:[0x0]
            0x00b2c6d5      push  eax
            0x00b2c6d6      sub   esp, 0xb4
            0x00b2c6dc      push  ebx
            0x00b2c6dd      push  esi
            0x00b2c6de      push  edi
            0x00b2c6df      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00b2c6e4      xor   eax, ebp
            0x00b2c6e6      push  eax
            0x00b2c6e7      lea   eax, dword [ebp-0x0c]
            0x00b2c6ea      mov   dword fs:[0x0], eax
            0x00b2c6f0      mov   esi, ecx
            0x00b2c6f2      mov   eax, dword [esi+0x04]
            0x00b2c6f5      lea   ecx, dword [ebp+0x50]
            0x00b2c6f8      mov   dword [ebp+0x4c], eax
            0x00b2c6fb      lea   eax, dword [esi+0x08]
            0x00b2c6fe      push  eax
            0x00b2c6ff      call  0x4f70d0
            0x00b2c704      mov   eax, dword [ebp+0x4c]
            0x00b2c707      sub   esp, 0x14
            0x00b2c70a      mov   ecx, esp
            0x00b2c70c      mov   dword [ecx], eax
            0x00b2c70e      lea   eax, dword [ebp+0x50]
            0x00b2c711      add   ecx, 0x04
            0x00b2c714      push  eax
            0x00b2c715      call  0x4f70d0
            0x00b2c71a      mov   edi, dword [ebp+0x70]
            0x00b2c71d      mov   ebx, dword [ebp+0x6c]
            0x00b2c720      push  edi
            0x00b2c721      push  ebx
            0x00b2c722      call  0xb28a70
            0x00b2c727      mov   ecx, dword [esi+0x104]
            0x00b2c72d      add   esp, 0x1c
            0x00b2c730      mov   dword [ebp+0x38], ecx
            0x00b2c733      lea   ecx, dword [esi+0x108]
            0x00b2c739      mov   dword [ebp+0x70], eax
            0x00b2c73c      push  ecx
            0x00b2c73d      lea   ecx, dword [ebp+0x3c]
            0x00b2c740      call  0x4f70d0
            0x00b2c745      mov   eax, dword [ebp+0x38]
            0x00b2c748      sub   esp, 0x14
            0x00b2c74b      mov   ecx, esp
            0x00b2c74d      mov   dword [ecx], eax
            0x00b2c74f      lea   eax, dword [ebp+0x3c]
            0x00b2c752      add   ecx, 0x04
            0x00b2c755      push  eax
            0x00b2c756      call  0x4f70d0
            0x00b2c75b      push  edi
            0x00b2c75c      push  ebx
            0x00b2c75d      call  0xb28a70
            0x00b2c762      add   esp, 0x1c
            0x00b2c765      test  eax, eax
        ,=< 0x00b2c767      jz    0xb2c778
        |   0x00b2c769      mov   dword [ebp+0x60], 0xffffffff         ; -1
        |   0x00b2c770      mov   eax, dword [eax+0x20]
        |   0x00b2c773      mov   dword [ebp+0x60], eax
       ,==< 0x00b2c776      jmp   0xb2c780
       |`-> 0x00b2c778      lea   ecx, dword [ebp+0x60]
       |    0x00b2c77b      call  0x4f6c50
       `--> 0x00b2c780      sub   esp, 0x1c
            0x00b2c783      mov   dword [ebp-0x04], 0x00
            0x00b2c78a      lea   eax, dword [esi+0xe8]
            0x00b2c790      mov   ecx, esp
            0x00b2c792      push  eax
            0x00b2c793      call  0xb2a260
            0x00b2c798      push  edi
            0x00b2c799      lea   eax, dword [ebp-0x28]
            0x00b2c79c      push  ebx
            0x00b2c79d      push  eax
            0x00b2c79e      call  0xb2e590
            0x00b2c7a3      sub   esp, 0x24
            0x00b2c7a6      mov   byte [ebp-0x04], 0x01
            0x00b2c7aa      lea   eax, dword [esi+0x9c]
            0x00b2c7b0      mov   ecx, esp
            0x00b2c7b2      push  eax
            0x00b2c7b3      call  0xb2a2f0
            0x00b2c7b8      push  edi
            0x00b2c7b9      lea   eax, dword [ebp-0xc0]
            0x00b2c7bf      push  ebx
            0x00b2c7c0      push  eax
            0x00b2c7c1      call  0xb2e600
            0x00b2c7c6      add   esp, 0x0c
            0x00b2c7c9      mov   byte [ebp-0x04], 0x02
            0x00b2c7cd      lea   eax, dword [esi+0x50]
            0x00b2c7d0      mov   ecx, esp
            0x00b2c7d2      push  eax
            0x00b2c7d3      call  0xb2a2f0
            0x00b2c7d8      push  edi
            0x00b2c7d9      lea   eax, dword [ebp-0x74]
            0x00b2c7dc      push  ebx
            0x00b2c7dd      push  eax
            0x00b2c7de      call  0xb2e600
            0x00b2c7e3      add   esp, 0x3c
            0x00b2c7e6      mov   byte [ebp-0x04], 0x03
            0x00b2c7ea      lea   eax, dword [esi+0x34]
            0x00b2c7ed      mov   ecx, esp
            0x00b2c7ef      push  eax
            0x00b2c7f0      call  0xb2a260
            0x00b2c7f5      push  edi
            0x00b2c7f6      lea   eax, dword [ebp]
            0x00b2c7f9      push  ebx
            0x00b2c7fa      push  eax
            0x00b2c7fb      call  0xb2e590
            0x00b2c800      add   esp, 0x0c
            0x00b2c803      mov   byte [ebp-0x04], 0x04
            0x00b2c807      lea   eax, dword [esi+0x18]
            0x00b2c80a      mov   ecx, esp
            0x00b2c80c      push  eax
            0x00b2c80d      call  0xb2a260
            0x00b2c812      push  edi
            0x00b2c813      lea   eax, dword [ebp+0x1c]
            0x00b2c816      push  ebx
            0x00b2c817      push  eax
            0x00b2c818      call  0xb2e590
            0x00b2c81d      lea   eax, dword [ebp+0x60]
            0x00b2c820      mov   dword [ebp-0x04], 0x0a
            0x00b2c827      push  eax
            0x00b2c828      lea   eax, dword [ebp-0x28]
            0x00b2c82b      push  eax
            0x00b2c82c      lea   eax, dword [ebp-0xc0]
            0x00b2c832      push  eax
            0x00b2c833      lea   eax, dword [ebp-0x74]
            0x00b2c836      push  eax
            0x00b2c837      lea   eax, dword [ebp]
            0x00b2c83a      push  eax
            0x00b2c83b      lea   eax, dword [ebp+0x1c]
            0x00b2c83e      push  eax
            0x00b2c83f      invalid
