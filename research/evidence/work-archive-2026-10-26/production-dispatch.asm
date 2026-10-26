            0x00b2d0a0      push  esi
            0x00b2d0a1      mov   esi, dword [ecx+0x04]
            0x00b2d0a4      mov   ecx, esi
            0x00b2d0a6      mov   eax, dword [esi]
            0x00b2d0a8      mov   eax, dword [eax+0x24]
            0x00b2d0ab      call  eax
            0x00b2d0ad      test  al, al
        ,=< 0x00b2d0af      jz    0xb2d0cc
        |   0x00b2d0b1      mov   eax, dword [esi]
        |   0x00b2d0b3      mov   ecx, esi
        |   0x00b2d0b5      call  dword [eax+0x20]                     ; 32
        |   0x00b2d0b8      push  0x00
        |   0x00b2d0ba      push  0x00
        |   0x00b2d0bc      push  esi
        |   0x00b2d0bd      mov   ecx, eax
        |   0x00b2d0bf      call  0xba5520
        |   0x00b2d0c4      mov   eax, dword [esi]
        |   0x00b2d0c6      mov   ecx, esi
        |   0x00b2d0c8      push  0x01                                 ; 1
        |   0x00b2d0ca      call  dword [eax]
        `-> 0x00b2d0cc      pop   esi
            0x00b2d0cd      ret   0x08
            0x00b2d0d0      push  dword [ecx+0x04]
            0x00b2d0d3      call  0xcfd310
            0x00b2d0d8      ret   0x08
            0x00b2d0db      int3
            0x00b2d0dc      int3
            0x00b2d0dd      int3
            0x00b2d0de      int3
            0x00b2d0df      int3
            0x00b2d0e0      mov   edx, ecx
            0x00b2d0e2      sub   esp, 0x14
            0x00b2d0e5      mov   ecx, esp
            0x00b2d0e7      mov   eax, dword [edx+0x04]
            0x00b2d0ea      mov   dword [ecx], eax
            0x00b2d0ec      lea   eax, dword [edx+0x08]
            0x00b2d0ef      push  eax
            0x00b2d0f0      add   ecx, 0x04
            0x00b2d0f3      call  0x4f70d0
            0x00b2d0f8      push  dword [esp+0x1c]
            0x00b2d0fc      push  dword [esp+0x1c]
            0x00b2d100      call  0xb2e4f0
            0x00b2d105      mov   ecx, dword [0x201e2dc]               ; [0x201e2dc:4]=0
            0x00b2d10b      add   esp, 0x1c
            0x00b2d10e      push  eax
            0x00b2d10f      call  0xbb4e00
            0x00b2d114      ret   0x08
            0x00b2d117      int3
            0x00b2d118      int3
            0x00b2d119      int3
            0x00b2d11a      int3
            0x00b2d11b      int3
            0x00b2d11c      int3
            0x00b2d11d      int3
            0x00b2d11e      int3
            0x00b2d11f      int3
            0x00b2d120      push  ebp
            0x00b2d121      mov   ebp, esp
            0x00b2d123      push  0xffffffff                           ; 255
            0x00b2d125      push  0x1868ec8
            0x00b2d12a      mov   eax, dword fs:[0x0]
            0x00b2d130      push  eax
            0x00b2d131      sub   esp, 0x10
            0x00b2d134      push  esi
            0x00b2d135      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00b2d13a      xor   eax, ebp
            0x00b2d13c      push  eax
            0x00b2d13d      lea   eax, dword [ebp-0x0c]
            0x00b2d140      mov   dword fs:[0x0], eax
            0x00b2d146      mov   esi, ecx
            0x00b2d148      lea   eax, dword [esi+0x04]
            0x00b2d14b      push  eax
            0x00b2d14c      push  dword [ebp+0x0c]
            0x00b2d14f      lea   eax, dword [ebp-0x1c]
            0x00b2d152      push  dword [ebp+0x08]
            0x00b2d155      push  eax
            0x00b2d156      call  0xb2e270
            0x00b2d15b      add   esp, 0x10
            0x00b2d15e      push  eax
            0x00b2d15f      mov   ecx, esi
            0x00b2d161      mov   dword [ebp-0x04], 0x00
            0x00b2d168      call  0xcfd340
            0x00b2d16d      cmp   dword [ebp-0x1c], 0x00
            0x00b2d171      mov   dword [ebp-0x04], 0x01
            0x00b2d178      mov   dword [ebp-0x10], 0x00
        ,=< 0x00b2d17f      jz    0xb2d18e
        |   0x00b2d181      push  dword [ebp-0x14]
        |   0x00b2d184      push  0x00
        |   0x00b2d186      call  0x5291c0
        |   0x00b2d18b      add   esp, 0x08
        `-> 0x00b2d18e      mov   ecx, dword [ebp-0x0c]
            0x00b2d191      mov   dword fs:[0x0], ecx
            0x00b2d198      pop   ecx
            0x00b2d199      pop   esi
            0x00b2d19a      mov   esp, ebp
            0x00b2d19c      pop   ebp
            0x00b2d19d      ret   0x08
            0x00b2d1a0      sub   esp, 0x10
            0x00b2d1a3      push  esi
            0x00b2d1a4      push  edi
            0x00b2d1a5      mov   edi, ecx
            0x00b2d1a7      sub   esp, 0x14
            0x00b2d1aa      mov   ecx, esp
            0x00b2d1ac      mov   eax, dword [edi+0x04]
            0x00b2d1af      mov   dword [ecx], eax
            0x00b2d1b1      lea   eax, dword [edi+0x08]
            0x00b2d1b4      push  eax
            0x00b2d1b5      add   ecx, 0x04
            0x00b2d1b8      call  0x4f70d0
            0x00b2d1bd      push  dword [esp+0x34]
            0x00b2d1c1      push  dword [esp+0x34]
            0x00b2d1c5      call  0xb2e4f0
            0x00b2d1ca      add   esp, 0x1c
            0x00b2d1cd      lea   ecx, dword [edi+0x18]
            0x00b2d1d0      mov   esi, eax
            0x00b2d1d2      push  ecx
            0x00b2d1d3      lea   ecx, dword [esp+0x0c]
            0x00b2d1d7      call  0x4f70d0
            0x00b2d1dc      sub   esp, 0x10
            0x00b2d1df      lea   eax, dword [esp+0x18]
            0x00b2d1e3      mov   ecx, esp
            0x00b2d1e5      push  eax
            0x00b2d1e6      call  0x4f70d0
            0x00b2d1eb      push  esi
            0x00b2d1ec      mov   ecx, edi
            0x00b2d1ee      invalid
            0x00b2d1ef      lodsd
            0x00b2c390      sub   esp, 0x24
            0x00b2c393      push  ebx
            0x00b2c394      mov   ebx, ecx
            0x00b2c396      lea   ecx, dword [esp+0x04]
            0x00b2c39a      push  esi
            0x00b2c39b      push  edi
            0x00b2c39c      mov   edi, dword [ebx+0x28]
            0x00b2c39f      lea   eax, dword [ebx+0x18]
            0x00b2c3a2      push  eax
            0x00b2c3a3      call  0x4f70d0
            0x00b2c3a8      lea   eax, dword [esp+0x0c]
            0x00b2c3ac      push  0x01                                 ; 1
            0x00b2c3ae      push  eax
            0x00b2c3af      call  0xb5abd0
            0x00b2c3b4      mov   ecx, dword [ebx+0x04]
            0x00b2c3b7      add   esp, 0x08
            0x00b2c3ba      mov   dword [esp+0x1c], ecx
            0x00b2c3be      mov   esi, eax
            0x00b2c3c0      lea   ecx, dword [ebx+0x08]
            0x00b2c3c3      push  ecx
            0x00b2c3c4      lea   ecx, dword [esp+0x24]
            0x00b2c3c8      call  0x4f70d0
            0x00b2c3cd      mov   eax, dword [esp+0x1c]
            0x00b2c3d1      sub   esp, 0x14
            0x00b2c3d4      mov   ecx, esp
            0x00b2c3d6      mov   dword [ecx], eax
            0x00b2c3d8      lea   eax, dword [esp+0x34]
            0x00b2c3dc      push  eax
            0x00b2c3dd      add   ecx, 0x04
            0x00b2c3e0      call  0x4f70d0
            0x00b2c3e5      push  dword [esp+0x4c]
            0x00b2c3e9      push  dword [esp+0x4c]
            0x00b2c3ed      call  0xb28a70
            0x00b2c3f2      add   esp, 0x1c
            0x00b2c3f5      mov   ecx, ebx
            0x00b2c3f7      push  edi
            0x00b2c3f8      push  esi
            0x00b2c3f9      push  eax
            0x00b2c3fa      call  0xb245c0
            0x00b2c3ff      pop   edi
            0x00b2c400      pop   esi
            0x00b2c401      pop   ebx
            0x00b2c402      add   esp, 0x24
            0x00b2c405      ret   0x08
            0x00b2c408      int3
            0x00b2c409      int3
            0x00b2c40a      int3
            0x00b2c40b      int3
            0x00b2c40c      int3
            0x00b2c40d      int3
            0x00b2c40e      int3
            0x00b2c40f      int3
            0x00b2c410      sub   esp, 0x14
            0x00b2c413      push  ebx
            0x00b2c414      mov   ebx, ecx
            0x00b2c416      lea   ecx, dword [esp+0x08]
            0x00b2c41a      push  esi
            0x00b2c41b      push  edi
            0x00b2c41c      mov   eax, dword [ebx+0x04]
            0x00b2c41f      invalid
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
            0x00b2c75d      invalid
            0x00b2c75e      push  cs
            0x00b2c75f      ret
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
            0x00b2d01d      invalid
            0x00b2d01e      inc   esp
            0x00b2d01f      invalid
            0x00c08340      push  ebp
            0x00c08341      mov   ebp, esp
            0x00c08343      push  0xffffffff                           ; 255
            0x00c08345      push  0x1876198
            0x00c0834a      mov   eax, dword fs:[0x0]
            0x00c08350      push  eax
            0x00c08351      push  ecx
            0x00c08352      push  esi
            0x00c08353      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00c08358      xor   eax, ebp
            0x00c0835a      push  eax
            0x00c0835b      lea   eax, dword [ebp-0x0c]
            0x00c0835e      mov   dword fs:[0x0], eax
            0x00c08364      mov   esi, ecx
            0x00c08366      mov   dword [ebp-0x10], esi
            0x00c08369      call  0xb4e0d0
            0x00c0836e      lea   ecx, dword [esi+0x0c]
            0x00c08371      mov   dword [ebp-0x04], 0x00
            0x00c08378      mov   dword [esi], 0x19b0180               ; [0x19b0180:4]=0xc091b0
            0x00c0837e      mov   dword [esi+0x08], 0x00
            0x00c08385      call  0xb43a40
            0x00c0838a      mov   dword [esi+0x5c], 0x00
            0x00c08391      mov   eax, esi
            0x00c08393      mov   dword [esi+0x60], 0x00
            0x00c0839a      mov   dword [esi+0x64], 0x00
            0x00c083a1      mov   dword [esi+0x68], 0x00
            0x00c083a8      mov   dword [esi+0x6c], 0x00
            0x00c083af      mov   dword [esi+0x70], 0x00
            0x00c083b6      mov   dword [esi+0x84], 0x00
            0x00c083c0      mov   dword [esi+0x88], 0x00
            0x00c083ca      mov   dword [esi+0x8c], 0x00
            0x00c083d4      mov   dword [esi+0x90], 0x00
            0x00c083de      mov   word [esi+0x94], 0x00
            0x00c083e7      mov   byte [esi+0x96], 0x01
            0x00c083ee      mov   dword [esi+0x9c], 0x00
            0x00c083f8      mov   dword [esi+0xa4], 0x00
            0x00c08402      mov   dword [esi+0xa8], 0x00
            0x00c0840c      mov   dword [esi+0x04], 0x00
            0x00c08413      mov   ecx, dword [ebp-0x0c]
            0x00c08416      mov   dword fs:[0x0], ecx
            0x00c0841d      pop   ecx
            0x00c0841e      pop   esi
            0x00c0841f      mov   esp, ebp
            0x00c08421      pop   ebp
            0x00c08422      ret
            0x00c08423      int3
            0x00c08424      int3
            0x00c08425      int3
            0x00c08426      int3
            0x00c08427      int3
            0x00c08428      int3
            0x00c08429      int3
            0x00c0842a      int3
            0x00c0842b      int3
            0x00c0842c      int3
            0x00c0842d      int3
            0x00c0842e      int3
            0x00c0842f      int3
            0x00c08430      push  ebp
            0x00c08431      mov   ebp, esp
            0x00c08433      push  0xffffffff                           ; 255
            0x00c08435      push  0x1876236
            0x00c0843a      mov   eax, dword fs:[0x0]
            0x00c08440      push  eax
            0x00c08441      sub   esp, 0x08
            0x00c08444      push  esi
            0x00c08445      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00c0844a      xor   eax, ebp
            0x00c0844c      push  eax
            0x00c0844d      lea   eax, dword [ebp-0x0c]
            0x00c08450      mov   dword fs:[0x0], eax
            0x00c08456      mov   esi, ecx
            0x00c08458      mov   dword [ebp-0x10], esi
            0x00c0845b      call  0xaac0b0
            0x00c08460      mov   dword [esi], 0x19b0400               ; [0x19b0400:4]=0xc09380
            0x00c08466      mov   dword [esi+0x2c], 0x00
            0x00c0846d      mov   dword [esi+0x30], 0x0a
            0x00c08474      mov   dword [esi+0x38], 0x00
            0x00c0847b      mov   dword [ebp-0x04], 0x00
            0x00c08482      mov   dword [esi+0x40], 0x00
            0x00c08489      mov   dword [esi+0x44], 0x00
            0x00c08490      mov   byte [esi+0x48], 0x00
            0x00c08494      mov   dword [esi+0x4c], 0x04
            0x00c0849b      mov   dword [esi+0x50], 0x09
            0x00c084a2      push  dword [0x1d6c084]
            0x00c084a8      mov   byte [ebp-0x04], 0x01
            0x00c084ac      push  0x01                                 ; 1
            0x00c084ae      push  0x2c                                 ; ',' ; 44
            0x00c084b0      push  0x01                                 ; 1
            0x00c084b2      call  0x529280
            0x00c084b7      add   esp, 0x10
            0x00c084ba      mov   dword [ebp-0x14], eax
            0x00c084bd      mov   byte [ebp-0x04], 0x02
            0x00c084c1      test  eax, eax
        ,=< 0x00c084c3      jz    0xc084e1
        |   0x00c084c5      mov   ecx, eax
        |   0x00c084c7      call  0xca5b80
        |   0x00c084cc      mov   dword [esi+0x2c], eax
        |   0x00c084cf      mov   eax, esi
        |   0x00c084d1      mov   ecx, dword [ebp-0x0c]
        |   0x00c084d4      mov   dword fs:[0x0], ecx
        |   0x00c084db      pop   ecx
        |   0x00c084dc      pop   esi
        |   0x00c084dd      mov   esp, ebp
        |   0x00c084df      pop   ebp
        |   0x00c084e0      ret
        `-> 0x00c084e1      mov   dword [esi+0x2c], 0x00
            0x00c084e8      mov   eax, esi
            0x00c084ea      mov   ecx, dword [ebp-0x0c]
            0x00c084ed      mov   dword fs:[0x0], ecx
            0x00c084f4      pop   ecx
            0x00c084f5      pop   esi
            0x00c084f6      mov   esp, ebp
            0x00c084f8      pop   ebp
            0x00c084f9      ret
            0x00c084fa      int3
            0x00c084fb      int3
            0x00c084fc      int3
            0x00c084fd      int3
            0x00c084fe      int3
            0x00c084ff      int3
            0x00c08500      push  ebp
            0x00c08501      mov   ebp, esp
            0x00c08503      push  0xffffffff                           ; 255
            0x00c08505      push  0x180ca50
            0x00c0850a      mov   eax, dword fs:[0x0]
            0x00c08510      push  eax
            0x00c08511      push  ebx
            0x00c08512      push  esi
            0x00c08513      push  edi
            0x00c08514      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00c08519      xor   eax, ebp
            0x00c0851b      push  eax
            0x00c0851c      lea   eax, dword [ebp-0x0c]
            0x00c0851f      mov   dword fs:[0x0], eax
            0x00c08525      mov   edi, ecx
            0x00c08527      mov   ebx, dword [edi+0x10]
            0x00c0852a      mov   ecx, dword [edi+0x0c]
            0x00c0852d      test  ebx, ebx
        ,=< 0x00c0852f      jz    0xc08567
        |   0x00c08531      lea   eax, dword [ebx+ebx*2]
        |   0x00c08534      shl   eax, 0x04
        |   0x00c08537      lea   esi, dword [ecx-0x10]
        |   0x00c0853a      add   esi, eax
        |   0x00c0853c      nop   dword [eax], eax
            0x00c080e0      push  ebp
            0x00c080e1      mov   ebp, esp
            0x00c080e3      push  0xffffffff                           ; 255
            0x00c080e5      push  0x1876198
            0x00c080ea      mov   eax, dword fs:[0x0]
            0x00c080f0      push  eax
            0x00c080f1      push  ecx
            0x00c080f2      push  esi
            0x00c080f3      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00c080f8      xor   eax, ebp
            0x00c080fa      push  eax
            0x00c080fb      lea   eax, dword [ebp-0x0c]
            0x00c080fe      mov   dword fs:[0x0], eax
            0x00c08104      mov   esi, ecx
            0x00c08106      mov   dword [ebp-0x10], esi
            0x00c08109      call  0xb4e0d0
            0x00c0810e      lea   ecx, dword [esi+0x0c]
            0x00c08111      mov   dword [ebp-0x04], 0x00
            0x00c08118      mov   dword [esi], 0x19b01b4               ; [0x19b01b4:4]=0xc090d0
            0x00c0811e      mov   dword [esi+0x08], 0x00
            0x00c08125      call  0xb43a40
            0x00c0812a      mov   dword [esi+0x1c], 0x00
            0x00c08131      mov   eax, esi
            0x00c08133      mov   dword [esi+0x20], 0x00
            0x00c0813a      mov   dword [esi+0x24], 0xffffffff         ; [0xffffffff:4]=-1 ; -1
            0x00c08141      mov   dword [esi+0x04], 0x02
            0x00c08148      mov   ecx, dword [ebp-0x0c]
            0x00c0814b      mov   dword fs:[0x0], ecx
            0x00c08152      pop   ecx
            0x00c08153      pop   esi
            0x00c08154      mov   esp, ebp
            0x00c08156      pop   ebp
            0x00c08157      ret
            0x00c08158      int3
            0x00c08159      int3
            0x00c0815a      int3
            0x00c0815b      int3
            0x00c0815c      int3
            0x00c0815d      int3
            0x00c0815e      int3
            0x00c0815f      int3
            0x00c08160      push  ecx
            0x00c08161      push  esi
            0x00c08162      push  dword [esp+0x0c]
            0x00c08166      mov   esi, ecx
            0x00c08168      mov   dword [esp+0x08], esi
            0x00c0816c      call  0xbe3be0
            0x00c08171      mov   dword [esi], 0x19b0134               ; [0x19b0134:4]=0xc09100
            0x00c08177      mov   eax, esi
            0x00c08179      pop   esi
            0x00c0817a      pop   ecx
            0x00c0817b      ret   0x04
            0x00c0817e      int3
            0x00c0817f      int3
            0x00c08180      push  ebp
            0x00c08181      mov   ebp, esp
            0x00c08183      push  0xffffffff                           ; 255
            0x00c08185      push  0x18761f4
            0x00c0818a      mov   eax, dword fs:[0x0]
            0x00c08190      push  eax
            0x00c08191      push  ecx
            0x00c08192      push  esi
            0x00c08193      push  edi
            0x00c08194      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00c08199      xor   eax, ebp
            0x00c0819b      push  eax
            0x00c0819c      lea   eax, dword [ebp-0x0c]
            0x00c0819f      mov   dword fs:[0x0], eax
            0x00c081a5      mov   edi, ecx
            0x00c081a7      mov   dword [ebp-0x10], edi
            0x00c081aa      mov   dword [ebp-0x04], 0x00
            0x00c081b1      call  0xb4e0d0
            0x00c081b6      mov   eax, dword [ebp+0x08]
            0x00c081b9      lea   ecx, dword [edi+0x1c]
            0x00c081bc      mov   dword [edi+0x08], eax
            0x00c081bf      mov   eax, dword [ebp+0x0c]
            0x00c081c2      mov   dword [edi], 0x19b0180               ; [0x19b0180:4]=0xc091b0
            0x00c081c8      mov   byte [ebp-0x04], 0x01
            0x00c081cc      movups xmm0, xmmword [eax]
            0x00c081cf      lea   eax, dword [ebp+0x10]
            0x00c081d2      push  eax
            0x00c081d3      movups xmmword [edi+0x0c], xmm0
            0x00c081d7      call  0xb2a2f0
            0x00c081dc      mov   eax, dword [ebp+0x5c]
            0x00c081df      xor   esi, esi
            0x00c081e1      mov   edx, dword [ebp+0x68]
            0x00c081e4      mov   dword [edi+0x68], eax
            0x00c081e7      mov   eax, dword [ebp+0x60]
            0x00c081ea      mov   dword [edi+0x6c], eax
            0x00c081ed      mov   eax, dword [ebp+0x64]
            0x00c081f0      mov   dword [edi+0x70], eax
            0x00c081f3      lea   eax, dword [edi+0x74]
            0x00c081f6      mov   dword [eax+0x10], 0x00
            0x00c081fd      lea   ecx, dword [eax+0x10]
            0x00c08200      mov   dword [ebp+0x08], ecx
            0x00c08203      lea   edi, dword [eax+0x14]
            0x00c08206      mov   ecx, dword [edx+0x14]
            0x00c08209      mov   dword [edi], ecx
            0x00c0820b      lea   ecx, dword [eax+0x18]
            0x00c0820e      mov   dword [ebp+0x60], ecx
            0x00c08211      mov   dword [ecx], 0x00
            0x00c08217      mov   ecx, edx
            0x00c08219      sub   ecx, eax
            0x00c0821b      mov   byte [ebp-0x04], 0x02
            0x00c0821f      mov   dword [ebp+0x0c], edi
            0x00c08222      mov   dword [ebp+0x5c], ecx
        .-> 0x00c08225      mov   edx, dword [edi]
        :   0x00c08227      mov   ecx, 0x04
        :   0x00c0822c      cmp   edx, ecx
        :   0x00c0822e      cmovb ecx, edx
        :   0x00c08231      cmp   esi, ecx
       ,==< 0x00c08233      jnb   0xc08243
       |:   0x00c08235      mov   ecx, dword [ebp+0x5c]
       |:   0x00c08238      inc   esi
       |:   0x00c08239      mov   ecx, dword [ecx+eax*1]
       |:   0x00c0823c      mov   dword [eax], ecx
       |:   0x00c0823e      add   eax, 0x04
       |`=< 0x00c08241      jmp   0xc08225
       `--> 0x00c08243      mov   edi, dword [ebp-0x10]
            0x00c08246      cmp   edx, 0x04                            ; 4
        ,=< 0x00c08249      jbe   0xc08295
        |   0x00c0824b      mov   ecx, dword [ebp+0x60]
        |   0x00c0824e      invalid
        |   0x00c0824f      inc   edx
            0x00c0fad0      push  ebp
            0x00c0fad1      mov   ebp, esp
            0x00c0fad3      push  0xffffffff                           ; 255
            0x00c0fad5      push  0x184d3f8
            0x00c0fada      mov   eax, dword fs:[0x0]
            0x00c0fae0      push  eax
            0x00c0fae1      sub   esp, 0x2c
            0x00c0fae4      push  esi
            0x00c0fae5      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00c0faea      xor   eax, ebp
            0x00c0faec      push  eax
            0x00c0faed      lea   eax, dword [ebp-0x0c]
            0x00c0faf0      mov   dword fs:[0x0], eax
            0x00c0faf6      mov   esi, ecx
            0x00c0faf8      push  dword [ebp+0x08]
            0x00c0fafb      lea   ecx, dword [ebp-0x38]
            0x00c0fafe      call  0xb580a0
            0x00c0fb03      push  dword [ebp+0x0c]
            0x00c0fb06      lea   eax, dword [ebp-0x38]
            0x00c0fb09      mov   dword [ebp-0x04], 0x00
            0x00c0fb10      push  eax
            0x00c0fb11      mov   ecx, esi
            0x00c0fb13      call  0xc06c20
            0x00c0fb18      lea   ecx, dword [ebp-0x38]
            0x00c0fb1b      call  0xb589a0
            0x00c0fb20      mov   ecx, dword [ebp-0x0c]
            0x00c0fb23      mov   dword fs:[0x0], ecx
            0x00c0fb2a      pop   ecx
            0x00c0fb2b      pop   esi
            0x00c0fb2c      mov   esp, ebp
            0x00c0fb2e      pop   ebp
            0x00c0fb2f      ret   0x08
            0x00c0fb32      int3
            0x00c0fb33      int3
            0x00c0fb34      int3
            0x00c0fb35      int3
            0x00c0fb36      int3
            0x00c0fb37      int3
            0x00c0fb38      int3
            0x00c0fb39      int3
            0x00c0fb3a      int3
            0x00c0fb3b      int3
            0x00c0fb3c      int3
            0x00c0fb3d      int3
            0x00c0fb3e      int3
            0x00c0fb3f      int3
            0x00c0fb40      push  ebp
            0x00c0fb41      mov   ebp, esp
            0x00c0fb43      push  0xffffffff                           ; 255
            0x00c0fb45      push  0x184d368
            0x00c0fb4a      mov   eax, dword fs:[0x0]
            0x00c0fb50      push  eax
            0x00c0fb51      sub   esp, 0x1c
            0x00c0fb54      push  esi
            0x00c0fb55      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00c0fb5a      xor   eax, ebp
            0x00c0fb5c      push  eax
            0x00c0fb5d      lea   eax, dword [ebp-0x0c]
            0x00c0fb60      mov   dword fs:[0x0], eax
            0x00c0fb66      mov   esi, ecx
            0x00c0fb68      push  dword [ebp+0x08]
            0x00c0fb6b      lea   ecx, dword [ebp-0x28]
            0x00c0fb6e      call  0xb58330
            0x00c0fb73      push  dword [ebp+0x0c]
            0x00c0fb76      lea   eax, dword [ebp-0x28]
            0x00c0fb79      mov   dword [ebp-0x04], 0x00
            0x00c0fb80      push  eax
            0x00c0fb81      mov   ecx, esi
            0x00c0fb83      call  0xc06e50
            0x00c0fb88      lea   ecx, dword [ebp-0x28]
            0x00c0fb8b      call  0xb589c0
            0x00c0fb90      mov   ecx, dword [ebp-0x0c]
            0x00c0fb93      mov   dword fs:[0x0], ecx
            0x00c0fb9a      pop   ecx
            0x00c0fb9b      pop   esi
            0x00c0fb9c      mov   esp, ebp
            0x00c0fb9e      pop   ebp
            0x00c0fb9f      ret   0x08
            0x00c0fba2      int3
            0x00c0fba3      int3
            0x00c0fba4      int3
            0x00c0fba5      int3
            0x00c0fba6      int3
            0x00c0fba7      int3
            0x00c0fba8      int3
            0x00c0fba9      int3
            0x00c0fbaa      int3
            0x00c0fbab      int3
            0x00c0fbac      int3
            0x00c0fbad      int3
            0x00c0fbae      int3
            0x00c0fbaf      int3
            0x00c0fbb0      push  ebp
            0x00c0fbb1      mov   ebp, esp
            0x00c0fbb3      push  0xffffffff                           ; 255
            0x00c0fbb5      push  0x184d3f8
            0x00c0fbba      mov   eax, dword fs:[0x0]
            0x00c0fbc0      push  eax
            0x00c0fbc1      sub   esp, 0x2c
            0x00c0fbc4      push  esi
            0x00c0fbc5      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00c0fbca      xor   eax, ebp
            0x00c0fbcc      push  eax
            0x00c0fbcd      lea   eax, dword [ebp-0x0c]
            0x00c0fbd0      mov   dword fs:[0x0], eax
            0x00c0fbd6      mov   esi, ecx
            0x00c0fbd8      push  dword [ebp+0x08]
            0x00c0fbdb      lea   ecx, dword [ebp-0x38]
            0x00c0fbde      call  0xb581e0
            0x00c0fbe3      push  dword [ebp+0x0c]
            0x00c0fbe6      lea   eax, dword [ebp-0x38]
            0x00c0fbe9      mov   dword [ebp-0x04], 0x00
            0x00c0fbf0      push  eax
            0x00c0fbf1      mov   ecx, esi
            0x00c0fbf3      call  0xc06c20
            0x00c0fbf8      lea   ecx, dword [ebp-0x38]
            0x00c0fbfb      call  0xb589a0
            0x00c0f530      push  ebp
            0x00c0f531      mov   ebp, esp
            0x00c0f533      push  0xffffffff                           ; 255
            0x00c0f535      push  0x184d3f8
            0x00c0f53a      mov   eax, dword fs:[0x0]
            0x00c0f540      push  eax
            0x00c0f541      sub   esp, 0x2c
            0x00c0f544      push  esi
            0x00c0f545      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00c0f54a      xor   eax, ebp
            0x00c0f54c      push  eax
            0x00c0f54d      lea   eax, dword [ebp-0x0c]
            0x00c0f550      mov   dword fs:[0x0], eax
            0x00c0f556      mov   esi, ecx
            0x00c0f558      push  dword [ebp+0x08]
            0x00c0f55b      lea   ecx, dword [ebp-0x38]
            0x00c0f55e      call  0xb580a0
            0x00c0f563      push  dword [ebp+0x0c]
            0x00c0f566      lea   eax, dword [ebp-0x38]
            0x00c0f569      mov   dword [ebp-0x04], 0x00
            0x00c0f570      push  eax
            0x00c0f571      mov   ecx, esi
            0x00c0f573      call  0xc06ba0
            0x00c0f578      lea   ecx, dword [ebp-0x38]
            0x00c0f57b      call  0xb589a0
            0x00c0f580      mov   ecx, dword [ebp-0x0c]
            0x00c0f583      mov   dword fs:[0x0], ecx
            0x00c0f58a      pop   ecx
            0x00c0f58b      pop   esi
            0x00c0f58c      mov   esp, ebp
            0x00c0f58e      pop   ebp
            0x00c0f58f      ret   0x08
            0x00c0f592      int3
            0x00c0f593      int3
            0x00c0f594      int3
            0x00c0f595      int3
            0x00c0f596      int3
            0x00c0f597      int3
            0x00c0f598      int3
            0x00c0f599      int3
            0x00c0f59a      int3
            0x00c0f59b      int3
            0x00c0f59c      int3
            0x00c0f59d      int3
            0x00c0f59e      int3
            0x00c0f59f      int3
            0x00c0f5a0      push  ebp
            0x00c0f5a1      mov   ebp, esp
            0x00c0f5a3      push  0xffffffff                           ; 255
            0x00c0f5a5      push  0x184d368
            0x00c0f5aa      mov   eax, dword fs:[0x0]
            0x00c0f5b0      push  eax
            0x00c0f5b1      sub   esp, 0x1c
            0x00c0f5b4      push  esi
            0x00c0f5b5      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00c0f5ba      xor   eax, ebp
            0x00c0f5bc      push  eax
            0x00c0f5bd      lea   eax, dword [ebp-0x0c]
            0x00c0f5c0      mov   dword fs:[0x0], eax
            0x00c0f5c6      mov   esi, ecx
            0x00c0f5c8      push  dword [ebp+0x08]
            0x00c0f5cb      lea   ecx, dword [ebp-0x28]
            0x00c0f5ce      invalid
            0x00c0f5cf      pop   ebp
       .--> 0x00c06b06      mov   eax, dword [edi+0x0c]
       ::   0x00c06b09      mov   ecx, ebx
       ::   0x00c06b0b      lea   eax, dword [eax+esi*4]
       ::   0x00c06b0e      test  ebp, ebp
      ,===< 0x00c06b10      jnz   0xc06b15
      |::   0x00c06b12      lea   ebx, dword [ebp-0x14]
      `---> 0x00c06b15      push  0x04                                 ; 4
       ::   0x00c06b17      push  eax
       ::   0x00c06b18      xor   eax, eax
       ::   0x00c06b1a      test  ebp, ebp
       ::   0x00c06b1c      cmovz ecx, eax
       ::   0x00c06b1f      call  0xb5abf0
       ::   0x00c06b24      inc   esi
       ::   0x00c06b25      cmp   esi, dword [esp+0x14]
       `==< 0x00c06b29      jb    0xc06b06
        :   0x00c06b2b      mov   eax, dword [esp+0x1c]
        :   0x00c06b2f      mov   ecx, dword [esp+0x20]
        :   0x00c06b33      inc   eax
        :   0x00c06b34      mov   ebx, dword [esp+0x2c]
        :   0x00c06b38      add   ecx, 0x14                            ; 20
        :   0x00c06b3b      mov   dword [esp+0x1c], eax
        :   0x00c06b3f      mov   dword [esp+0x20], ecx
        :   0x00c06b43      cmp   eax, dword [esp+0x10]
        `=< 0x00c06b47      jb    0xc06a40
            0x00c06b4d      pop   edi
            0x00c06b4e      pop   esi
            0x00c06b4f      pop   ebp
            0x00c06b50      pop   ebx
            0x00c06b51      add   esp, 0x18
            0x00c06b54      ret   0x08
            0x00c06b57      int3
            0x00c06b58      int3
            0x00c06b59      int3
            0x00c06b5a      int3
            0x00c06b5b      int3
            0x00c06b5c      int3
            0x00c06b5d      int3
            0x00c06b5e      int3
            0x00c06b5f      int3
            0x00c06b60      push  edi
            0x00c06b61      mov   edi, dword [esp+0x0c]
            0x00c06b65      test  edi, edi
        ,=< 0x00c06b67      jz    0xc06b90
        |   0x00c06b69      push  esi
        |   0x00c06b6a      mov   esi, dword [esp+0x0c]
        |   0x00c06b6e      lea   ecx, dword [edi+edi*2]
        |   0x00c06b71      shl   ecx, 0x04
        |   0x00c06b74      add   esi, 0xffffffd0                      ; 4294967248
        |   0x00c06b77      add   esi, ecx
        |   0x00c06b79      nop   dword [eax], eax
       .--> 0x00c06b80      mov   ecx, esi
       :|   0x00c06b82      call  0xc36a20
       :|   0x00c06b87      sub   esi, 0x30                            ; 48
       :|   0x00c06b8a      sub   edi, 0x01
       `==< 0x00c06b8d      jnz   0xc06b80
        |   0x00c06b8f      pop   esi
        `-> 0x00c06b90      pop   edi
            0x00c06b91      ret
            0x00c06b92      int3
            0x00c06b93      int3
            0x00c06b94      int3
            0x00c06b95      int3
            0x00c06b96      int3
            0x00c06b97      int3
            0x00c06b98      int3
            0x00c06b99      int3
            0x00c06b9a      int3
            0x00c06b9b      int3
            0x00c06b9c      int3
            0x00c06b9d      int3
            0x00c06b9e      int3
            0x00c06b9f      int3
            0x00c06ba0      push  ebx
            0x00c06ba1      push  esi
            0x00c06ba2      mov   esi, dword [esp+0x0c]
            0x00c06ba6      mov   ebx, ecx
            0x00c06ba8      push  edi
            0x00c06ba9      push  dword [esp+0x14]
            0x00c06bad      push  esi
            0x00c06bae      call  0xb53df0
            0x00c06bb3      push  0x00
            0x00c06bb5      lea   eax, dword [ebx+0x08]
            0x00c06bb8      lea   edi, dword [esi+0x14]
            0x00c06bbb      push  eax
            0x00c06bbc      mov   ecx, edi
            0x00c06bbe      call  0xb074c0
            0x00c06bc3      xor   eax, eax
            0x00c06bc5      lea   ecx, dword [ebx+0x0c]
            0x00c06bc8      test  edi, edi
            0x00c06bca      cmovz esi, eax
            0x00c06bcd      push  dword [esi+0x0c]
            0x00c06bd0      push  esi
            0x00c06bd1      call  0xbd01e0
            0x00c06bd6      lea   eax, dword [edi-0x14]
            0x00c06bd9      neg   edi
            0x00c06bdb      push  0x04                                 ; 4
            0x00c06bdd      sbb   edi, edi
            0x00c06bdf      and   edi, eax
            0x00c06be1      lea   eax, dword [ebx+0x1c]
            0x00c06be4      push  eax
            0x00c06be5      mov   ecx, edi
            0x00c06be7      call  0xb5abf0
            0x00c06bec      push  0x04                                 ; 4
            0x00c06bee      lea   eax, dword [esp+0x18]
            0x00c06bf2      mov   dword [esp+0x18], 0x00
            0x00c06bfa      push  eax
            0x00c06bfb      mov   ecx, edi
            0x00c06bfd      call  0xb5abf0
            0x00c06c02      mov   eax, dword [esp+0x14]
            0x00c06c06      mov   ecx, edi
            0x00c06c08      mov   dword [ebx+0x20], eax
            0x00c06c0b      lea   eax, dword [ebx+0x24]
            0x00c06c0e      push  0x04                                 ; 4
            0x00c06c10      push  eax
            0x00c06c11      call  0xb5abf0
            0x00c06c16      pop   edi
            0x00c06c17      pop   esi
            0x00c06c18      pop   ebx
            0x00c06c19      ret   0x08
            0x00c06c1c      int3
            0x00c06c1d      int3
            0x00c06c1e      int3
            0x00c06c1f      int3
            0x00c06c20      push  ebx
            0x00c06c21      push  esi
            0x00c06c22      mov   esi, dword [esp+0x0c]
            0x00c06c26      mov   ebx, ecx
            0x00c06c28      push  edi
            0x00c06c29      push  dword [esp+0x14]
            0x00c06c2d      push  esi
            0x00c06c2e      call  0xb53df0
            0x00c06c33      push  0x00
            0x00c06c35      lea   eax, dword [ebx+0x08]
            0x00c06c38      lea   edi, dword [esi+0x14]
            0x00c06c3b      push  eax
            0x00c06c3c      mov   ecx, edi
            0x00c06c3e      call  0xb074c0
            0x00c06c43      xor   eax, eax
            0x00c06c45      lea   ecx, dword [ebx+0x0c]
            0x00c06c48      test  edi, edi
            0x00c06c4a      cmovz esi, eax
            0x00c06c4d      push  dword [esi+0x0c]
            0x00c06c50      push  esi
            0x00c06c51      call  0xbd01e0
