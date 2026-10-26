            0x00b5a630      push  ecx
            0x00b5a631      test  dword [ecx+0x10], 0x7ffffff
            0x00b5a638      push  edi
            0x00b5a639      lea   edi, dword [ecx+0x10]
        ,=< 0x00b5a63c      jz    0xb5a66a
        |   0x00b5a63e      push  dword [esp+0x0c]
        |   0x00b5a642      call  0x524ca0
        |   0x00b5a647      add   esp, 0x04
        |   0x00b5a64a      lea   ecx, dword [esp+0x04]
        |   0x00b5a64e      push  ecx
        |   0x00b5a64f      push  eax
        |   0x00b5a650      push  dword [esp+0x14]
        |   0x00b5a654      mov   ecx, edi
        |   0x00b5a656      call  0x945d40
        |   0x00b5a65b      mov   eax, dword [esp+0x04]
        |   0x00b5a65f      test  eax, eax
       ,==< 0x00b5a661      jz    0xb5a66a
       ||   0x00b5a663      mov   ecx, dword [edi]
       ||   0x00b5a665      mov   edx, dword [edi+0x04]
      ,===< 0x00b5a668      jmp   0xb5a67c
      |``-> 0x00b5a66a      mov   ecx, dword [edi]
      |     0x00b5a66c      mov   eax, ecx
      |     0x00b5a66e      mov   edx, dword [edi+0x04]
      |     0x00b5a671      and   eax, 0x7ffffff
      |     0x00b5a676      lea   eax, dword [eax+eax*4]
      |     0x00b5a679      lea   eax, dword [edx+eax*4]
      `---> 0x00b5a67c      and   ecx, 0x7ffffff
            0x00b5a682      pop   edi
            0x00b5a683      lea   ecx, dword [ecx+ecx*4]
            0x00b5a686      lea   ecx, dword [edx+ecx*4]
            0x00b5a689      cmp   eax, ecx
        ,=< 0x00b5a68b      jnz   0xb5a693
        |   0x00b5a68d      xor   eax, eax
        |   0x00b5a68f      pop   ecx
        |   0x00b5a690      ret   0x08
        `-> 0x00b5a693      mov   eax, dword [eax+0x10]
            0x00b5a696      pop   ecx
            0x00b5a697      ret   0x08
            0x00b5a69a      int3
            0x00b5a69b      int3
            0x00b5a69c      int3
            0x00b5a69d      int3
            0x00b5a69e      int3
            0x00b5a69f      int3
            0x00b5a6a0      push  ebp
            0x00b5a6a1      mov   ebp, esp
            0x00b5a6a3      push  0xffffffff                           ; 255
            0x00b5a6a5      push  0x186c25c
            0x00b5a6aa      mov   eax, dword fs:[0x0]
            0x00b5a6b0      push  eax
            0x00b5a6b1      push  esi
            0x00b5a6b2      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00b5a6b7      xor   eax, ebp
            0x00b5a6b9      push  eax
            0x00b5a6ba      lea   eax, dword [ebp-0x0c]
            0x00b5a6bd      mov   dword fs:[0x0], eax
            0x00b5a6c3      cmp   dword [0x203b898], 0x02              ; [0x203b898:4]=0
        ,=< 0x00b5a6ca      jz    0xb5a72b
        |   0x00b5a6cc      mov   ecx, 0x01
        |   0x00b5a6d1      mov   esi, 0x203b898
        |   0x00b5a6d6      xor   eax, eax
        |   0x00b5a6d8      lock  cmpxchg dword [esi], ecx
        |   0x00b5a6dc      test  eax, eax
       ,==< 0x00b5a6de      jnz   0xb5a711
       ||   0x00b5a6e0      mov   eax, dword fs:[0x2c]
       ||   0x00b5a6e6      mov   ecx, dword [0x218e080]               ; [0x218e080:4]=0
       ||   0x00b5a6ec      mov   ecx, dword [eax+ecx*4]
       ||   0x00b5a6ef      mov   eax, dword [0x203b8a0]               ; [0x203b8a0:4]=0
       ||   0x00b5a6f4      cmp   eax, dword [ecx+0x04]
      ,===< 0x00b5a6fa      jnle  0xb5a742
    ..----> 0x00b5a6fc      mov   eax, 0x203b89c
    ::|||   0x00b5a701      mov   ecx, 0x203b894
    ::|||   0x00b5a706      xchg  dword [ecx], eax
    ::|||   0x00b5a708      mov   eax, 0x02
    ::|||   0x00b5a70d      xchg  dword [esi], eax
   ,======< 0x00b5a70f      jmp   0xb5a72b
   |::|`--> 0x00b5a711      cmp   dword [0x203b898], 0x02              ; [0x203b898:4]=0
   |::|,==< 0x00b5a718      jz    0xb5a72b
   |::|||   0x00b5a71a      nop   word [eax+eax*1], ax
  .-------> 0x00b5a720      pause
  :|::|||   0x00b5a722      cmp   dword [0x203b898], 0x02              ; [0x203b898:4]=0
  `=======< 0x00b5a729      jnz   0xb5a720
   `---``-> 0x00b5a72b      mov   eax, dword [0x203b894]               ; [0x203b894:4]=0
    ::|     0x00b5a730      mov   eax, dword [eax]
    ::|     0x00b5a732      mov   ecx, dword [ebp-0x0c]
    ::|     0x00b5a735      mov   dword fs:[0x0], ecx
    ::|     0x00b5a73c      pop   ecx
    ::|     0x00b5a73d      pop   esi
    ::|     0x00b5a73e      mov   esp, ebp
    ::|     0x00b5a740      pop   ebp
    ::|     0x00b5a741      ret
    ::`---> 0x00b5a742      push  0x203b8a0
    ::      0x00b5a747      call  0x1806ee7
    ::      0x00b5a74c      add   esp, 0x04
    ::      0x00b5a74f      cmp   dword [0x203b8a0], 0xffffffff        ; [0x203b8a0:4]=0
    `=====< 0x00b5a756      jnz   0xb5a6fc
     :      0x00b5a758      push  str.SavingSystemFreeList             ; 0x19a31f0 ; "SavingSystemFreeList"
     :      0x00b5a75d      mov   ecx, 0x1fcf4c8
     :      0x00b5a762      mov   dword [ebp-0x04], 0x00
     :      0x00b5a769      call  0x517980
     :      0x00b5a76e      push  0x203b8a0
     :      0x00b5a773      mov   dword [0x203b89c], eax
     :      0x00b5a778      call  0x1806e9d
     :      0x00b5a77d      add   esp, 0x04
     `====< 0x00b5a780      jmp   0xb5a6fc
            0x00b5a785      int3
            0x00b5a786      int3
            0x00b5a787      int3
            0x00b5a788      int3
            0x00b5a789      int3
            0x00b5a78a      int3
            0x00b5a78b      int3
            0x00b5a78c      int3
            0x00b5a78d      int3
            0x00b5a78e      int3
            0x00b5a78f      int3
            0x00b5a790      mov   edx, dword [esp+0x04]
            0x00b5a794      push  esi
            0x00b5a795      mov   esi, dword [esp+0x0c]
            0x00b5a799      lea   eax, dword [edx-0x03]
            0x00b5a79c      cmp   eax, 0x05                            ; 5
        ,=< 0x00b5a79f      jnbe  0xb5a7e1
        |   0x00b5a7a1      movss xmm2, dword [ecx+edx*4+0x70]
        |   0x00b5a7a7      lea   eax, dword [edx-0x04]
        |   0x00b5a7aa      movss dword [esi], xmm2
        |   0x00b5a7ae      test  eax, eax
       ,==< 0x00b5a7b0      jnz   0xb5a7b9
       ||   0x00b5a7b2      subss xmm2, dword [ecx+0x44]
      ,===< 0x00b5a7b7      jmp   0xb5a7c7
      |`--> 0x00b5a7b9      movss xmm0, dword [ecx+0x40]
      | |   0x00b5a7be      addss xmm0, dword [ecx+0x3c]
      | |   0x00b5a7c3      subss xmm2, xmm0
      `---> 0x00b5a7c7      movss dword [esi], xmm2
        |   0x00b5a7cb      movaps xmm0, xmm2
        |   0x00b5a7ce      movss xmm1, dword [ecx+0x2c]
        |   0x00b5a7d3      mov   al, 0x01
        |   0x00b5a7d5      minss xmm0, xmm1
        |   0x00b5a7d9      movss dword [esi], xmm0
        |   0x00b5a7dd      pop   esi
        |   0x00b5a7de      ret   0x08
        `-> 0x00b5a7e1      xor   al, al
            0x00b5a7e3      pop   esi
            0x00b5a7e4      ret   0x08
            0x00b5a7e7      int3
            0x00b5a7e8      int3
            0x00b5a7e9      int3
            0x00b5a7ea      int3
            0x00b5a7eb      int3
            0x00b5a7ec      int3
            0x00b5a7ed      int3
            0x00b5a7ee      int3
            0x00b5a7ef      int3
            0x00b5a7f0      mov   edx, ecx
            0x00b5a7f2      mov   ecx, dword [esp+0x04]
            0x00b5a7f6      lea   eax, dword [ecx-0x03]
            0x00b5a7f9      cmp   eax, 0x05                            ; 5
        ,=< 0x00b5a7fc      jnbe  0xb5a80d
        |   0x00b5a7fe      mov   eax, dword [esp+0x08]
        |   0x00b5a802      mov   ecx, dword [edx+ecx*4+0x48]
        |   0x00b5a806      mov   dword [eax], ecx
        |   0x00b5a808      mov   al, 0x01
        |   0x00b5a80a      ret   0x08
        `-> 0x00b5a80d      xor   al, al
            0x00b5a80f      ret   0x08
            0x00b5a812      int3
            0x00b5a813      int3
            0x00b5a814      int3
            0x00b5a815      int3
            0x00b5a816      int3
            0x00b5a817      int3
            0x00b5a818      int3
            0x00b5a819      int3
            0x00b5a81a      int3
            0x00b5a81b      int3
            0x00b5a81c      int3
            0x00b5a81d      int3
            0x00b5a81e      int3
            0x00b5a81f      int3
            0x00b5a820      push  ebp
            0x00b5a821      mov   ebp, esp
            0x00b5a823      push  0xffffffff                           ; 255
            0x00b5a825      push  0x186c2b1
            0x00b5a82a      mov   eax, dword fs:[0x0]
            0x00b5a830      push  eax
            0x00b5a831      sub   esp, 0x14
            0x00b5a834      push  ebx
            0x00b5a835      push  esi
            0x00b5a836      push  edi
            0x00b5a837      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00b5a83c      xor   eax, ebp
            0x00b5a83e      push  eax
            0x00b5a83f      lea   eax, dword [ebp-0x0c]
            0x00b5a842      mov   dword fs:[0x0], eax
            0x00b5a848      mov   esi, ecx
            0x00b5a84a      mov   edi, dword [ebp+0x0c]
            0x00b5a84d      push  edi
            0x00b5a84e      mov   dword [ebp-0x10], 0x00
            0x00b5a855      call  0x4d7b40
            0x00b5a85a      mov   eax, dword [esi+0x10]
            0x00b5a85d      cmp   eax, 0x02                            ; 2
        ,=< 0x00b5a860      jnz   0xb5a8a9
        |   0x00b5a862      mov   ecx, dword [esi+0x1c]
        |   0x00b5a865      lea   edx, dword [ebp-0x20]
        |   0x00b5a868      mov   eax, dword [esi+0x18]
        |   0x00b5a86b      add   ecx, edi
        |   0x00b5a86d      push  edx
        |   0x00b5a86e      call  eax
        |   0x00b5a870      mov   edx, eax
        |   0x00b5a872      mov   dword [ebp-0x18], 0x00
        |   0x00b5a879      lea   eax, dword [ebp-0x18]
        |   0x00b5a87c      mov   dword [ebp-0x14], 0x00
        |   0x00b5a883      cmp   edx, eax
       ,==< 0x00b5a885      jz    0xb5a89f
       ||   0x00b5a887      mov   ecx, dword [edx]
       ||   0x00b5a889      mov   dword [edx], 0x00
       ||   0x00b5a88f      mov   eax, dword [edx+0x04]
       ||   0x00b5a892      mov   dword [ebp-0x18], ecx
       ||   0x00b5a895      mov   dword [ebp-0x14], eax
       ||   0x00b5a898      mov   dword [edx+0x04], 0x00
       `--> 0x00b5a89f      lea   ecx, dword [ebp-0x20]
        |   0x00b5a8a2      call  0x4f9660
       ,==< 0x00b5a8a7      jmp   0xb5a8ef
       |`-> 0x00b5a8a9      cmp   eax, 0x03                            ; 3
       |    0x00b5a8ac      mov   eax, dword [esi+0x18]
       |,=< 0x00b5a8af      jnz   0xb5a8cf
       ||   0x00b5a8b1      mov   ecx, dword [esi+0x1c]
       ||   0x00b5a8b4      add   ecx, edi
       ||   0x00b5a8b6      call  eax
       ||   0x00b5a8b8      mov   dword [ebp-0x18], 0x00
       ||   0x00b5a8bf      invalid
            0x00a69870      sub   esp, 0x18
            0x00a69873      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00a69878      xor   eax, esp
            0x00a6987a      mov   dword [esp+0x14], eax
            0x00a6987e      mov   eax, dword [esp+0x1c]
            0x00a69882      push  ebx
            0x00a69883      push  ebp
            0x00a69884      push  esi
            0x00a69885      push  edi
            0x00a69886      push  eax
            0x00a69887      lea   eax, dword [esp+0x18]
            0x00a6988b      mov   ebx, ecx
            0x00a6988d      push  eax
            0x00a6988e      call  0xb59e80
            0x00a69893      mov   eax, dword [esp+0x1c]
            0x00a69897      lea   ecx, dword [ebx+0x08]
            0x00a6989a      mov   esi, dword [esp+0x20]
            0x00a6989e      lea   edx, dword [esp+0x18]
            0x00a698a2      mov   edi, dword [esp+0x24]
            0x00a698a6      add   esp, 0x08
            0x00a698a9      mov   ebp, dword [esp+0x20]
            0x00a698ad      test  ebx, ebx
            0x00a698af      mov   dword [esp+0x10], eax
            0x00a698b3      mov   eax, 0x18                            ; 24
            0x00a698b8      cmovz ecx, eax
            0x00a698bb      push  0x04                                 ; 4
            0x00a698bd      push  edx
            0x00a698be      mov   ecx, dword [ecx]
            0x00a698c0      mov   eax, dword [ecx]
            0x00a698c2      call  dword [eax+0x1c]                     ; 28
            0x00a698c5      mov   dword [esp+0x10], esi
            0x00a698c9      lea   edx, dword [esp+0x10]
            0x00a698cd      test  ebx, ebx
            0x00a698cf      lea   esi, dword [ebx+0x08]
            0x00a698d2      mov   eax, 0x18                            ; 24
            0x00a698d7      cmovz esi, eax
            0x00a698da      push  0x04                                 ; 4
            0x00a698dc      push  edx
            0x00a698dd      mov   ecx, dword [esi]
            0x00a698df      mov   eax, dword [ecx]
            0x00a698e1      call  dword [eax+0x1c]                     ; 28
            0x00a698e4      mov   ecx, dword [esi]
            0x00a698e6      lea   edx, dword [esp+0x10]
            0x00a698ea      mov   dword [esp+0x10], edi
            0x00a698ee      push  0x04                                 ; 4
            0x00a698f0      push  edx
            0x00a698f1      mov   eax, dword [ecx]
            0x00a698f3      call  dword [eax+0x1c]                     ; 28
            0x00a698f6      mov   ecx, dword [esi]
            0x00a698f8      lea   edx, dword [esp+0x10]
            0x00a698fc      mov   dword [esp+0x10], ebp
            0x00a69900      push  0x04                                 ; 4
            0x00a69902      push  edx
            0x00a69903      mov   eax, dword [ecx]
            0x00a69905      call  dword [eax+0x1c]                     ; 28
            0x00a69908      mov   ecx, dword [esp+0x24]
            0x00a6990c      pop   edi
            0x00a6990d      pop   esi
            0x00a6990e      pop   ebp
            0x00a6990f      pop   ebx
            0x00a69910      xor   ecx, esp
            0x00a69912      call  0x18075f6
            0x00a69917      add   esp, 0x18
            0x00a6991a      ret   0x08
            0x00a6991d      int3
            0x00a6991e      int3
            0x00a6991f      int3
            0x00a69920      sub   esp, 0x18
            0x00a69923      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00a69928      xor   eax, esp
            0x00a6992a      mov   dword [esp+0x14], eax
            0x00a6992e      mov   eax, dword [esp+0x1c]
            0x00a69932      push  ebx
            0x00a69933      push  ebp
            0x00a69934      push  esi
            0x00a69935      push  edi
            0x00a69936      push  eax
            0x00a69937      lea   eax, dword [esp+0x18]
            0x00a6993b      mov   ebp, ecx
            0x00a6993d      push  eax
            0x00a6993e      call  0xb59e80
            0x00a69943      mov   eax, dword [esp+0x1c]
            0x00a69947      add   esp, 0x08
            0x00a6994a      mov   esi, dword [esp+0x18]
            0x00a6994e      mov   edi, dword [esp+0x1c]
            0x00a69952      mov   ebx, dword [esp+0x20]
            0x00a69956      mov   dword [esp+0x10], eax
            0x00a6995a      lea   eax, dword [ebp-0x10]
            0x00a6995d      neg   ebp
            0x00a6995f      push  0x04                                 ; 4
            0x00a69961      sbb   ebp, ebp
            0x00a69963      and   ebp, eax
            0x00a69965      lea   eax, dword [esp+0x14]
            0x00a69969      push  eax
            0x00a6996a      mov   ecx, ebp
            0x00a6996c      call  0xb5ae20
            0x00a69971      push  0x04                                 ; 4
            0x00a69973      lea   eax, dword [esp+0x14]
            0x00a69977      mov   dword [esp+0x14], esi
            0x00a6997b      push  eax
            0x00a6997c      mov   ecx, ebp
            0x00a6997e      call  0xb5ae20
            0x00a69983      push  0x04                                 ; 4
            0x00a69985      lea   eax, dword [esp+0x14]
            0x00a69989      mov   dword [esp+0x14], edi
            0x00a6998d      push  eax
            0x00a6998e      mov   ecx, ebp
            0x00b2f0a0      push  ebp
            0x00b2f0a1      mov   ebp, esp
            0x00b2f0a3      push  0xffffffff                           ; 255
            0x00b2f0a5      push  0x186932b
            0x00b2f0aa      mov   eax, dword fs:[0x0]
            0x00b2f0b0      push  eax
            0x00b2f0b1      push  ecx
            0x00b2f0b2      push  ebx
            0x00b2f0b3      push  esi
            0x00b2f0b4      push  edi
            0x00b2f0b5      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00b2f0ba      xor   eax, ebp
            0x00b2f0bc      push  eax
            0x00b2f0bd      lea   eax, dword [ebp-0x0c]
            0x00b2f0c0      mov   dword fs:[0x0], eax
            0x00b2f0c6      push  dword [0x1d6c084]
            0x00b2f0cc      push  0x01                                 ; 1
            0x00b2f0ce      push  0x1c                                 ; 28
            0x00b2f0d0      push  0x01                                 ; 1
            0x00b2f0d2      call  0x529280
            0x00b2f0d7      mov   esi, eax
            0x00b2f0d9      add   esp, 0x10
            0x00b2f0dc      mov   dword [ebp-0x10], esi
            0x00b2f0df      mov   dword [ebp-0x04], 0x00
            0x00b2f0e6      test  esi, esi
        ,=< 0x00b2f0e8      jz    0xb2f10c
        |   0x00b2f0ea      mov   ecx, esi
        |   0x00b2f0ec      call  0xb21f60
        |   0x00b2f0f1      mov   dword [esi], 0x19a187c               ; [0x19a187c:4]=0x5127a0
        |   0x00b2f0f7      lea   ecx, dword [esi+0x08]
        |   0x00b2f0fa      mov   byte [ebp-0x04], 0x01
        |   0x00b2f0fe      mov   dword [esi+0x04], 0x00
        |   0x00b2f105      call  0x4f71f0
       ,==< 0x00b2f10a      jmp   0xb2f10e
       |`-> 0x00b2f10c      xor   esi, esi
       `--> 0x00b2f10e      mov   edi, dword [ebp+0x08]
            0x00b2f111      lea   ebx, dword [esi+0x04]
            0x00b2f114      push  0x04                                 ; 4
            0x00b2f116      push  ebx
            0x00b2f117      mov   ecx, edi
            0x00b2f119      mov   dword [ebp-0x04], 0xffffffff         ; -1
            0x00b2f120      mov   eax, dword [edi]
            0x00b2f122      mov   eax, dword [eax+0x04]
            0x00b2f125      call  eax
            0x00b2f127      test  al, al
        ,=< 0x00b2f129      jz    0xb2f165
        |   0x00b2f12b      mov   eax, dword [edi]
        |   0x00b2f12d      mov   ecx, edi
        |   0x00b2f12f      push  0x10                                 ; 16
        |   0x00b2f131      mov   edx, dword [eax+0x04]
        |   0x00b2f134      lea   eax, dword [ebx+0x04]
        |   0x00b2f137      push  eax
        |   0x00b2f138      call  edx
        |   0x00b2f13a      test  al, al
       ,==< 0x00b2f13c      jz    0xb2f165
       ||   0x00b2f13e      mov   eax, dword [edi]
       ||   0x00b2f140      mov   ecx, edi
       ||   0x00b2f142      push  0x04                                 ; 4
       ||   0x00b2f144      mov   edx, dword [eax+0x04]
       ||   0x00b2f147      lea   eax, dword [esi+0x18]
       ||   0x00b2f14a      push  eax
       ||   0x00b2f14b      call  edx
       ||   0x00b2f14d      test  al, al
      ,===< 0x00b2f14f      jz    0xb2f165
      |||   0x00b2f151      mov   eax, esi
      |||   0x00b2f153      mov   ecx, dword [ebp-0x0c]
      |||   0x00b2f156      mov   dword fs:[0x0], ecx
      |||   0x00b2f15d      pop   ecx
      |||   0x00b2f15e      pop   edi
      |||   0x00b2f15f      pop   esi
      |||   0x00b2f160      pop   ebx
      |||   0x00b2f161      mov   esp, ebp
      |||   0x00b2f163      pop   ebp
      |||   0x00b2f164      ret
      ```-> 0x00b2f165      test  esi, esi
        ,=< 0x00b2f167      jz    0xb2f172
        |   0x00b2f169      mov   eax, dword [esi]
        |   0x00b2f16b      mov   ecx, esi
        |   0x00b2f16d      push  0x01                                 ; 1
        |   0x00b2f16f      call  dword [eax+0x08]                     ; 8
        `-> 0x00b2f172      xor   eax, eax
            0x00b2f174      mov   ecx, dword [ebp-0x0c]
            0x00b2f177      mov   dword fs:[0x0], ecx
            0x00b2f17e      pop   ecx
            0x00b2f17f      pop   edi
            0x00b2f180      pop   esi
            0x00b2f181      pop   ebx
            0x00b2f182      mov   esp, ebp
            0x00b2f184      pop   ebp
            0x00b2f185      ret
            0x00b2f186      int3
            0x00b2f187      int3
            0x00b2f188      int3
            0x00b2f189      int3
            0x00b2f18a      int3
            0x00b2f18b      int3
            0x00b2f18c      int3
            0x00b2f18d      int3
            0x00b2f18e      int3
            0x00b2f18f      int3
            0x00b2f190      push  ebp
            0x00b2f191      mov   ebp, esp
            0x00b2f193      push  0xffffffff                           ; 255
            0x00b2f195      push  0x1869401
            0x00b2f19a      mov   eax, dword fs:[0x0]
            0x00b2f580      push  ebp
            0x00b2f581      mov   ebp, esp
            0x00b2f583      push  0xffffffff                           ; 255
            0x00b2f585      push  0x186932b
            0x00b2f58a      mov   eax, dword fs:[0x0]
            0x00b2f590      push  eax
            0x00b2f591      push  ecx
            0x00b2f592      push  ebx
            0x00b2f593      push  esi
            0x00b2f594      push  edi
            0x00b2f595      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00b2f59a      xor   eax, ebp
            0x00b2f59c      push  eax
            0x00b2f59d      lea   eax, dword [ebp-0x0c]
            0x00b2f5a0      mov   dword fs:[0x0], eax
            0x00b2f5a6      push  dword [0x1d6c084]
            0x00b2f5ac      push  0x01                                 ; 1
            0x00b2f5ae      push  0x18                                 ; 24
            0x00b2f5b0      push  0x01                                 ; 1
            0x00b2f5b2      call  0x529280
            0x00b2f5b7      mov   edi, eax
            0x00b2f5b9      add   esp, 0x10
            0x00b2f5bc      mov   dword [ebp-0x10], edi
            0x00b2f5bf      mov   dword [ebp-0x04], 0x00
            0x00b2f5c6      test  edi, edi
        ,=< 0x00b2f5c8      jz    0xb2f5ec
        |   0x00b2f5ca      mov   ecx, edi
        |   0x00b2f5cc      call  0xb21f60
        |   0x00b2f5d1      mov   dword [edi], 0x19a19e4               ; [0x19a19e4:4]=0x561c50
        |   0x00b2f5d7      lea   ecx, dword [edi+0x08]
        |   0x00b2f5da      mov   byte [ebp-0x04], 0x01
        |   0x00b2f5de      mov   dword [edi+0x04], 0x00
        |   0x00b2f5e5      call  0x4f71f0
       ,==< 0x00b2f5ea      jmp   0xb2f5ee
       |`-> 0x00b2f5ec      xor   edi, edi
       `--> 0x00b2f5ee      mov   ebx, dword [ebp+0x08]
            0x00b2f5f1      lea   ecx, dword [edi+0x04]
            0x00b2f5f4      push  0x04                                 ; 4
            0x00b2f5f6      push  ecx
            0x00b2f5f7      mov   ecx, ebx
            0x00b2f5f9      mov   dword [ebp-0x04], 0xffffffff         ; -1
            0x00b2f600      mov   eax, dword [ebx]
            0x00b2f602      mov   eax, dword [eax+0x04]
            0x00b2f605      call  eax
            0x00b2f607      test  al, al
        ,=< 0x00b2f609      jz    0xb2f632
        |   0x00b2f60b      mov   edx, dword [ebx]
        |   0x00b2f60d      mov   ecx, ebx
        |   0x00b2f60f      push  0x10                                 ; 16
        |   0x00b2f611      mov   esi, dword [edx+0x04]
        |   0x00b2f614      lea   edx, dword [edi+0x08]
        |   0x00b2f617      push  edx
        |   0x00b2f618      call  esi
        |   0x00b2f61a      test  al, al
       ,==< 0x00b2f61c      jz    0xb2f632
       ||   0x00b2f61e      mov   eax, edi
       ||   0x00b2f620      mov   ecx, dword [ebp-0x0c]
       ||   0x00b2f623      mov   dword fs:[0x0], ecx
       ||   0x00b2f62a      pop   ecx
       ||   0x00b2f62b      pop   edi
       ||   0x00b2f62c      pop   esi
       ||   0x00b2f62d      pop   ebx
       ||   0x00b2f62e      mov   esp, ebp
       ||   0x00b2f630      pop   ebp
       ||   0x00b2f631      ret
       ``-> 0x00b2f632      test  edi, edi
        ,=< 0x00b2f634      jz    0xb2f63f
        |   0x00b2f636      mov   eax, dword [edi]
        |   0x00b2f638      mov   ecx, edi
        |   0x00b2f63a      push  0x01                                 ; 1
        |   0x00b2f63c      call  dword [eax+0x08]                     ; 8
        `-> 0x00b2f63f      xor   eax, eax
            0x00b2f641      mov   ecx, dword [ebp-0x0c]
            0x00b2f644      mov   dword fs:[0x0], ecx
            0x00b2f64b      pop   ecx
            0x00b2f64c      pop   edi
            0x00b2f64d      pop   esi
            0x00b2f64e      pop   ebx
            0x00b2f64f      mov   esp, ebp
            0x00b2f651      pop   ebp
            0x00b2f652      ret
            0x00b2f653      int3
            0x00b2f654      int3
            0x00b2f655      int3
            0x00b2f656      int3
            0x00b2f657      int3
            0x00b2f658      int3
            0x00b2f659      int3
            0x00b2f65a      int3
            0x00b2f65b      int3
            0x00b2f65c      int3
            0x00b2f65d      int3
            0x00b2f65e      int3
            0x00b2f65f      int3
            0x00b2f660      push  ebp
            0x00b2f661      mov   ebp, esp
            0x00b2f663      push  0xffffffff                           ; 255
            0x00b2f665      push  0x1848d23
            0x00b2f66a      mov   eax, dword fs:[0x0]
            0x00b2f670      push  eax
            0x00b2f671      push  ecx
            0x00b2f672      push  esi
            0x00b2f673      push  edi
            0x00b2f674      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00b2f679      xor   eax, ebp
            0x00b2f67b      push  eax
            0x00b2f67c      lea   eax, dword [ebp-0x0c]
            0x00b2f67f      mov   dword fs:[0x0], eax
            0x00b2f685      push  dword [0x1d6c084]
            0x00b2f68b      push  0x01                                 ; 1
            0x00b2f68d      push  0x0c                                 ; 0xc ; 12
            0x00b2f68f      push  0x01                                 ; 1
            0x00b2f691      call  0x529280
            0x00b2f696      mov   esi, eax
            0x00b2f698      add   esp, 0x10
            0x00b2f69b      mov   dword [ebp-0x10], esi
            0x00b2f69e      mov   dword [ebp-0x04], 0x00
            0x00b2f6a5      test  esi, esi
        ,=< 0x00b2f6a7      jz    0xb2f6b8
        |   0x00b2f6a9      mov   ecx, esi
        |   0x00b2f6ab      call  0xb21f60
        |   0x00b2f6b0      mov   dword [esi], 0x19a1aac               ; [0x19a1aac:4]=0x5127a0
       ,==< 0x00b2f6b6      jmp   0xb2f6ba
       |`-> 0x00b2f6b8      xor   esi, esi
       `--> 0x00b2f6ba      mov   edi, dword [ebp+0x08]
            0x00b2f6bd      mov   ecx, edi
            0x00b2f6bf      push  0x04                                 ; 4
            0x00b2f6c1      mov   dword [ebp-0x04], 0xffffffff         ; -1
            0x00b2f6c8      mov   eax, dword [edi]
            0x00b2f6ca      mov   edx, dword [eax+0x04]
            0x00b2f6cd      lea   eax, dword [esi+0x04]
            0x00b2f6d0      push  eax
            0x00b2f6d1      call  edx
            0x00b2f6d3      test  al, al
        ,=< 0x00b2f6d5      jnz   0xb2f6f7
        |   0x00b2f6d7      test  esi, esi
       ,==< 0x00b2f6d9      jz    0xb2f6e4
       ||   0x00b2f6db      mov   eax, dword [esi]
       ||   0x00b2f6dd      mov   ecx, esi
       ||   0x00b2f6df      invalid
            0x00b24100      pushfd
            0x00b24101      mov   ebp, 0xc4830000
            0x00b24106      add   al, 0x5e                             ; 94
            0x00b24108      ret
            0x00b24109      push  esi
            0x00b2410a      call  0xb2f9e0
            0x00b2410f      add   esp, 0x04
            0x00b24112      pop   esi
            0x00b24113      ret
            0x00b24114      push  esi
            0x00b24115      call  0xb2fad0
            0x00b2411a      add   esp, 0x04
            0x00b2411d      pop   esi
            0x00b2411e      ret
            0x00b2411f      push  esi
            0x00b24120      call  0xb2e670
            0x00b24125      add   esp, 0x04
            0x00b24128      pop   esi
            0x00b24129      ret
            0x00b2412a      push  esi
            0x00b2412b      call  0xb30290
            0x00b24130      add   esp, 0x04
            0x00b24133      pop   esi
            0x00b24134      ret
            0x00b24135      push  esi
            0x00b24136      call  0xb303a0
            0x00b2413b      add   esp, 0x04
            0x00b2413e      pop   esi
            0x00b2413f      ret
            0x00b24140      push  esi
            0x00b24141      call  0xb2fdd0
            0x00b24146      add   esp, 0x04
            0x00b24149      pop   esi
            0x00b2414a      ret
            0x00b2414b      push  esi
            0x00b2414c      call  0xb301a0
            0x00b24151      add   esp, 0x04
            0x00b24154      pop   esi
            0x00b24155      ret
            0x00b24156      push  esi
            0x00b24157      call  0xb30570
            0x00b2415c      add   esp, 0x04
            0x00b2415f      pop   esi
            0x00b24160      ret
            0x00b24161      push  esi
            0x00b24162      call  0xb2f580
            0x00b24167      add   esp, 0x04
            0x00b2416a      pop   esi
            0x00b2416b      ret
            0x00b2416c      push  esi
            0x00b2416d      call  0xb2f3b0
            0x00b24172      add   esp, 0x04
            0x00b24175      pop   esi
            0x00b24176      ret
            0x00b24177      push  esi
            0x00b24178      call  0xb2f2e0
            0x00b2417d      add   esp, 0x04
            0x00b24180      pop   esi
            0x00b24181      ret
            0x00b24182      push  esi
            0x00b24183      call  0xb2f720
            0x00b24188      add   esp, 0x04
            0x00b2418b      pop   esi
            0x00b2418c      ret
            0x00b2418d      push  esi
            0x00b2418e      call  0xb2e980
            0x00b24193      add   esp, 0x04
            0x00b24196      pop   esi
            0x00b24197      ret
            0x00b24198      push  esi
            0x00b24199      call  0xb2ea50
            0x00b2419e      add   esp, 0x04
            0x00b241a1      pop   esi
            0x00b241a2      ret
            0x00b241a3      push  esi
            0x00b241a4      call  0xb2ec60
            0x00b241a9      add   esp, 0x04
            0x00b241ac      pop   esi
            0x00b241ad      ret
            0x00b241ae      push  esi
            0x00b241af      call  0xb2fcd0
            0x00b241b4      add   esp, 0x04
            0x00b241b7      pop   esi
            0x00b241b8      ret
            0x00b241b9      push  esi
            0x00b241ba      call  0xb2eb20
            0x00b241bf      add   esp, 0x04
            0x00b241c2      pop   esi
            0x00b241c3      ret
            0x00b241c4      push  esi
            0x00b241c5      call  0xb2ed10
            0x00b241ca      add   esp, 0x04
            0x00b241cd      pop   esi
            0x00b241ce      ret
            0x00b241cf      push  esi
            0x00b241d0      call  0xb2f660
            0x00b241d5      add   esp, 0x04
            0x00b241d8      pop   esi
            0x00b241d9      ret
            0x00b241da      push  esi
            0x00b241db      call  0xb300e0
            0x00b241e0      add   esp, 0x04
            0x00b241e3      pop   esi
            0x00b241e4      ret
            0x00b241e5      push  esi
            0x00b241e6      call  0xb2ff50
            0x00b241eb      add   esp, 0x04
            0x00b241ee      pop   esi
            0x00b241ef      ret
            0x00b241f0      xor   eax, eax
            0x00b241f2      pop   esi
            0x00b241f3      ret
            0x00b241f4      test  dword [eax-0x4e], eax
            0x00b241f7      add   byte [eax-0x64ff4dc0], dl
            0x00b241fd      inc   eax
            0x00b241fe      mov   dl, 0x00
            0x00b24200      cmpsb
            0x00b24201      inc   eax
            0x00b24202      mov   dl, 0x00
            0x00b24204      mov   cl, 0x40                             ; '@' ; 64
            0x00b24206      mov   dl, 0x00
            0x00b24208      mov   esp, 0xc700b240
            0x00b2420d      inc   eax
            0x00b2420e      mov   dl, 0x00
            0x00b24210      rol   byte [eax-0x4e], cl
            0x00b24213      add   ch, bl
            0x00b24215      inc   eax
            0x00b24216      mov   dl, 0x00
            0x00b24218      call  0xfffffffff3b2f45d
            0x00b2421d      inc   eax
            0x00b2421e      mov   dl, 0x00
            0x00c07290      push  ebx
            0x00c07291      push  esi
            0x00c07292      mov   esi, dword [esp+0x10]
            0x00c07296      push  edi
            0x00c07297      mov   edi, ecx
            0x00c07299      mov   ebx, dword [edi+0x0c]
            0x00c0729c      mov   eax, dword [edi+0x08]
            0x00c0729f      imul  edx, ebx, 0xb4
            0x00c072a5      add   edx, eax
            0x00c072a7      cmp   eax, edx
        ,=< 0x00c072a9      jz    0xc072c3
        |   0x00c072ab      nop   dword [eax+eax*1], eax
       .--> 0x00c072b0      cmp   dword [eax], 0x3e                    ; '>'
      ,===< 0x00c072b3      jnz   0xc072ba
      |:|   0x00c072b5      cmp   dword [eax+0x04], esi
     ,====< 0x00c072b8      jz    0xc072f3
     |`---> 0x00c072ba      add   eax, 0xb4                            ; 180
     | :|   0x00c072bf      cmp   eax, edx
     | `==< 0x00c072c1      jnz   0xc072b0
     | .`-> 0x00c072c3      cmp   ebx, dword [edi]
     | :,=< 0x00c072c5      jnz   0xc072cc
     | :|   0x00c072c7      call  0x9d6ad0
     | :`-> 0x00c072cc      imul  ecx, ebx, 0xb4
     | :    0x00c072d2      lea   eax, dword [ebx+0x01]
     | :    0x00c072d5      mov   dword [edi+0x0c], eax
     | :    0x00c072d8      mov   eax, dword [esp+0x10]
     | :    0x00c072dc      add   ecx, dword [edi+0x08]
     | :    0x00c072df      pop   edi
     | :    0x00c072e0      mov   dword [ecx+0x04], esi
     | :    0x00c072e3      mov   dword [ecx], 0x3e                    ; '>'
     | :                                                               ; [0x3e:4]=-1 ; 62
     | :    0x00c072e9      mov   eax, dword [eax]
     | :    0x00c072eb      pop   esi
     | :    0x00c072ec      mov   dword [ecx+0x08], eax
     | :    0x00c072ef      pop   ebx
     | :    0x00c072f0      ret   0x08
     `----> 0x00c072f3      cmp   eax, edx
       `==< 0x00c072f5      jz    0xc072c3
            0x00c072f7      mov   ecx, dword [esp+0x10]
            0x00c072fb      pop   edi
            0x00c072fc      pop   esi
            0x00c072fd      pop   ebx
            0x00c072fe      mov   ecx, dword [ecx]
            0x00c07300      mov   dword [eax+0x08], ecx
            0x00c07303      ret   0x08
            0x00c07306      int3
            0x00c07307      int3
            0x00c07308      int3
            0x00c07309      int3
            0x00c0730a      int3
            0x00c0730b      int3
            0x00c0730c      int3
            0x00c0730d      int3
            0x00c0730e      int3
            0x00c0730f      int3
            0x00c07310      push  ebx
            0x00c07311      push  esi
            0x00c07312      mov   esi, ecx
            0x00c07314      push  edi
            0x00c07315      mov   edi, dword [esp+0x14]
            0x00c07319      mov   ebx, dword [esi+0x0c]
            0x00c0731c      mov   eax, dword [esi+0x08]
            0x00c0731f      imul  edx, ebx, 0xb4
            0x00c07325      add   edx, eax
            0x00c07327      cmp   eax, edx
        ,=< 0x00c07329      jz    0xc07343
        |   0x00c0732b      nop   dword [eax+eax*1], eax
       .--> 0x00c07330      cmp   dword [eax], 0x69                    ; 'i'
      ,===< 0x00c07333      jnz   0xc0733a
      |:|   0x00c07335      cmp   dword [eax+0x04], edi
     ,====< 0x00c07338      jz    0xc07371
     |`---> 0x00c0733a      add   eax, 0xb4                            ; 180
     | :|   0x00c0733f      cmp   eax, edx
     | `==< 0x00c07341      jnz   0xc07330
     | .`-> 0x00c07343      cmp   ebx, dword [esi]
     | :,=< 0x00c07345      jnz   0xc0734c
     | :|   0x00c07347      call  0x9d6ad0
     | :`-> 0x00c0734c      imul  ecx, ebx, 0xb4
     | :    0x00c07352      lea   eax, dword [ebx+0x01]
     | :    0x00c07355      mov   dword [esi+0x0c], eax
     | :    0x00c07358      mov   eax, dword [esp+0x10]
     | :    0x00c0735c      add   ecx, dword [esi+0x08]
     | :    0x00c0735f      mov   dword [ecx+0x04], edi
     | :    0x00c07362      pop   edi
     | :    0x00c07363      pop   esi
     | :    0x00c07364      mov   dword [ecx], 0x69                    ; 'i'
     | :                                                               ; [0x69:4]=-1 ; 105
     | :    0x00c0736a      mov   dword [ecx+0x08], eax
     | :    0x00c0736d      pop   ebx
     | :    0x00c0736e      ret   0x08
     `----> 0x00c07371      cmp   eax, edx
       `==< 0x00c07373      jz    0xc07343
            0x00c07375      mov   ecx, dword [esp+0x10]
            0x00c07379      pop   edi
            0x00c0737a      pop   esi
            0x00c0737b      mov   dword [eax+0x08], ecx
            0x00c0737e      pop   ebx
            0x00c0737f      ret   0x08
            0x00c07382      int3
            0x00c07383      int3
            0x00c07384      int3
            0x00c07385      int3
            0x00c07386      int3
            0x00c07387      int3
            0x00c07388      int3
            0x00c07389      int3
            0x00c0738a      int3
            0x00c0738b      int3
            0x00c0738c      int3
            0x00c0738d      int3
            0x00c0738e      int3
            0x00c0738f      int3
            0x00c07390      push  ebx
            0x00c07391      push  esi
            0x00c07392      mov   esi, ecx
            0x00c07394      push  edi
            0x00c07395      mov   edi, dword [esp+0x14]
            0x00c07399      mov   ebx, dword [esi+0x0c]
            0x00c0739c      mov   eax, dword [esi+0x08]
            0x00c0739f      imul  edx, ebx, 0xb4
            0x00c073a5      add   edx, eax
            0x00c073a7      cmp   eax, edx
        ,=< 0x00c073a9      jz    0xc073c3
        |   0x00c073ab      nop   dword [eax+eax*1], eax
        |   0x00c073b0      cmp   dword [eax], 0x6b                    ; 'k'
       ,==< 0x00c073b3      jnz   0xc073ba
       ||   0x00c073b5      cmp   dword [eax+0x04], edi
      ,===< 0x00c073b8      jz    0xc073f1
      |`--> 0x00c073ba      add   eax, 0xb4                            ; 180
      | |   0x00c073bf      invalid
            0x00c07310      push  ebx
            0x00c07311      push  esi
            0x00c07312      mov   esi, ecx
            0x00c07314      push  edi
            0x00c07315      mov   edi, dword [esp+0x14]
            0x00c07319      mov   ebx, dword [esi+0x0c]
            0x00c0731c      mov   eax, dword [esi+0x08]
            0x00c0731f      imul  edx, ebx, 0xb4
            0x00c07325      add   edx, eax
            0x00c07327      cmp   eax, edx
        ,=< 0x00c07329      jz    0xc07343
        |   0x00c0732b      nop   dword [eax+eax*1], eax
       .--> 0x00c07330      cmp   dword [eax], 0x69                    ; 'i'
      ,===< 0x00c07333      jnz   0xc0733a
      |:|   0x00c07335      cmp   dword [eax+0x04], edi
     ,====< 0x00c07338      jz    0xc07371
     |`---> 0x00c0733a      add   eax, 0xb4                            ; 180
     | :|   0x00c0733f      cmp   eax, edx
     | `==< 0x00c07341      jnz   0xc07330
     | .`-> 0x00c07343      cmp   ebx, dword [esi]
     | :,=< 0x00c07345      jnz   0xc0734c
     | :|   0x00c07347      call  0x9d6ad0
     | :`-> 0x00c0734c      imul  ecx, ebx, 0xb4
     | :    0x00c07352      lea   eax, dword [ebx+0x01]
     | :    0x00c07355      mov   dword [esi+0x0c], eax
     | :    0x00c07358      mov   eax, dword [esp+0x10]
     | :    0x00c0735c      add   ecx, dword [esi+0x08]
     | :    0x00c0735f      mov   dword [ecx+0x04], edi
     | :    0x00c07362      pop   edi
     | :    0x00c07363      pop   esi
     | :    0x00c07364      mov   dword [ecx], 0x69                    ; 'i'
     | :                                                               ; [0x69:4]=-1 ; 105
     | :    0x00c0736a      mov   dword [ecx+0x08], eax
     | :    0x00c0736d      pop   ebx
     | :    0x00c0736e      ret   0x08
     `----> 0x00c07371      cmp   eax, edx
       `==< 0x00c07373      jz    0xc07343
            0x00c07375      mov   ecx, dword [esp+0x10]
            0x00c07379      pop   edi
            0x00c0737a      pop   esi
            0x00c0737b      mov   dword [eax+0x08], ecx
            0x00c0737e      pop   ebx
            0x00c0737f      ret   0x08
            0x00c07382      int3
            0x00c07383      int3
            0x00c07384      int3
            0x00c07385      int3
            0x00c07386      int3
            0x00c07387      int3
            0x00c07388      int3
            0x00c07389      int3
            0x00c0738a      int3
            0x00c0738b      int3
            0x00c0738c      int3
            0x00c0738d      int3
            0x00c0738e      int3
            0x00c0738f      int3
            0x00c07390      push  ebx
            0x00c07391      push  esi
            0x00c07392      mov   esi, ecx
            0x00c07394      push  edi
            0x00c07395      mov   edi, dword [esp+0x14]
            0x00c07399      mov   ebx, dword [esi+0x0c]
            0x00c0739c      mov   eax, dword [esi+0x08]
            0x00c0739f      imul  edx, ebx, 0xb4
            0x00c073a5      add   edx, eax
            0x00c073a7      cmp   eax, edx
        ,=< 0x00c073a9      jz    0xc073c3
        |   0x00c073ab      nop   dword [eax+eax*1], eax
       .--> 0x00c073b0      cmp   dword [eax], 0x6b                    ; 'k'
      ,===< 0x00c073b3      jnz   0xc073ba
      |:|   0x00c073b5      cmp   dword [eax+0x04], edi
     ,====< 0x00c073b8      jz    0xc073f1
     |`---> 0x00c073ba      add   eax, 0xb4                            ; 180
     | :|   0x00c073bf      cmp   eax, edx
     | `==< 0x00c073c1      jnz   0xc073b0
     | .`-> 0x00c073c3      cmp   ebx, dword [esi]
     | :,=< 0x00c073c5      jnz   0xc073cc
     | :|   0x00c073c7      call  0x9d6ad0
     | :`-> 0x00c073cc      imul  ecx, ebx, 0xb4
     | :    0x00c073d2      lea   eax, dword [ebx+0x01]
     | :    0x00c073d5      mov   dword [esi+0x0c], eax
     | :    0x00c073d8      mov   eax, dword [esp+0x10]
     | :    0x00c073dc      add   ecx, dword [esi+0x08]
     | :    0x00c073df      mov   dword [ecx+0x04], edi
     | :    0x00c073e2      pop   edi
     | :    0x00c073e3      pop   esi
     | :    0x00c073e4      mov   dword [ecx], 0x6b                    ; 'k'
     | :                                                               ; [0x6b:4]=-1 ; 107
     | :    0x00c073ea      mov   dword [ecx+0x08], eax
     | :    0x00c073ed      pop   ebx
     | :    0x00c073ee      ret   0x08
     `----> 0x00c073f1      cmp   eax, edx
       `==< 0x00c073f3      jz    0xc073c3
            0x00c073f5      mov   ecx, dword [esp+0x10]
            0x00c073f9      pop   edi
            0x00c073fa      pop   esi
            0x00c073fb      mov   dword [eax+0x08], ecx
            0x00c073fe      pop   ebx
            0x00c073ff      ret   0x08
            0x00c07402      int3
            0x00c07403      int3
            0x00c07404      int3
            0x00c07405      int3
            0x00c07406      int3
            0x00c07407      int3
            0x00c07408      int3
            0x00c07409      int3
            0x00c0740a      int3
            0x00c0740b      int3
            0x00c0740c      int3
            0x00c0740d      int3
            0x00c0740e      int3
            0x00c0740f      int3
            0x00c07410      push  ebp
            0x00c07411      mov   ebp, esp
            0x00c07413      push  0xffffffff                           ; 255
            0x00c07415      push  0x1876168
            0x00c0741a      mov   eax, dword fs:[0x0]
            0x00c07420      push  eax
            0x00c07421      sub   esp, 0x30
            0x00c07424      push  esi
            0x00c07425      push  edi
            0x00c07426      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00c0742b      xor   eax, ebp
            0x00c0742d      push  eax
            0x00c0742e      lea   eax, dword [ebp-0x0c]
            0x00c07431      mov   dword fs:[0x0], eax
            0x00c07437      mov   edi, ecx
            0x00c07439      mov   dword [ebp-0x24], edi
            0x00c0743c      mov   eax, dword [edi]
            0x00c0743e      mov   esi, eax
            0x00c07440      mov   edx, dword [ebp+0x08]
            0x00c07443      mov   ecx, eax
            0x00c07445      mov   dword [ebp-0x1c], eax
            0x00c07448      and   esi, 0x7ffffff
            0x00c0744e      invalid
            0x00c0744f      invalid
