            0x00ba6310      mov   eax, dword [ecx+0x18]
            0x00ba6313      mov   ecx, dword [ecx+0x1c]
            0x00ba6316      push  esi
            0x00ba6317      lea   ecx, dword [eax+ecx*4]
            0x00ba631a      cmp   eax, ecx
        ,=< 0x00ba631c      jz    0xba6330
        |   0x00ba631e      mov   esi, dword [esp+0x08]
       .--> 0x00ba6322      mov   edx, dword [eax]
       :|   0x00ba6324      cmp   dword [edx+0x08], esi
      ,===< 0x00ba6327      jz    0xba6336
      |:|   0x00ba6329      add   eax, 0x04
      |:|   0x00ba632c      cmp   eax, ecx
      |`==< 0x00ba632e      jnz   0xba6322
      | `-> 0x00ba6330      xor   eax, eax
      |     0x00ba6332      pop   esi
      |     0x00ba6333      ret   0x04
      `---> 0x00ba6336      mov   eax, edx
            0x00ba6338      pop   esi
            0x00ba6339      ret   0x04
            0x00ba633c      int3
            0x00ba633d      int3
            0x00ba633e      int3
            0x00ba633f      int3
            0x00ba6340      fld   dword [ecx+0x24]
            0x00ba6343      fmul  dword [esp+0x04]
            0x00ba6347      ret   0x04
            0x00ba634a      int3
            0x00ba634b      int3
            0x00ba634c      int3
            0x00ba634d      int3
            0x00ba634e      int3
            0x00ba634f      int3
            0x00ba6350      sub   esp, 0x14
            0x00ba6353      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00ba6358      xor   eax, esp
            0x00ba635a      mov   dword [esp+0x10], eax
            0x00ba635e      push  esi
            0x00ba635f      mov   esi, dword [esp+0x1c]
            0x00ba6363      lea   eax, dword [esp+0x04]
            0x00ba6367      push  edi
            0x00ba6368      mov   edi, dword [esp+0x24]
            0x00ba636c      push  edi
            0x00ba636d      push  eax
            0x00ba636e      call  0xb59e80
            0x00ba6373      mov   ecx, dword [0x201e100]               ; [0x201e100:4]=0
            0x00ba6379      lea   eax, dword [esp+0x10]
            0x00ba637d      add   esp, 0x08
            0x00ba6380      push  eax
            0x00ba6381      call  0x949f40
            0x00ba6386      test  al, al
        ,=< 0x00ba6388      jz    0xba63a9
        |   0x00ba638a      lea   eax, dword [esp+0x08]
        |   0x00ba638e      mov   ecx, esi
        |   0x00ba6390      push  eax
        |   0x00ba6391      call  0x4f70d0
        |   0x00ba6396      mov   eax, esi
        |   0x00ba6398      pop   edi
        |   0x00ba6399      pop   esi
        |   0x00ba639a      mov   ecx, dword [esp+0x10]
        |   0x00ba639e      xor   ecx, esp
        |   0x00ba63a0      call  0x18075f6
        |   0x00ba63a5      add   esp, 0x14
        |   0x00ba63a8      ret
        `-> 0x00ba63a9      mov   ax, word [edi+0x88]
            0x00ba63b0      push  ecx
            0x00ba63b1      mov   ecx, esp
            0x00ba63b3      mov   word [ecx], ax
            0x00ba63b6      call  0xa68dc0
            0x00ba63bb      add   esp, 0x04
            0x00ba63be      mov   ecx, esi
            0x00ba63c0      push  eax
            0x00ba63c1      push  0x00
            0x00ba63c3      push  0x00
            0x00ba63c5      push  0x0a                                 ; 0xa ; 10
            0x00ba63c7      call  0x4f71d0
            0x00ba63cc      mov   ecx, dword [esp+0x18]
            0x00ba63d0      mov   eax, esi
            0x00ba63d2      pop   edi
            0x00ba63d3      pop   esi
            0x00ba63d4      xor   ecx, esp
            0x00ba63d6      call  0x18075f6
            0x00ba63db      add   esp, 0x14
            0x00ba63de      ret
            0x00ba63df      int3
            0x00ba63e0      mov   ax, word [esp+0x08]
            0x00ba63e5      push  ecx
            0x00ba63e6      mov   ecx, esp
            0x00ba63e8      mov   word [ecx], ax
            0x00ba63eb      call  0xa68dc0
            0x00ba63f0      mov   ecx, dword [esp+0x08]
            0x00ba63f4      add   esp, 0x04
            0x00ba63f7      push  eax
            0x00ba63f8      push  0x00
            0x00ba63fa      push  0x00
            0x00ba63fc      push  0x0a                                 ; 0xa ; 10
            0x00ba63fe      call  0x4f71d0
            0x00ba6403      mov   eax, dword [esp+0x04]
            0x00ba6407      ret
            0x00ba6408      int3
            0x00ba6409      int3
            0x00ba640a      int3
            0x00ba640b      int3
            0x00ba640c      int3
            0x00ba640d      int3
            0x00ba640e      int3
            0x00ba640f      int3
            0x00ba6410      push  ebp
            0x00ba6411      mov   ebp, esp
            0x00ba6413      push  0xffffffff                           ; 255
            0x00ba6415      push  0x18704fc
            0x00ba641a      mov   eax, dword fs:[0x0]
            0x00ba6420      push  eax
            0x00ba6421      push  esi
            0x00ba6422      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00ba6427      xor   eax, ebp
            0x00ba6429      push  eax
            0x00ba642a      lea   eax, dword [ebp-0x0c]
            0x00ba642d      mov   dword fs:[0x0], eax
            0x00ba6433      mov   esi, dword [ecx+0x0c]
            0x00ba6436      mov   eax, dword fs:[0x2c]
            0x00ba643c      mov   ecx, dword [0x218e080]               ; [0x218e080:4]=0
            0x00ba6442      add   esi, dword [ebp+0x0c]
            0x00ba6445      mov   ecx, dword [eax+ecx*4]
            0x00ba6448      mov   eax, dword [0x203cad4]               ; [0x203cad4:4]=0
            0x00ba644d      cmp   eax, dword [ecx+0x04]
        ,=< 0x00ba6453      jnle  0xba6486
        |   0x00ba6455      mov   eax, dword [esi]
        |   0x00ba6457      cmp   eax, 0x58                            ; 'X' ; 88
        |   0x00ba645a      lea   eax, dword [eax*4+0x203c970]
       ,==< 0x00ba6461      jl    0xba6468
       ||   0x00ba6463      mov   eax, 0x203cad0
       `--> 0x00ba6468      mov   ecx, dword [ebp+0x08]
        |   0x00ba646b      push  eax
        |   0x00ba646c      call  0x4e6c30
        |   0x00ba6471      mov   eax, dword [ebp+0x08]
        |   0x00ba6474      mov   ecx, dword [ebp-0x0c]
        |   0x00ba6477      mov   dword fs:[0x0], ecx
        |   0x00ba647e      pop   ecx
        |   0x00ba647f      pop   esi
        |   0x00ba6480      mov   esp, ebp
        |   0x00ba6482      pop   ebp
        |   0x00ba6483      ret   0x08
        `-> 0x00ba6486      push  0x203cad4
            0x00ba648b      call  0x1806ee7
            0x00b9ce40      push  esi
            0x00b9ce41      mov   esi, ecx
            0x00b9ce43      push  esi
            0x00b9ce44      call  0xcc07e0
            0x00b9ce49      add   esp, 0x04
            0x00b9ce4c      test  al, al
            0x00b9ce4e      mov   eax, 0x07
        ,=< 0x00b9ce53      jnz   0xb9ce5b
        |   0x00b9ce55      mov   eax, dword [esi+0xa8]
        `-> 0x00b9ce5b      pop   esi
            0x00b9ce5c      ret
            0x00b9ce5d      int3
            0x00b9ce5e      int3
            0x00b9ce5f      int3
            0x00b9ce60      mov   ecx, dword [esp+0x04]
            0x00b9ce64      call  0xb01530
            0x00b9ce69      test  eax, eax
        ,=< 0x00b9ce6b      jz    0xb9cecb
        |   0x00b9ce6d      mov   eax, dword [eax+0x28]
        |   0x00b9ce70      mov   eax, dword [eax+0xf8]
        |   0x00b9ce76      cmp   eax, 0x01                            ; 1
       ,==< 0x00b9ce79      jnz   0xb9ce83
       ||   0x00b9ce7b      mov   ecx, 0x02
       ||   0x00b9ce80      mov   eax, ecx
       ||   0x00b9ce82      ret
       `--> 0x00b9ce83      cmp   eax, 0x02                            ; 2
       ,==< 0x00b9ce86      jz    0xb9cec3
       ||   0x00b9ce88      cmp   eax, 0x03                            ; 3
      ,===< 0x00b9ce8b      jz    0xb9cec3
      |||   0x00b9ce8d      cmp   eax, 0x04                            ; 4
     ,====< 0x00b9ce90      jz    0xb9cec3
     ||||   0x00b9ce92      cmp   eax, 0x05                            ; 5
    ,=====< 0x00b9ce95      jz    0xb9cec3
    |||||   0x00b9ce97      cmp   eax, 0x06                            ; 6
   ,======< 0x00b9ce9a      jnz   0xb9cea1
   ||||||   0x00b9ce9c      xor   ecx, ecx
   ||||||   0x00b9ce9e      mov   eax, ecx
   ||||||   0x00b9cea0      ret
   `------> 0x00b9cea1      cmp   eax, 0x07                            ; 7
   ,======< 0x00b9cea4      jz    0xb9cebb
   ||||||   0x00b9cea6      cmp   eax, 0x08                            ; 8
  ,=======< 0x00b9cea9      jz    0xb9cebb
  |||||||   0x00b9ceab      xor   ecx, ecx
  |||||||   0x00b9cead      mov   edx, 0x04
  |||||||   0x00b9ceb2      cmp   eax, 0x09                            ; 9
  |||||||   0x00b9ceb5      cmovz ecx, edx
  |||||||   0x00b9ceb8      mov   eax, ecx
  |||||||   0x00b9ceba      ret
  ``------> 0x00b9cebb      mov   ecx, 0x01
    |||||   0x00b9cec0      mov   eax, ecx
    |||||   0x00b9cec2      ret
    ````--> 0x00b9cec3      mov   ecx, 0x03
        |   0x00b9cec8      mov   eax, ecx
        |   0x00b9ceca      ret
        `-> 0x00b9cecb      xor   eax, eax
            0x00b9cecd      ret
            0x00b9cece      int3
            0x00b9cecf      int3
            0x00b9ced0      mov   ecx, dword [ecx+0xf8]
            0x00b9ced6      cmp   ecx, 0x01                            ; 1
        ,=< 0x00b9ced9      jnz   0xb9cedf
        |   0x00b9cedb      lea   eax, dword [ecx+0x01]
        |   0x00b9cede      ret
        `-> 0x00b9cedf      cmp   ecx, 0x02                            ; 2
        ,=< 0x00b9cee2      jz    0xb9cf19
        |   0x00b9cee4      cmp   ecx, 0x03                            ; 3
       ,==< 0x00b9cee7      jz    0xb9cf19
       ||   0x00b9cee9      cmp   ecx, 0x04                            ; 4
      ,===< 0x00b9ceec      jz    0xb9cf19
      |||   0x00b9ceee      cmp   ecx, 0x05                            ; 5
     ,====< 0x00b9cef1      jz    0xb9cf19
     ||||   0x00b9cef3      cmp   ecx, 0x06                            ; 6
    ,=====< 0x00b9cef6      jnz   0xb9cefb
    |||||   0x00b9cef8      xor   eax, eax
    |||||   0x00b9cefa      ret
    `-----> 0x00b9cefb      cmp   ecx, 0x07                            ; 7
    ,=====< 0x00b9cefe      jz    0xb9cf13
    |||||   0x00b9cf00      cmp   ecx, 0x08                            ; 8
   ,======< 0x00b9cf03      jz    0xb9cf13
   ||||||   0x00b9cf05      xor   eax, eax
   ||||||   0x00b9cf07      mov   edx, 0x04
   ||||||   0x00b9cf0c      cmp   ecx, 0x09                            ; 9
   ||||||   0x00b9cf0f      cmovz eax, edx
   ||||||   0x00b9cf12      ret
   ``-----> 0x00b9cf13      mov   eax, 0x01
     ||||   0x00b9cf18      ret
     ````-> 0x00b9cf19      mov   eax, 0x03
            0x00b9cf1e      ret
            0x00b9cf1f      int3
            0x00b9cf20      mov   eax, dword [ecx+0x24]
            0x00b9cf23      ret   0x04
            0x00b9cf26      int3
            0x00b9cf27      int3
            0x00b9cf28      int3
            0x00b9cf29      int3
            0x00b9cf2a      int3
            0x00b9cf2b      int3
            0x00b9cf2c      int3
            0x00b9cf2d      int3
            0x00b9cf2e      int3
            0x00b9cf2f      int3
            0x00b9cf30      fld   dword [ecx+0x44]
            0x00b9cf33      ret
            0x00b9cf34      int3
            0x00b9cf35      int3
            0x00b9cf36      int3
            0x00b9cf37      int3
            0x00b9cf38      int3
            0x00b9cf39      int3
            0x00b9cf3a      int3
            0x00b9cf3b      int3
            0x00b9cf3c      int3
            0x00b9cf3d      int3
            0x00b9cf3e      int3
            0x00b9cf3f      int3
            0x00b9cf40      push  ecx
            0x00b9cf41      push  esi
            0x00b9cf42      lea   eax, dword [esp+0x04]
            0x00b9cf46      mov   esi, ecx
            0x00b9cf48      push  eax
            0x00b9cf49      call  0xb136e0
            0x00b9cf4e      add   esp, 0x04
            0x00b9cf51      mov   ecx, esi
            0x00b9cf53      push  eax
            0x00b9cf54      call  0xafd2b0
            0x00b9cf59      pop   esi
            0x00b9cf5a      test  eax, eax
        ,=< 0x00b9cf5c      jz    0xb9cf63
        |   0x00b9cf5e      fld   dword [eax+0x1c]
        |   0x00b9cf61      pop   ecx
        |   0x00b9cf62      ret
        `-> 0x00b9cf63      fldz
            0x00b9cf65      pop   ecx
            0x00b9cf66      ret
            0x00b9cf67      int3
            0x00b9cf68      int3
            0x00b9cf69      int3
            0x00b9cf6a      int3
            0x00b9cf6b      int3
            0x00b9cf6c      int3
            0x00b9cf6d      int3
            0x00b9cf6e      int3
            0x00b9cf6f      int3
            0x00b9cf70      push  ebp
            0x00b9cf71      mov   ebp, esp
            0x00b9cf73      push  0xffffffff                           ; 255
            0x00b9cf75      push  0x1812050
            0x00b9cf7a      mov   eax, dword fs:[0x0]
            0x00b9cf80      push  eax
            0x00b9cf81      sub   esp, 0x0c
            0x00b9cf84      push  esi
            0x00b9cf85      push  edi
            0x00b9cf86      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00b9cf8b      xor   eax, ebp
            0x00b9cf8d      push  eax
            0x00b9cf8e      lea   eax, dword [ebp-0x0c]
            0x00b9cf91      mov   dword fs:[0x0], eax
            0x00b9cf97      mov   esi, dword [ebp+0x08]
            0x00b9cf9a      mov   ecx, esi
            0x00b9cf9c      call  0xb014f0
            0x00b9cfa1      test  eax, eax
        ,=< 0x00b9cfa3      jz    0xb9cfbd
        |   0x00b9cfa5      mov   ecx, eax
        |   0x00b9cfa7      call  0xa74c40
        |   0x00b9cfac      mov   ecx, dword [ebp-0x0c]
        |   0x00b9cfaf      mov   dword fs:[0x0], ecx
        |   0x00b9cfb6      pop   ecx
        |   0x00b9cfb7      pop   edi
        |   0x00b9cfb8      pop   esi
        |   0x00b9cfb9      mov   esp, ebp
        |   0x00b9cfbb      pop   ebp
        |   0x00b9cfbc      ret
        `-> 0x00b9cfbd      mov   eax, dword [0x201f660]               ; [0x201f660:4]=0
            0x00b9cfc2      xor   edx, edx
            0x00b9cfc4      xor   edi, edi
            0x00b9cfc6      mov   eax, dword [eax+0xa8]
            0x00b9cfcc      mov   dword [ebp-0x14], edx
            0x00b9cfcf      mov   dword [ebp-0x10], edi
            0x00b9cfd2      mov   ecx, dword [eax*4+0x2027ed0]
            0x00b9cfd9      mov   dword [ebp-0x18], ecx
            0x00b9cfdc      test  ecx, ecx
        ,=< 0x00b9cfde      jz    0xb9d003
        |   0x00b9cfe0      mov   eax, dword [ecx]
        |   0x00b9cfe2      lea   edx, dword [ebp-0x14]
        |   0x00b9cfe5      push  edi
        |   0x00b9cfe6      push  edx
        |   0x00b9cfe7      call  dword [eax+0x40]                     ; 64
        |   0x00b9cfea      mov   ecx, dword [ebp-0x18]
        |   0x00b9cfed      mov   edi, dword [ebp-0x10]
        |   0x00b9cff0      mov   edx, dword [ebp-0x14]
        |   0x00b9cff3      test  ecx, ecx
       ,==< 0x00b9cff5      jz    0xb9d003
       ||   0x00b9cff7      movzx eax, word [esi]
       ||   0x00b9cffa      cmp   eax, edi
      ,===< 0x00b9cffc      jnb   0xb9d003
      |||   0x00b9cffe      mov   eax, dword [edx+eax*4]
     ,====< 0x00b9d001      jmp   0xb9d005
     |```-> 0x00b9d003      xor   eax, eax
     `----> 0x00b9d005      mov   ecx, dword [ebp-0x0c]
            0x00b9d008      mov   dword fs:[0x0], ecx
            0x00b9d00f      pop   ecx
            0x00b9d010      pop   edi
            0x00b9d011      pop   esi
            0x00b9d012      mov   esp, ebp
            0x00b9d014      pop   ebp
            0x00b9d015      ret
            0x00b9d016      int3
            0x00b9d017      int3
            0x00b9d018      int3
            0x00b9d019      int3
            0x00b9d01a      int3
            0x00b9d01b      int3
            0x00b9d01c      int3
            0x00b9d01d      int3
            0x00b9d01e      int3
            0x00b9d01f      int3
            0x00bcdcd0      push  ebx
            0x00bcdcd1      mov   ebx, dword [esp+0x08]
            0x00bcdcd5      push  esi
            0x00bcdcd6      push  edi
            0x00bcdcd7      mov   edi, ecx
            0x00bcdcd9      push  dword [edi+0x0c]
            0x00bcdcdc      mov   ecx, dword [edi]
            0x00bcdcde      push  ebx
            0x00bcdcdf      call  0xb9d3c0
            0x00bcdce4      mov   ecx, dword [edi+0x04]
            0x00bcdce7      mov   esi, eax
            0x00bcdce9      test  ecx, ecx
        ,=< 0x00bcdceb      jz    0xbcdcf8
        |   0x00bcdced      push  dword [edi+0x0c]
        |   0x00bcdcf0      push  ebx
        |   0x00bcdcf1      call  0xb9d3c0
        |   0x00bcdcf6      add   esi, eax
        `-> 0x00bcdcf8      mov   ecx, dword [edi+0x08]
            0x00bcdcfb      test  ecx, ecx
        ,=< 0x00bcdcfd      jz    0xbcdd10
        |   0x00bcdcff      push  dword [edi+0x0c]
        |   0x00bcdd02      push  ebx
        |   0x00bcdd03      call  0xb9d3c0
        |   0x00bcdd08      pop   edi
        |   0x00bcdd09      add   eax, esi
        |   0x00bcdd0b      pop   esi
        |   0x00bcdd0c      pop   ebx
        |   0x00bcdd0d      ret   0x04
        `-> 0x00bcdd10      pop   edi
            0x00bcdd11      mov   eax, esi
            0x00bcdd13      pop   esi
            0x00bcdd14      pop   ebx
            0x00bcdd15      ret   0x04
            0x00bcdd18      int3
            0x00bcdd19      int3
            0x00bcdd1a      int3
            0x00bcdd1b      int3
            0x00bcdd1c      int3
            0x00bcdd1d      int3
            0x00bcdd1e      int3
            0x00bcdd1f      int3
            0x00bcdd20      push  dword [esp+0x08]
            0x00bcdd24      call  0xc181f0
            0x00bcdd29      mov   edx, eax
            0x00bcdd2b      mov   eax, dword [esp+0x04]
            0x00bcdd2f      test  edx, edx
        ,=< 0x00bcdd31      jz    0xbcdd47
        |   0x00bcdd33      mov   ecx, dword [edx+0xe0]
        |   0x00bcdd39      mov   dword [eax], ecx
        |   0x00bcdd3b      mov   ecx, dword [edx+0xe4]
        |   0x00bcdd41      mov   dword [eax+0x04], ecx
        |   0x00bcdd44      ret   0x08
        `-> 0x00bcdd47      mov   dword [eax], 0x3f800000              ; [0x3f800000:4]=-1
            0x00bcdd4d      mov   dword [eax+0x04], 0x00
            0x00bcdd54      ret   0x08
            0x00bcdd57      int3
            0x00bcdd58      int3
            0x00bcdd59      int3
            0x00bcdd5a      int3
            0x00bcdd5b      int3
            0x00bcdd5c      int3
            0x00bcdd5d      int3
            0x00bcdd5e      int3
            0x00bcdd5f      int3
            0x00bcdd60      sub   esp, 0x24
            0x00bcdd63      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00bcdd68      xor   eax, esp
            0x00bcdd6a      mov   dword [esp+0x20], eax
            0x00bcdd6e      mov   eax, dword [esp+0x30]
            0x00bcdd72      mov   ecx, dword [0x201e2d8]               ; [0x201e2d8:4]=0
            0x00bcdd78      push  ebx
            0x00bcdd79      push  ebp
            0x00bcdd7a      push  esi
            0x00bcdd7b      mov   esi, dword [esp+0x38]
            0x00bcdd7f      push  edi
            0x00bcdd80      mov   edi, dword [esp+0x38]
            0x00bcdd84      mov   dword [esp+0x10], edi
            0x00bcdd88      mov   dword [esp+0x1c], esi
            0x00bcdd8c      mov   dword [esp+0x18], eax
            0x00bcdd90      call  0xab0f80
            0x00bcdd95      xor   ebx, ebx
            0x00bcdd97      mov   ebp, eax
            0x00bcdd99      mov   dword [esp+0x14], ebp
            0x00bcdd9d      cmp   dword [esi+0x10], ebx
        ,=< 0x00bcdda0      jbe   0xbcde83
        |   0x00bcdda6      cmp   dword [edi+0x10], 0x00
       ,==< 0x00bcddaa      jz    0xbcde83
       ||   0x00bcddb0      mov   eax, dword [esi+0x0c]
       ||   0x00bcddb3      mov   esi, dword [eax+ebx*4]
       ||   0x00bcddb6      mov   ecx, esi
       ||   0x00bcddb8      call  0x55e020
       ||   0x00bcddbd      movss xmm0, dword [esi+0x0c]
       ||   0x00bcddc2      lea   eax, dword [esp+0x24]
       ||   0x00bcddc6      movss dword [esp+0x24], xmm0
       ||   0x00bcddcc      mov   ecx, ebp
       ||   0x00bcddce      movss xmm0, dword [esi+0x10]
       ||   0x00bcddd3      movss dword [esp+0x28], xmm0
       ||   0x00bcddd9      movss xmm0, dword [esi+0x14]
       ||   0x00bcddde      push  eax
       ||   0x00bcdddf      movss dword [esp+0x30], xmm0
       ||   0x00bcdde5      call  0xc181f0
       ||   0x00bcddea      mov   esi, eax
       ||   0x00bcddec      test  esi, esi
      ,===< 0x00bcddee      jz    0xbcde75
      |||   0x00bcddf4      mov   ecx, esi
      |||   0x00bcddf6      call  0x745030
      |||   0x00bcddfb      test  eax, eax
     ,====< 0x00bcddfd      jz    0xbcde75
     ||||   0x00bcddff      mov   ecx, esi
     ||||   0x00bcde01      call  0x745030
     ||||   0x00bcde06      mov   ecx, eax
     ||||   0x00bcde08      call  0xb7a870
     ||||   0x00bcde0d      mov   ecx, dword [esp+0x10]
     ||||   0x00bcde11      mov   ebp, eax
     ||||   0x00bcde13      mov   esi, dword [edi+0x0c]
     ||||   0x00bcde16      mov   ecx, dword [ecx+0x10]
     ||||   0x00bcde19      lea   ecx, dword [esi+ecx*4]
     ||||   0x00bcde1c      cmp   esi, ecx
    ,=====< 0x00bcde1e      jz    0xbcde6d
    |||||   0x00bcde20      mov   ecx, dword [esi]
    |||||   0x00bcde22      call  0xb7a870
    |||||   0x00bcde27      cmp   eax, ebp
   ,======< 0x00bcde29      jnz   0xbcde47
   ||||||   0x00bcde2b      push  dword [esp+0x44]
   ||||||   0x00bcde2f      lea   eax, dword [esp+0x28]
   ||||||   0x00bcde33      push  ebx
   ||||||   0x00bcde34      push  dword [esp+0x20]
   ||||||   0x00bcde38      push  eax
   ||||||   0x00bcde39      push  dword [esi]
   ||||||   0x00bcde3b      call  0xbd0570
   ||||||   0x00bcde40      add   esp, 0x14
   ||||||   0x00bcde43      test  al, al
  ,=======< 0x00bcde45      jnz   0xbcde59
  |`------> 0x00bcde47      mov   ecx, dword [edi+0x10]
  | |||||   0x00bcde4a      add   esi, 0x04
  | |||||   0x00bcde4d      mov   eax, dword [edi+0x0c]
            0x00b2e760      push  ebp
            0x00b2e761      mov   ebp, esp
            0x00b2e763      push  0xffffffff                           ; 255
            0x00b2e765      push  0x186932b
            0x00b2e76a      mov   eax, dword fs:[0x0]
            0x00b2e770      push  eax
            0x00b2e771      push  ecx
            0x00b2e772      push  ebx
            0x00b2e773      push  esi
            0x00b2e774      push  edi
            0x00b2e775      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00b2e77a      xor   eax, ebp
            0x00b2e77c      push  eax
            0x00b2e77d      lea   eax, dword [ebp-0x0c]
            0x00b2e780      mov   dword fs:[0x0], eax
            0x00b2e786      push  dword [0x1d6c084]
            0x00b2e78c      push  0x01                                 ; 1
            0x00b2e78e      push  0x2c                                 ; ',' ; 44
            0x00b2e790      push  0x01                                 ; 1
            0x00b2e792      call  0x529280
            0x00b2e797      mov   esi, eax
            0x00b2e799      add   esp, 0x10
            0x00b2e79c      mov   dword [ebp-0x10], esi
            0x00b2e79f      mov   dword [ebp-0x04], 0x00
            0x00b2e7a6      test  esi, esi
        ,=< 0x00b2e7a8      jz    0xb2e7d4
        |   0x00b2e7aa      mov   ecx, esi
        |   0x00b2e7ac      call  0xb21f60
        |   0x00b2e7b1      mov   dword [esi], 0x19a1908               ; [0x19a1908:4]=0x561c50
        |   0x00b2e7b7      lea   ecx, dword [esi+0x08]
        |   0x00b2e7ba      mov   byte [ebp-0x04], 0x01
        |   0x00b2e7be      mov   dword [esi+0x04], 0x00
        |   0x00b2e7c5      call  0x4f71f0
        |   0x00b2e7ca      lea   ecx, dword [esi+0x18]
        |   0x00b2e7cd      call  0x4f71f0
       ,==< 0x00b2e7d2      jmp   0xb2e7d6
       |`-> 0x00b2e7d4      xor   esi, esi
       `--> 0x00b2e7d6      mov   edi, dword [ebp+0x08]
            0x00b2e7d9      lea   ebx, dword [esi+0x04]
            0x00b2e7dc      push  0x04                                 ; 4
            0x00b2e7de      push  ebx
            0x00b2e7df      mov   ecx, edi
            0x00b2e7e1      mov   dword [ebp-0x04], 0xffffffff         ; -1
            0x00b2e7e8      mov   eax, dword [edi]
            0x00b2e7ea      mov   eax, dword [eax+0x04]
            0x00b2e7ed      call  eax
            0x00b2e7ef      test  al, al
        ,=< 0x00b2e7f1      jz    0xb2e840
        |   0x00b2e7f3      mov   eax, dword [edi]
        |   0x00b2e7f5      mov   ecx, edi
        |   0x00b2e7f7      push  0x10                                 ; 16
        |   0x00b2e7f9      mov   edx, dword [eax+0x04]
        |   0x00b2e7fc      lea   eax, dword [ebx+0x04]
        |   0x00b2e7ff      push  eax
        |   0x00b2e800      call  edx
        |   0x00b2e802      test  al, al
       ,==< 0x00b2e804      jz    0xb2e840
       ||   0x00b2e806      mov   eax, dword [edi]
       ||   0x00b2e808      mov   ecx, edi
       ||   0x00b2e80a      push  0x10                                 ; 16
       ||   0x00b2e80c      mov   edx, dword [eax+0x04]
       ||   0x00b2e80f      lea   eax, dword [esi+0x18]
       ||   0x00b2e812      push  eax
       ||   0x00b2e813      call  edx
       ||   0x00b2e815      test  al, al
      ,===< 0x00b2e817      jz    0xb2e840
      |||   0x00b2e819      mov   eax, dword [edi]
      |||   0x00b2e81b      mov   ecx, edi
      |||   0x00b2e81d      push  0x04                                 ; 4
      |||   0x00b2e81f      mov   edx, dword [eax+0x04]
      |||   0x00b2e822      lea   eax, dword [esi+0x28]
      |||   0x00b2e825      push  eax
      |||   0x00b2e826      call  edx
      |||   0x00b2e828      test  al, al
     ,====< 0x00b2e82a      jz    0xb2e840
     ||||   0x00b2e82c      mov   eax, esi
     ||||   0x00b2e82e      mov   ecx, dword [ebp-0x0c]
     ||||   0x00b2e831      mov   dword fs:[0x0], ecx
     ||||   0x00b2e838      pop   ecx
     ||||   0x00b2e839      pop   edi
     ||||   0x00b2e83a      pop   esi
     ||||   0x00b2e83b      pop   ebx
     ||||   0x00b2e83c      mov   esp, ebp
     ||||   0x00b2e83e      pop   ebp
     ||||   0x00b2e83f      ret
     ````-> 0x00b2e840      test  esi, esi
        ,=< 0x00b2e842      jz    0xb2e84d
        |   0x00b2e844      mov   eax, dword [esi]
        |   0x00b2e846      mov   ecx, esi
        |   0x00b2e848      push  0x01                                 ; 1
        |   0x00b2e84a      call  dword [eax+0x08]                     ; 8
        `-> 0x00b2e84d      xor   eax, eax
            0x00b2e84f      mov   ecx, dword [ebp-0x0c]
            0x00b2e852      mov   dword fs:[0x0], ecx
            0x00b2e859      pop   ecx
            0x00b2e85a      pop   edi
            0x00b2e85b      pop   esi
            0x00b2e85c      pop   ebx
            0x00b2e85d      mov   esp, ebp
            0x00b2e85f      pop   ebp
            0x00b2e860      ret
            0x00b2e861      int3
            0x00b2e862      int3
            0x00b2e863      int3
            0x00b2e864      int3
            0x00b2e865      int3
            0x00b2e866      int3
            0x00b2e867      int3
            0x00b2e868      int3
            0x00b2e869      int3
            0x00b2e86a      int3
            0x00b2e86b      int3
            0x00b2e86c      int3
            0x00b2e86d      int3
            0x00b2e86e      int3
            0x00b2e86f      int3
            0x00b2e830      hlt
            0x00b2e831      mov   dword fs:[0x0], ecx
            0x00b2e838      pop   ecx
            0x00b2e839      pop   edi
            0x00b2e83a      pop   esi
            0x00b2e83b      pop   ebx
            0x00b2e83c      mov   esp, ebp
            0x00b2e83e      pop   ebp
            0x00b2e83f      ret
            0x00b2e840      test  esi, esi
        ,=< 0x00b2e842      jz    0xb2e84d
        |   0x00b2e844      mov   eax, dword [esi]
        |   0x00b2e846      mov   ecx, esi
        |   0x00b2e848      push  0x01                                 ; 1
        |   0x00b2e84a      call  dword [eax+0x08]                     ; 8
        `-> 0x00b2e84d      xor   eax, eax
            0x00b2e84f      mov   ecx, dword [ebp-0x0c]
            0x00b2e852      mov   dword fs:[0x0], ecx
            0x00b2e859      pop   ecx
            0x00b2e85a      pop   edi
            0x00b2e85b      pop   esi
            0x00b2e85c      pop   ebx
            0x00b2e85d      mov   esp, ebp
            0x00b2e85f      pop   ebp
            0x00b2e860      ret
            0x00b2e861      int3
            0x00b2e862      int3
            0x00b2e863      int3
            0x00b2e864      int3
            0x00b2e865      int3
            0x00b2e866      int3
            0x00b2e867      int3
            0x00b2e868      int3
            0x00b2e869      int3
            0x00b2e86a      int3
            0x00b2e86b      int3
            0x00b2e86c      int3
            0x00b2e86d      int3
            0x00b2e86e      int3
            0x00b2e86f      int3
            0x00b2e870      push  ebp
            0x00b2e871      mov   ebp, esp
            0x00b2e873      push  0xffffffff                           ; 255
            0x00b2e875      push  0x186932b
            0x00b2e87a      mov   eax, dword fs:[0x0]
            0x00b2e880      push  eax
            0x00b2e881      push  ecx
            0x00b2e882      push  ebx
            0x00b2e883      push  esi
            0x00b2e884      push  edi
            0x00b2e885      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00b2e88a      xor   eax, ebp
            0x00b2e88c      push  eax
            0x00b2e88d      lea   eax, dword [ebp-0x0c]
            0x00b2e890      mov   dword fs:[0x0], eax
            0x00b2e896      push  dword [0x1d6c084]
            0x00b2e89c      push  0x01                                 ; 1
            0x00b2e89e      push  0x20                                 ; 32
            0x00b2e8a0      push  0x01                                 ; 1
            0x00b2e8a2      call  0x529280
            0x00b2e8a7      mov   esi, eax
            0x00b2e8a9      add   esp, 0x10
            0x00b2e8ac      mov   dword [ebp-0x10], esi
            0x00b2e8af      mov   dword [ebp-0x04], 0x00
            0x00b2e8b6      test  esi, esi
        ,=< 0x00b2e8b8      jz    0xb2e8dc
        |   0x00b2e8ba      mov   ecx, esi
        |   0x00b2e8bc      invalid
        |   0x00b2e8bd      lahf
        |   0x00b2e8be      invalid
        |   0x00b2e8bf      invalid
